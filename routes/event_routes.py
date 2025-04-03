from schemas import EventCreate,EventResponse,EventStatus,EventUpdate,AttendeeResponse
from typing import List, Optional
from models import EventStatus,Event,Attendee
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db

router = APIRouter()

def update_event_status(db: Session):
    events = db.query(Event).all()
    for event in events:
        if event.end_time < datetime.now() and event.status != 'completed':
            event.status = 'completed'
            db.add(event)
    db.commit()

# Create Event: Endpoint to create new events. Status is initialized as 'scheduled'.
@router.post("/events/", response_model=EventResponse)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    db_event = Event(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    update_event_status(db) 
    return db_event

#Update Event: Endpoint to update event details and modify the status.
@router.put("/events/{event_id}", response_model=EventResponse)
def update_event(event_id: int, event: EventUpdate, db: Session = Depends(get_db)):
    db_event = db.query(Event).filter(Event.event_id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    for key, value in event.model_dump(exclude_unset=True).items():
        setattr(db_event, key, value)
    
    db.commit()
    db.refresh(db_event)
    return db_event


#List Events: Fetch events with filters (status, location, date).
@router.get("/events/", response_model=List[EventResponse])
def list_events(status: Optional[EventStatus] = None, location: Optional[str] = None,start_time: Optional[datetime] = None, end_time: Optional[datetime] = None, db: Session = Depends(get_db)):
    #Automatically set event status to 'completed' if the end_time has passed.
    update_event_status(db)
    query = db.query(Event)
    if status:
        query = query.filter(Event.status == status)
    if location:
        query = query.filter(Event.location == location)
    if start_time:
        query = query.filter(Event.start_time >= start_time)
    if end_time:
        query = query.filter(Event.end_time <= end_time)
    events = query.all()
    return events

@router.get("/events/{event_id}/", response_model=EventResponse)   
def get_event(event_id: int, db: Session = Depends(get_db)):
    #Automatically set event status to 'completed' if the end_time has passed.
    update_event_status(db)  
    event = db.query(Event).filter(Event.event_id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found.")
    return event

#List Attendees: Retrieve attendees for a specific event with optional filters.
@router.get("/events/{event_id}/attendees/", response_model=List[AttendeeResponse])
def list_attendees(event_id: int, db: Session = Depends(get_db)):
    attendees = db.query(Attendee).filter(Attendee.event_id == event_id).all()
    return attendees