from sqlalchemy.orm import Session
from sqlalchemy import Date, cast

# IMPORTED by 'schemas.py'
from datetime import date

# from . import models, schemas
# from medical_diary import models, schemas
import models, schemas

# region 'Clinic'
def get_clinic(db: Session, clinic_id: int):
    return db.query(
        models.Clinic).filter(models.Clinic.id == clinic_id)


def create_clinic(db: Session, clinic: schemas.ClinicCreate):
    # create a SQLALchemy 'model' instance with given data
    db_clinic = models.Clinic(**clinic.dict())
    # 'add' the instance object to the db session
    db.add(db_clinic)
    # 'commit' the changes to the db(=saving)
    db.commit()
    # 'refresh' the instance, so that it contains any new data from db, like a generated ID.
    db.refresh(db_clinic)
    return db_clinic
# endregion


# region 'Prescription'
def get_prescription(db: Session, prescription_id: int):
    return db.query(
        models.Prescription).filter(models.Prescription.id == prescription_id)


def get_prescriptions_by_clinic_and_when(db: Session, clinic:int | None, date_string: str | None):
    db_prescription = db.query(models.Prescription)

    # filter by clinic(clinic_id)
    if clinic is not None:
        db_prescription = db_prescription.filter(models.Prescription.clinic_id == clinic)

    # filter by date
    if date_string is not None:
        # TODO parse date(date string) properly
        the_date = date(*list(map(int, date_string.split('-'))))

        db_prescription = db_prescription.filter(
            models.Prescription.prescription_date == the_date)  # Matching: 'date'

    # return all the rows filtered by given conditions
    return db_prescription.all()


def create_prescription(db: Session, prescription: schemas.PrescriptionCreate):
    # create a SQLALchemy 'model' instance with given data
    db_prescription = models.Prescription(
        clinic_id=prescription.clinic_id,
        prescription_date=prescription.prescription_date,
        number_of_days=prescription.number_of_days,
        parent=prescription.parent,
        child=prescription.child,
        note=prescription.note,
    )
    # 'add' the instance object to the db session
    db.add(db_prescription)
    # 'commit' the changes to the db(=saving)
    db.commit()
    # 'refresh' the instance, so that it contains any new data from db, like a generated ID.
    db.refresh(db_prescription)
    return db_prescription
# endregion


# region 'Administration'
def get_administration_record(db: Session, administration_record_id: int):
    return db.query(
        models.Administration).filter(
        models.Administration.id == administration_record_id).first()


def get_administration_records(db: Session, skip: int = 0, limit: int = 120):
    return db.query(
        models.Administration).offset(skip).limit(limit).all()  # TODO wait, 'fetch' is unavailable?


# def get_administration_record_by_when(db: Session, date_string: str, time_of_day_string: str):
def get_administration_record_by_when(db: Session, date_string: str, time_of_day: schemas.TimesOfDay | None):
    # TODO What is proper way to deal with 'date & time' type and 'enumeration' type? - and is this okay with enum now?

    # TODO protect this part from parsing error -> but... isn't it for pydantic or else? @2022-12-02_1007
    # parse 'date_string' to 'datetime.date' instance
    the_date = date(*list(map(int, date_string.split('-'))))

    temp = db.query(models.Administration
             # ).filter(models.Administration.prescription == prescription  # Matching: 'prescription'
             ).filter(cast(models.Administration.datetime, Date) == the_date)  # Matching: 'datetime'

    # print(date_string, temp, models.Administration.datetime)
    if time_of_day is None:
        return temp.all()
    return temp.filter(models.Administration.time_of_day == time_of_day).all()  # Matching: 'time_of_day'


def get_administration_record_by_which(db: Session, prescription_id: int, pack_no: int):
    return db.query(models.Administration
        ).filter(models.Administration.prescription_id == prescription_id
        ).filter(models.Administration.pack_no == pack_no)


def create_administration_record(db: Session, administration_record: schemas.AdministrationCreate):
    # create a SQLALchemy 'model' instance with given data
    db_administration_record = models.Administration(
        prescription_id=administration_record.prescription_id,
        datetime=administration_record.datetime,
        exact_time=administration_record.exact_time,
        time_of_day=administration_record.time_of_day,
        pack_no=administration_record.pack_no,
        message=administration_record.message,
        comment=administration_record.comment,
    )
    # 'add' the instance object to the db session
    db.add(db_administration_record)
    # 'commit' the changes to the db(=saving)
    db.commit()
    db.refresh(db_administration_record)
    # 'refresh' the instance, so that it contains any new data from db, like a generated ID.
    return db_administration_record
# endregion
