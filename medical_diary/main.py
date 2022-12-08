from fastapi import Depends, FastAPI, HTTPException, status
# from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

# from . import crud, models, schemas
# from .database import SessionLocal, engine
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Default message
@app.get("/")
async def root():
    return {"message": "Hello World. This is medical diary test server."}


# region Administration Records
@app.post("/administrations/", response_model=schemas.Administration)
def create_administration_records(record: schemas.AdministrationCreate, db: Session = Depends(get_db)):
    # 'record' is a body parameter

    # region check up the data by unique time of a day(=for when)
    db_administration = crud.get_administration_record_by_when(
        db, date_string=record.datetime[:10],
        time_of_day=record.time_of_day)

    if db_administration:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Matching record already exists.")
    # endregion

    # region check up the data by unique medicine package number(=which one)
    db_administration = crud.get_administration_record_by_which(
        db, prescription_id=record.prescription_id,
        pack_no=record.pack_no)

    if db_administration:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The medicine has been taken already.")
    # endregion

    return crud.create_administration_record(db=db, administration_record=record)

    # TODO Legacy codes... what do I have to do with 'OID' data? (marked@221130_1112)
    # #
    # # DB processing...
    # #
    # OID = 0
    #
    # return {"OID": OID}  # TODO return result of DB processing(consider calling 'RETURNING *;' in SQL)


@app.get("/administrations/", response_model=list[schemas.Administration])
def read_administration_record(
        skip: int = 0, limit: int = 120,  # Query parameters
        db: Session = Depends(get_db)):
    records = crud.get_administration_records(db, skip=skip, limit=limit)
    return records


@app.get("/administrations/{date_string}", response_model=list[schemas.Administration])
def read_administration_records_by_when(
        date_string: str,
        tod: schemas.TimesOfDay | None = None, # query
        db: Session = Depends(get_db)):
    db_record = crud.get_administration_record_by_when(db, date_string=date_string, time_of_day=tod)
    # print(db_record)

    if db_record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found.")
    return db_record
# endregion


# region Prescription
@app.post("/prescriptions/", response_model=schemas.Prescription)
def create_prescription(
        prescription: schemas.PrescriptionCreate, db: Session = Depends(get_db)):
    # 'prescription' is a body parameter.

    # region check given date and clinic pair already exists.
    # TODO deal with the date string part.(needs more consideration)
    db_prescription = crud.get_prescriptions_by_clinic_and_when(
        db, clinic=prescription.clinic_id, date_string=prescription.prescription_date.strftime("%Y-%m-%d"))
    if db_prescription is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A prescription already exists on the given clinic and date.")
    # endregion

    return crud.create_prescription(db=db, prescription=prescription)

@app.get("/prescriptions/", response_model=list[schemas.Prescription])
def read_prescriptions(
        # prescription: int | None, clinic: int | None, date_string: str | None,  # Query parameters
        prescription: int | None = None, clinic: int | None = None, date_string: str | None = None,  # Query parameters
        db: Session = Depends(get_db)):

    # region check at least one parameter is given to search prescriptions;
    # ... but obviously, it would return all the records nothing is given, so the code below is not necessary.
    # if prescription is None and clinic is None and date_string is None:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No parameter to find prescription(s).")
    # endregion

    # TODO what about else? (filtered by clinic(id) and date) - Possibly done
    if prescription is not None:
        db_prescription = crud.get_prescription(db, prescription_id=prescription)
    else:
        db_prescription = crud.get_prescriptions_by_clinic_and_when(db, clinic=clinic, date_string=date_string)

    if db_prescription is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prescription not found.")
    return db_prescription
# endregion


# region Drug
# endregion


# region Clinic
# endregion
