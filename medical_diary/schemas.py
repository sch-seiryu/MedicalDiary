from enum import Enum

from pydantic import BaseModel, Field

from datetime import date
from datetime import datetime as dt


# region Enumerations
class TimesOfDay(str, Enum):
    MORNING = "MORNING"
    NOON = "NOON"
    NIGHT = "NIGHT"
    DEMAND = "DEMAND"
    ELSE = "ELSE"


class AdministrationResults(str, Enum):
    DONE = "DONE"
    MISSED = "MISSED"
    SKIPPED = "SKIPPED"
# endregion


# region models for 'clinic'
class ClinicBase(BaseModel):
    specialties: str
    clinic_name: str


class ClinicCreate(ClinicBase):
    pass


class Clinic(ClinicBase):
    id: int

    class Config:
        orm_mode = True
# endregion


# region models for 'prescription'
class PrescriptionBase(BaseModel):
    clinic_id: int
    prescription_date: date
    number_of_days: int
    parent: int | None
    child: int | None
    note: str | None


class PrescriptionCreate(PrescriptionBase):
    pass


class Prescription(PrescriptionBase):
    id: int

    class Config:
        orm_mode = True
# endregion


# region models for 'administration'
# region (by tutorials) from the earlier version...
"""class AdministrationOld(BaseModel):
    prescription_id: int = Field(
        default=None, description="The ID of prescription in \'prescription'\ table. A positive integer.", ge=1) # ...
    datetime: str = ...
    # about the regex... r"^\d{4}-?d{1,2}-?d{1,2}\s*T?\d{1,2}:?\d{1,2}$"
    exact_time: bool = True
    time_of_day: TimesOfDay = ...
    pack_no: int | None  # ?
    message: str | None = None
    comment: str | None = None"""
# endregion


class AdministrationBase(BaseModel):
    prescription_id: int | None
    datetime: dt
    exact_time: bool
    # time_of_day: str | None  # TODO_DONE enum type
    # administration_result: str | None  # TODO_DONE enum type
    time_of_day: TimesOfDay | None
    administration_result: AdministrationResults | None
    pack_no: int | None
    message: str | None
    comment: str | None


class AdministrationCreate(AdministrationBase):
    pass


class Administration(AdministrationBase):
    id: int
    # db_timestamp: str | dt
    db_timestamp: dt

    class Config:
        orm_mode = True
# endregion