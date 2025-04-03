from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from models import EventStatus

class EventCreate(BaseModel):
    name: str
    description: str
    start_time: datetime
    end_time: datetime
    location: str
    max_attendees: int =20

class EventUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    max_attendees: Optional[int] = None
    status: Optional[EventStatus] = None

class AttendeeCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    event_id: int

class AttendeeCheckIn(BaseModel):
    attendee_id: int

class AttendeeResponse(BaseModel):
    attendee_id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    check_in_status: bool

class EventResponse(BaseModel):
    event_id: int
    name: str
    description: str
    start_time: datetime
    end_time: datetime
    location: str
    max_attendees: int
    status: EventStatus