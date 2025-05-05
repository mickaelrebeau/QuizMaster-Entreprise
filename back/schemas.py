from pydantic import BaseModel, EmailStr
from typing import List, Optional
import datetime

class UserBase(BaseModel):
    email: EmailStr
    is_rh: Optional[bool] = False

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        orm_mode = True

class FichePosteBase(BaseModel):
    titre: str
    description: str
    entreprise: str

class FichePosteCreate(FichePosteBase):
    pass

class FichePoste(FichePosteBase):
    id: int
    class Config:
        orm_mode = True

class QuestionBase(BaseModel):
    texte: str

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int
    class Config:
        orm_mode = True

class ReponseBase(BaseModel):
    texte: str
    is_correct: Optional[bool] = False

class ReponseCreate(ReponseBase):
    pass

class Reponse(ReponseBase):
    id: int
    class Config:
        orm_mode = True

class QuizBase(BaseModel):
    titre: str
    fiche_poste_id: int

class QuizCreate(QuizBase):
    questions: List[QuestionCreate]

class Quiz(QuizBase):
    id: int
    questions: List[Question] = []
    class Config:
        orm_mode = True

class LienCandidatBase(BaseModel):
    quiz_id: int
    email: EmailStr

class LienCandidatCreate(LienCandidatBase):
    pass

class LienCandidat(LienCandidatBase):
    id: int
    token: str
    class Config:
        orm_mode = True

class ResultatBase(BaseModel):
    lien_candidat_id: int
    score: int

class ResultatCreate(ResultatBase):
    pass

class Resultat(ResultatBase):
    id: int
    date: datetime.datetime
    class Config:
        orm_mode = True

class ReponseCandidatBase(BaseModel):
    lien_candidat_id: int
    question_id: int
    reponse_id: int

class ReponseCandidatCreate(ReponseCandidatBase):
    pass

class ReponseCandidat(ReponseCandidatBase):
    id: int
    class Config:
        orm_mode = True 