from sqlalchemy.orm import Session
import models, schemas
import uuid
from sqlalchemy import func
from datetime import datetime, timedelta

def create_fiche_poste(db: Session, fiche: schemas.FichePosteCreate):
    db_fiche = models.FichePoste(**fiche.dict())
    db.add(db_fiche)
    db.commit()
    db.refresh(db_fiche)
    return db_fiche

def get_fiche_poste(db: Session, fiche_id: int):
    return db.query(models.FichePoste).filter(models.FichePoste.id == fiche_id).first()

def create_quiz(db: Session, quiz: schemas.QuizCreate, createur_id: int):
    db_quiz = models.Quiz(titre=quiz.titre, fiche_poste_id=quiz.fiche_poste_id, createur_id=createur_id)
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    for q in quiz.questions:
        db_question = models.Question(texte=q.texte, quiz_id=db_quiz.id)
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
    return db_quiz

def get_quiz(db: Session, quiz_id: int):
    return db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()

def create_lien_candidat(db: Session, quiz_id: int, email: str):
    token = str(uuid.uuid4())
    db_lien = models.LienCandidat(quiz_id=quiz_id, email=email, token=token)
    db.add(db_lien)
    db.commit()
    db.refresh(db_lien)
    return db_lien

def get_lien_candidat(db: Session, token: str):
    return db.query(models.LienCandidat).filter(models.LienCandidat.token == token).first()

def create_resultat(db: Session, resultat: schemas.ResultatCreate):
    db_resultat = models.Resultat(**resultat.dict())
    db.add(db_resultat)
    db.commit()
    db.refresh(db_resultat)
    return db_resultat

def get_resultats_by_quiz(db: Session, quiz_id: int):
    return db.query(models.Resultat).join(models.LienCandidat).filter(models.LienCandidat.quiz_id == quiz_id).all()

def create_reponse_candidat(db: Session, reponse: schemas.ReponseCandidatCreate):
    db_reponse = models.ReponseCandidat(**reponse.dict())
    db.add(db_reponse)
    db.commit()
    db.refresh(db_reponse)
    return db_reponse

def get_reponses_candidat(db: Session, lien_candidat_id: int):
    return db.query(models.ReponseCandidat).filter(models.ReponseCandidat.lien_candidat_id == lien_candidat_id).all()

def get_quizzes(db: Session):
    return db.query(models.Quiz).all() 

def count_quizzes(db: Session):
    return db.query(models.Quiz).count()

def count_liens(db: Session):
    return db.query(models.LienCandidat).count()

def count_resultats(db: Session):
    return db.query(models.Resultat).count()

def count_resultats_en_attente(db: Session):
    # Un lien sans résultat associé = en attente
    total_liens = db.query(models.LienCandidat).count()
    total_resultats = db.query(models.Resultat).count()
    return total_liens - total_resultats

def quizzes_per_month(db: Session, months: int = 12):
    now = datetime.now()
    start = now - timedelta(days=30*months)
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
    return results

def score_distribution(db: Session):
    # Exemple de tranches : 0-5, 6-10, 11-15, 16-20
    bins = [(0,5), (6,10), (11,15), (16,20)]
    dist = []
    for b in bins:
        count = db.query(models.Resultat).filter(models.Resultat.score >= b[0], models.Resultat.score <= b[1]).count()
        dist.append({'range': f'{b[0]}-{b[1]}', 'count': count})
    return dist 