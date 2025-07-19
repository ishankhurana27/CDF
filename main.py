from fastapi import FastAPI
from app import api
from app.database import Base, engine

app = FastAPI()
app.include_router(api.router)

Base.metadata.create_all(bind=engine)
