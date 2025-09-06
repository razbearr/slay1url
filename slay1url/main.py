#slay1url/main.py
import validators
import secrets
from fastapi import FastAPI, HTTPException,Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from .database import sessionLocal, engine
from . import model, schemas

app = FastAPI()
model.Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return "URL shortner"

def raise_bad_request(message):
    raise HTTPException(status_code=400,detail=message)

def raise_not_found(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)

@app.post("/url",response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise_bad_request(message="Invalid URL")
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    key ="".join(secrets.choice(chars) for _ in range (6))
    secret_key ="".join(secrets.choice(chars) for _ in range (7))
    db_url = model.URL(target_url=url.target_url, key=key, secret_key=secret_key)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    db_url.url = key
    db_url.admin_url = secret_key
    return db_url

@app.get("/{url_key}")
def forward_to_target_url(url_key: str,request: Request,db: Session = Depends(get_db)):
    db_url = (db.query(model.URL).filter(model.URL.key == url_key, model.URL.is_active).first())
    if db_url:
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)
