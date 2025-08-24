# main.py
from fastapi import FastAPI
from app.routes import auth, tasks
from app.middleware import log_middleware  
from app.database import create_db_and_tables 

app = FastAPI()

#  Initialise la base de données 
create_db_and_tables()

#  Ajoute le middleware 
app.middleware("http")(log_middleware)

#  Ajoute les routes
app.include_router(auth.router)
app.include_router(tasks.router)
