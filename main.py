from fastapi import FastAPI
from models import Base
from database import engine
from routes.event_routes import router as event_router
from routes.attendee import router as attendee_router

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(event_router)
app.include_router(attendee_router)

@app.get('/')
def read_root():
    return {'message':'Welcome to the Event Management API'}