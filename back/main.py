from fastapi import FastAPI, Depends, HTTPException, status, Body
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
    # Appel à l'IA pour générer les questions
    result = await ai.generate_quiz(fiche.description, fiche.entreprise)
    # On suppose que l'IA retourne une liste de questions (à adapter selon le retour réel)
    questions = result.get("questions", [])
    quiz_data = schemas.QuizCreate(titre=f"Quiz pour {fiche.titre}", fiche_poste_id=fiche.id, questions=[schemas.QuestionCreate(texte=q) for q in questions])
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
    score = body.get("score")
    reponses = body.get("reponses", [])
    # Sauvegarde du score
    resultat = crud.create_resultat(db, schemas.ResultatCreate(lien_candidat_id=lien.id, score=score))
    # Sauvegarde des réponses du candidat
    for rep in reponses:
        # On cherche la question, sinon on la crée
        question_obj = db.query(models.Question).filter(models.Question.texte == rep["question"]).first()
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
    return {"resultat_id": resultat.id, "msg": "Réponses et score enregistrés"}

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

