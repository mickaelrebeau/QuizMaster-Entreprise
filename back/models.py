from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Boolean
from sqlalchemy.orm import relationship, declarative_base
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_rh = Column(Boolean, default=False)
    quizzes = relationship('Quiz', back_populates='createur')

class FichePoste(Base):
    __tablename__ = 'fiches_poste'
    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String, index=True)
    description = Column(Text)
    entreprise = Column(String)
    quizzes = relationship('Quiz', back_populates='fiche_poste')

class Quiz(Base):
    __tablename__ = 'quizzes'
    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String)
    date_creation = Column(DateTime, default=datetime.datetime.utcnow)
    createur_id = Column(Integer, ForeignKey('Users.id'))
    fiche_poste_id = Column(Integer, ForeignKey('fiches_poste.id'))
    questions = relationship('Question', back_populates='quiz')
    createur = relationship('User', back_populates='quizzes')
    fiche_poste = relationship('FichePoste', back_populates='quizzes')

class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, index=True)
    texte = Column(Text)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'))
    quiz = relationship('Quiz', back_populates='questions')
    reponses = relationship('Reponse', back_populates='question')

class Reponse(Base):
    __tablename__ = 'reponses'
    id = Column(Integer, primary_key=True, index=True)
    texte = Column(Text)
    question_id = Column(Integer, ForeignKey('questions.id'))
    question = relationship('Question', back_populates='reponses')
    is_correct = Column(Boolean, default=False)

class LienCandidat(Base):
    __tablename__ = 'liens_candidats'
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'))
    token = Column(String, unique=True, index=True)
    email = Column(String)
    quiz = relationship('Quiz')

class Resultat(Base):
    __tablename__ = 'resultats'
    id = Column(Integer, primary_key=True, index=True)
    lien_candidat_id = Column(Integer, ForeignKey('liens_candidats.id'))
    score = Column(Integer)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    lien_candidat = relationship('LienCandidat')

class ReponseCandidat(Base):
    __tablename__ = 'reponses_candidats'
    id = Column(Integer, primary_key=True, index=True)
    lien_candidat_id = Column(Integer, ForeignKey('liens_candidats.id'))
    question_id = Column(Integer, ForeignKey('questions.id'))
    reponse_id = Column(Integer, ForeignKey('reponses.id'))
    lien_candidat = relationship('LienCandidat')
    question = relationship('Question')
    reponse = relationship('Reponse') 