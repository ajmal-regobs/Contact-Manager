from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlalchemy.orm import Session

from app.database import Base, LogsBase, engine, get_db, get_logs_db, logs_engine
from app.models import CallLog, Contact
from app.schemas import CallLogResponse, ContactCreate, ContactResponse

app = FastAPI(title="Contact Manager")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    LogsBase.metadata.create_all(bind=logs_engine)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    response: Response = await call_next(request)
    db = next(get_logs_db())
    try:
        log = CallLog(
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
        )
        db.add(log)
        db.commit()
    finally:
        db.close()
    return response


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/contacts", response_model=ContactResponse, status_code=201)
def add_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    existing = db.query(Contact).filter(Contact.email == contact.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Contact with this email already exists")

    db_contact = Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@app.delete("/contacts/{contact_id}", status_code=200)
def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    db.delete(contact)
    db.commit()
    return {"message": "Contact deleted successfully"}


@app.get("/contacts", response_model=list[ContactResponse])
def list_contacts(db: Session = Depends(get_db)):
    return db.query(Contact).all()


@app.get("/logs", response_model=list[CallLogResponse])
def list_logs(db: Session = Depends(get_logs_db)):
    return db.query(CallLog).order_by(CallLog.timestamp.desc()).all()
