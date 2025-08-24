from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from app.database import get_session
from app.models import Task



router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# Afficher les tâches (avec recherche)
@router.get("/tasks", response_class=HTMLResponse)
async def show_tasks(request: Request, q: str = "", db: Session = Depends(get_session)):
    statement = select(Task)
    if q:
        statement = statement.where(Task.title.contains(q))
    tasks = db.exec(statement).all()
    return templates.TemplateResponse("tasks.html", {
        "request": request,
        "tasks": tasks,
        "query": q
    })

@router.post("/tasks", response_class=HTMLResponse)
async def add_task(
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_session),
):

    new_task = Task(title=title, description=description)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    tasks = db.exec(select(Task)).all()
    return templates.TemplateResponse(
        "tasks.html",
        {"request": request, "message": f"Tâche '{title}' ajoutée !", "tasks": tasks}
    )


#  Supprimer une tâche
@router.post("/tasks/delete", response_class=HTMLResponse)
async def delete_task(
    request: Request,
    task_id: int = Form(...),
    db: Session = Depends(get_session),
):
    task = db.get(Task, task_id)
    if task:
        db.delete(task)
        db.commit()
    tasks = db.exec(select(Task)).all()
    return templates.TemplateResponse(
        "tasks.html",
        {"request": request, "message": "Tâche supprimée", "tasks": tasks}
    )

