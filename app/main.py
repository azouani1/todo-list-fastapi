# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import auth, tasks
from app.middleware import log_middleware  
from app.database import create_db_and_tables 

app = FastAPI()

# Sert les fichiers statiques (CSS, images, etc.)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

#  Initialise la base de données 
create_db_and_tables()

#  Ajoute le middleware 
app.middleware("http")(log_middleware)

#  Ajoute les routes
app.include_router(auth.router)
app.include_router(tasks.router)
