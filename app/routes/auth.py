# app/routes/auth.py

from fastapi import APIRouter, Request, Form, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select
from app.models import User
from app.database import get_session
from fastapi.templating import Jinja2Templates
from passlib.hash import bcrypt

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
def register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    user_exists = session.exec(select(User).where(User.username == username)).first()
    if user_exists:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Nom d'utilisateur déjà pris"})

    hashed_pw = bcrypt.hash(password)
    new_user = User(username=username, password=hashed_pw)
    session.add(new_user)
    session.commit()
    return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)

@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    user = session.exec(select(User).where(User.username == username)).first()
    if not user or not bcrypt.verify(password, user.password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Identifiants invalides"})

    return RedirectResponse("/dashboard", status_code=status.HTTP_302_FOUND)

    response = RedirectResponse("/tasks", status_code=302)
    response.set_cookie("user_id", user.id)
    return response

@router.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("user_id")
    return response