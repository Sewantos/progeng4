from fastapi import FastAPI
from .database import engine
from .models import Base
from .routers import students, groups


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(students.router)
app.include_router(groups.router)
