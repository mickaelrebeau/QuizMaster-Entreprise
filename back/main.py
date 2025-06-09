from fastapi import FastAPI, Depends, HTTPException, status, Body, Request
from database import engine, Base, SessionLocal
import models, ai, crud, schemas
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import asyncio
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from typing import List
import uvicorn
import json
import re
from sqlalchemy import func

app = FastAPI()

# CORS pour le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "supersecretkey"  # À remplacer par une vraie clé secrète
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Auth utils ---
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"msg": "QuizMaster Entreprise API"}

# --- Fiches de poste ---
@app.post("/fiche-poste", response_model=schemas.FichePoste)
def create_fiche_poste(fiche: schemas.FichePosteCreate, db: Session = Depends(get_db)):
    return crud.create_fiche_poste(db, fiche)

@app.get("/fiche-poste/{fiche_id}", response_model=schemas.FichePoste)
def get_fiche_poste(fiche_id: int, db: Session = Depends(get_db)):
    fiche = crud.get_fiche_poste(db, fiche_id)
    if not fiche:
        raise HTTPException(status_code=404, detail="Fiche de poste non trouvée")
    return fiche

@app.get("/fiches-poste", response_model=List[schemas.FichePoste])
def get_all_fiches_poste(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.FichePoste).all()

# --- Génération de quiz via IA ---
@app.post("/quiz/generer")
async def generer_quiz(fiche_id: int, db: Session = Depends(get_db)):
    fiche = crud.get_fiche_poste(db, fiche_id)
    if not fiche:
        raise HTTPException(status_code=404, detail="Fiche de poste non trouvée")
    max_attempts = 5
    for attempt in range(max_attempts):
        result = await ai.generate_quiz(fiche.description, fiche.entreprise)
        try:
            ia_json = result.get("message")
            if isinstance(ia_json, str):
                match = re.search(r"\{.*\}", ia_json, re.DOTALL)
                if match:
                    ia_json = json.loads(match.group(0))
                else:
                    raise ValueError("Aucun JSON trouvé dans la réponse IA :\n" + ia_json)
            # Validation stricte : doit contenir une liste non vide de questions
            questions = ia_json.get("questions", [])
            if not isinstance(questions, list) or not questions:
                raise ValueError("Le JSON IA ne contient pas de questions valides.")
            # Validation de la structure de chaque question
            for q in questions:
                if not (isinstance(q, dict) and "question" in q and "reponses" in q and "reponse_correcte" in q):
                    raise ValueError(f"Question mal formée : {q}")
                if not (isinstance(q["reponses"], list) and len(q["reponses"]) == 4):
                    raise ValueError(f"Question sans 4 réponses : {q}")
            break  # JSON valide, on sort de la boucle
        except Exception as e:
            print(f"[Tentative {attempt+1}] Erreur parsing JSON IA:", e)
            print("Réponse brute IA:", result.get("message"))
            if attempt == max_attempts - 1:
                raise HTTPException(status_code=500, detail=f"Impossible d'obtenir un quiz IA valide après {max_attempts} tentatives.")
            continue  # On relance la génération
    # On prépare les questions et réponses pour l'enregistrement
    questions_data = []
    for q in questions:
        reponses = []
        for rep in q.get("reponses", []):
            is_correct = (rep == q.get("reponse_correcte"))
            reponses.append(schemas.ReponseCreate(texte=rep, is_correct=is_correct))
        questions_data.append(schemas.QuestionCreate(
            texte=q.get("question", ""),
            reponses=reponses
        ))
    quiz_data = schemas.QuizCreate(
        titre=f"Quiz pour {fiche.titre}",
        fiche_poste_id=fiche.id,
        questions=questions_data
    )
    quiz = crud.create_quiz(db, quiz_data, createur_id=1)  # TODO: remplacer par l'ID du RH connecté
    return {"quiz_id": quiz.id}

# --- Récupération d'un quiz ---
@app.get("/quiz/{quiz_id}", response_model=schemas.Quiz)
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = crud.get_quiz(db, quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz non trouvé")
    return quiz

# --- Génération de lien candidat ---
@app.post("/candidat/lien")
def generer_lien_candidat(data: schemas.LienCandidatBase, db: Session = Depends(get_db)):
    lien = crud.create_lien_candidat(db, data.quiz_id, data.email)
    return {"lien": f"/candidat/quiz/{lien.token}"}

# --- Accès au quiz pour le candidat via token ---
@app.get("/candidat/quiz/{token}", response_model=schemas.Quiz)
def get_quiz_candidat(token: str, db: Session = Depends(get_db)):
    lien = crud.get_lien_candidat(db, token)
    if not lien:
        raise HTTPException(status_code=404, detail="Lien invalide")
    quiz = crud.get_quiz(db, lien.quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz non trouvé")
    return quiz

# --- Soumission des réponses (simplifiée) ---
@app.post("/candidat/quiz/{token}/repondre")
def repondre_quiz(token: str, db: Session = Depends(get_db), body: dict = Body(...)):
    lien = crud.get_lien_candidat(db, token)
    if not lien:
        raise HTTPException(status_code=404, detail="Lien invalide")
    # Vérification : le candidat a-t-il déjà répondu ?
    deja_repondu = db.query(models.Resultat).filter(models.Resultat.lien_candidat_id == lien.id).first()
    if deja_repondu:
        raise HTTPException(status_code=400, detail="Vous avez déjà répondu à ce quiz.")
    reponses = body.get("reponses", [])
    score = 0
    for rep in reponses:
        question_obj = db.query(models.Question).filter(models.Question.texte == rep["question"]).first()
        if not question_obj:
            continue
        bonne_reponse = db.query(models.Reponse).filter(models.Reponse.question_id == question_obj.id, models.Reponse.is_correct == True).first()
        if bonne_reponse and rep["reponse"] == bonne_reponse.texte:
            score += 1
        # On cherche la question, sinon on la crée
        if not question_obj:
            # On relie la question au quiz du lien
            question_obj = models.Question(texte=rep["question"], quiz_id=lien.quiz_id)
            db.add(question_obj)
            db.commit()
            db.refresh(question_obj)
            print(f"[LOG] Question créée : {rep['question']}")
        # On cherche la réponse, sinon on la crée
        reponse_obj = db.query(models.Reponse).filter(models.Reponse.texte == rep["reponse"], models.Reponse.question_id == question_obj.id).first()
        if not reponse_obj:
            reponse_obj = models.Reponse(texte=rep["reponse"], question_id=question_obj.id, is_correct=False)
            db.add(reponse_obj)
            db.commit()
            db.refresh(reponse_obj)
            print(f"[LOG] Réponse créée : {rep['reponse']} pour question {rep['question']}")
        crud.create_reponse_candidat(db, schemas.ReponseCandidatCreate(
            lien_candidat_id=lien.id,
            question_id=question_obj.id,
            reponse_id=reponse_obj.id
        ))
    # Enregistre le score calculé
    resultat = crud.create_resultat(db, schemas.ResultatCreate(lien_candidat_id=lien.id, score=score))
    return {"resultat_id": resultat.id, "score": score, "msg": "Réponses et score enregistrés"}

@app.get("/candidat/quiz/{token}/reponses-detaillees")
def get_reponses_detaillees(token: str, db: Session = Depends(get_db)):
    lien = crud.get_lien_candidat(db, token)
    if not lien:
        raise HTTPException(status_code=404, detail="Lien invalide")
    reponses_candidat = crud.get_reponses_candidat(db, lien.id)
    result = []
    for rep_cand in reponses_candidat:
        question = db.query(models.Question).filter(models.Question.id == rep_cand.question_id).first()
        reponse = db.query(models.Reponse).filter(models.Reponse.id == rep_cand.reponse_id).first()
        bonne_reponse = db.query(models.Reponse).filter(models.Reponse.question_id == question.id, models.Reponse.is_correct == True).first()
        result.append({
            "question": question.texte if question else None,
            "reponse_choisie": reponse.texte if reponse else None,
            "bonne_reponse": bonne_reponse.texte if bonne_reponse else None
        })
    return result

# --- Résultats pour un quiz ---
@app.get("/quiz/{quiz_id}/resultats")
def get_resultats(quiz_id: int, db: Session = Depends(get_db)):
    resultats = crud.get_resultats_by_quiz(db, quiz_id)
    return resultats

# --- Auth endpoints ---
@app.post("/auth/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password, is_rh=user.is_rh)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/auth/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

# --- Endpoint pour soumettre les réponses du candidat (en lot) ---
@app.post("/candidat/quiz/{token}/reponses")
def enregistrer_reponses(token: str, reponses: List[schemas.ReponseCandidatCreate], db: Session = Depends(get_db)):
    lien = crud.get_lien_candidat(db, token)
    if not lien:
        raise HTTPException(status_code=404, detail="Lien invalide")
    for rep in reponses:
        if rep.lien_candidat_id != lien.id:
            raise HTTPException(status_code=400, detail="Mauvais lien_candidat_id")
        crud.create_reponse_candidat(db, rep)
    return {"msg": "Réponses enregistrées"}

@app.get("/candidat/quiz/{token}/reponses", response_model=List[schemas.ReponseCandidat])
def get_reponses_candidat(token: str, db: Session = Depends(get_db)):
    lien = crud.get_lien_candidat(db, token)
    if not lien:
        raise HTTPException(status_code=404, detail="Lien invalide")
    return crud.get_reponses_candidat(db, lien.id)

@app.get("/quizzes", response_model=List[schemas.Quiz])
def get_quizzes(db: Session = Depends(get_db)):
    return crud.get_quizzes(db)

@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    nb_quiz = crud.count_quizzes(db)
    nb_liens = crud.count_liens(db)
    nb_resultats_recus = crud.count_resultats(db)
    nb_resultats_en_attente = crud.count_resultats_en_attente(db)
    return {
        "nb_quiz": nb_quiz,
        "nb_liens": nb_liens,
        "nb_resultats_recus": nb_resultats_recus,
        "nb_resultats_en_attente": nb_resultats_en_attente
    }

@app.get("/stats/quizzes-per-month")
def get_quizzes_per_month(db: Session = Depends(get_db)):
    results = crud.quizzes_per_month(db)
    # results = [(month, count), ...] => [{'month': month, 'count': count}, ...]
    return [{"month": r[0], "count": r[1]} for r in results]

@app.get("/stats/score-distribution")
def get_score_distribution(db: Session = Depends(get_db)):
    return crud.score_distribution(db)

@app.get("/liens-candidats")
def get_all_liens_candidats(db: Session = Depends(get_db)):
    liens = db.query(models.LienCandidat).all()
    return [{
        "id": lien.id,
        "quiz_id": lien.quiz_id,
        "email": lien.email,
        "token": lien.token,
        "date_creation": lien.date_creation if hasattr(lien, 'date_creation') else None
    } for lien in liens]

@app.delete("/quiz/{quiz_id}")
def delete_quiz_endpoint(quiz_id: int, db: Session = Depends(get_db)):
    success = crud.delete_quiz(db, quiz_id)
    if not success:
        raise HTTPException(status_code=404, detail="Quiz non trouvé")
    return {"msg": "Quiz supprimé"}

@app.get("/stats/evolution")
def get_stats_evolution(
    type_data: str = "quiz",  # quiz, score, liens, completion
    months: int = 12,
    db: Session = Depends(get_db)
):
    now = datetime.now()
    start = now - timedelta(days=30*months)
    
    if type_data == "quiz":
        results = (
            db.query(
                func.to_char(models.Quiz.date_creation, 'YYYY-MM').label('month'),
                func.count(models.Quiz.id)
            )
            .filter(models.Quiz.date_creation >= start)
            .group_by('month')
            .order_by('month')
            .all()
        )
    elif type_data == "score":
        results = (
            db.query(
                func.to_char(models.Resultat.date, 'YYYY-MM').label('month'),
                func.avg(models.Resultat.score)
            )
            .filter(models.Resultat.date >= start)
            .group_by('month')
            .order_by('month')
            .all()
        )
    elif type_data == "liens":
        results = (
            db.query(
                func.to_char(models.LienCandidat.date_creation, 'YYYY-MM').label('month'),
                func.count(models.LienCandidat.id)
            )
            .filter(models.LienCandidat.date_creation >= start)
            .group_by('month')
            .order_by('month')
            .all()
        )
    elif type_data == "completion":
        # Calcul du taux de complétion par mois
        results = []
        current = start
        while current <= now:
            month = current.strftime('%Y-%m')
            # Nombre total de liens créés ce mois
            total_liens = db.query(models.LienCandidat).filter(
                func.to_char(models.LienCandidat.date_creation, 'YYYY-MM') == month
            ).count()
            # Nombre de résultats reçus ce mois
            resultats = db.query(models.Resultat).filter(
                func.to_char(models.Resultat.date, 'YYYY-MM') == month
            ).count()
            # Calcul du taux
            taux = (resultats / total_liens * 100) if total_liens > 0 else 0
            results.append((month, taux))
            current = (current.replace(day=1) + timedelta(days=32)).replace(day=1)
    else:
        raise HTTPException(status_code=400, detail="Type de données invalide")
    
    return [{"month": r[0], "value": float(r[1])} for r in results]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

