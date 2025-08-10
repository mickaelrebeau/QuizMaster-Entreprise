import re
from fastapi import FastAPI, Depends
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request, HTTPException
from starlette.responses import JSONResponse
import time
from database import engine, Base, SessionLocal
from sqlalchemy.orm import Session
from crud import create_lead
from schemas import LeadCreate

rate_limit_storage = {}

RATE_LIMIT = 100  
RATE_PERIOD = 15 * 60 

app = FastAPI(
    title="QuizMaster Landing Backend",
    description="API for the QuizMaster Landing Page",
    version="1.0.0",
    contact={
        "name": "Mickael Rébeau",
        "email": "rebeau.mickael@gmail.com"
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mickaelrebeau.github.io", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    ip = request.client.host
    now = int(time.time())
    window_start = now - RATE_PERIOD

    timestamps = rate_limit_storage.get(ip, [])
    timestamps = [ts for ts in timestamps if ts > window_start]
    if len(timestamps) >= RATE_LIMIT:
        return JSONResponse(
            status_code=429,
            content={"detail": "Trop de requêtes depuis cette IP, veuillez réessayer plus tard."}
        )
    timestamps.append(now)
    rate_limit_storage[ip] = timestamps

    response = await call_next(request)
    return response

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def email_is_valid(email: str):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/demo")
async def demo(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    name = data.get("name")
    email = data.get("email")
    company = data.get("company")
    phone = data.get("phone")
    message = data.get("message")

    if not name or not email or not company or not phone:
        return JSONResponse(
            status_code=400,
            content={"detail": "Tous les champs sont obligatoires"}
        )
    
    if not email_is_valid(email):
        return JSONResponse(
            status_code=400,
            content={"detail": "Format d'email invalide"}
        )
    
    lead_data = LeadCreate(
        name=name,
        email=email,
        company=company,
        phone=phone,
        message=message,
        form_type="demo"
    )
    create_lead(db, lead_data)
    return JSONResponse(
        status_code=201,
        content={"success": True, "message": "Demande de démo enregistrée avec succès"}
    )
    
@app.post("/api/preinscription")
async def preinscription(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    name = data.get("name")
    email = data.get("email")
    company = data.get("company")

    if not name or not email or not company:
        return JSONResponse(
            status_code=400,
            content={"detail": "Tous les champs sont obligatoires"}
        )
    
    if not email_is_valid(email):
        return JSONResponse(
            status_code=400,
            content={"detail": "Format d'email invalide"}
        )

    lead_data = LeadCreate(
        name=name,
        email=email,
        company=company,
        form_type="preinscription"
    )
    create_lead(db, lead_data)
    return JSONResponse(
        status_code=201,
        content={"success": True, "message": "Inscription à la bêta enregistrée avec succès"}
    )

@app.post("/api/contact")
async def contact(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    if not name or not email or not message:
        return JSONResponse(
            status_code=400,
            content={"detail": "Tous les champs sont obligatoires"}
        )
    
    if not email_is_valid(email):
        return JSONResponse(
            status_code=400,
            content={"detail": "Format d'email invalide"}
        )
    
    lead_data = LeadCreate(
        name=name,
        email=email,
        message=message,
        form_type="contact"
    )
    create_lead(db, lead_data)
    return JSONResponse(
        status_code=201,
        content={"success": True, "message": "Message envoyé avec succès"}
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
