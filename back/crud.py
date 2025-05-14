from sqlalchemy.orm import Session
import models, schemas
import uuid

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