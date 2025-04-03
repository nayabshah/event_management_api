from fastapi import APIRouter,Depends,HTTPException,UploadFile, File
from database import get_db
from sqlalchemy.orm import Session
from models import Event, Attendee
from schemas import AttendeeResponse,AttendeeCreate,AttendeeCheckIn
from sqlalchemy.exc import IntegrityError
import io
import pandas as pd

router = APIRouter()



#Bulk check-in via CSV upload
@router.post("/attendees/bulk-checkin/")
async def check_in_attendees(file: UploadFile , db: Session = Depends(get_db)):
   
    contents = file.file.read()
    df = pd.read_csv(io.BytesIO(contents))
   
    if 'attendee_id' not in df.columns:
        raise HTTPException(status_code=400, detail="CSV must contain 'attendee_id' column.")

    results = []
    for attendee_id in df['attendee_id']:
        db_attendee = db.query(Attendee).filter(Attendee.attendee_id == attendee_id).first()
        if db_attendee:
            if not db_attendee.check_in_status:
                db_attendee.check_in_status = True
                results.append({"attendee_id": attendee_id, "status": "checked in"})
            else:
                results.append({"attendee_id": attendee_id, "status": "already checked in"})
        else:
            results.append({"attendee_id": attendee_id, "status": "not found"})

    db.commit()
    return {"results": results}


#Register Attendee: Allows users to register for an event, checking max_attendees.
@router.post("/attendees/", response_model=AttendeeResponse)
def register_attendee(attendee: AttendeeCreate, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.event_id == attendee.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    #Prevent registration if the max_attendees limit is reached.
    if event.max_attendees and len(db.query(Attendee).filter(Attendee.event_id == attendee.event_id).all()) >= event.max_attendees:
        raise HTTPException(status_code=400, detail="Max attendees limit reached")
    
    db_attendee = Attendee(**attendee.model_dump())
    try:
        db.add(db_attendee)
        db.commit()
        db.refresh(db_attendee)
        return db_attendee
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400,detail='Email already registered.')

#Check-in Attendee: Marks an attendee as checked in.
@router.put("/attendees/checkin/", response_model=AttendeeResponse)
def check_in_attendee(attendee: AttendeeCheckIn, db: Session = Depends(get_db)):
    db_attendee = db.query(Attendee).filter(Attendee.attendee_id == attendee.attendee_id).first()
    if not db_attendee:
        raise HTTPException(status_code=404, detail="Attendee not found")
    
    db_attendee.check_in_status = True
    db.commit()
    db.refresh(db_attendee)
    return db_attendee
