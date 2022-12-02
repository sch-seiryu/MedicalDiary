from fastapi import Depends, FastAPI, HTTPException
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
def create_administration_record(record: schemas.AdministrationCreate, db: Session = Depends(get_db)):
    # 'record' is a body parameter

    # region check up the data by unique time of a day(=for when)
    db_administration = crud.get_administration_record_by_when(
        db, date_string=record.datetime[:10],
        time_of_day=record.time_of_day)

    if db_administration:
        raise HTTPException(status_code=400, detail="Matching record already exists.")
    # endregion

    # region check up the data by unique medicine package number(=which one)
    db_administration = crud.get_administration_record_by_which(
        db, prescription_id=record.prescription_id,
        pack_no=record.pack_no)

    if db_administration:
        raise HTTPException(status_code=400, detail="The medicine has been taken already.")
    # endregion

    return crud.create_administration_record(db=db, administration_record=record)

    # TODO Legacy codes... what do I have to do with 'OID' data? (marked@221130_1112)
    # #
    # # TODO DB processing...
    # #
    # OID = 0
    #
    # return {"OID": OID}  # TODO return result of DB processing(consider calling 'RETURNING *;' in SQL)


@app.get("/administrations/", response_model=list[schemas.Administration])
def read_administration_record(skip: int = 0, limit: int = 120, db: Session = Depends(get_db)):
    records = crud.get_administration_records(db, skip=skip, limit=limit)
    return records


@app.get("/administrations/{date_string}", response_model=list[schemas.Administration])
def read_administration_records_by_when(
        date_string: str,
        tod: schemas.TimesOfDay | None = None, # query
        db: Session = Depends(get_db)):
    db_record = crud.get_administration_record_by_when(db, date_string=date_string, time_of_day=tod)
    print(db_record)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found.")
    return db_record
# endregion


