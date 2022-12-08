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
class AdministrationBase(BaseModel):
    prescription_id: int | None
    # TODO prescription: int = Field(
    #         default=None, description="The ID of prescription in \'prescription'\ table. A positive integer.", ge=1) # ...
    datetime: dt
    # TODO about the regex... r"^\d{4}-?d{1,2}-?d{1,2}\s*T?\d{1,2}:?\d{1,2}$"
    exact_time: bool
    time_of_day: TimesOfDay | None
    administration_result: AdministrationResults | None
    pack_no: int | None
    message: str | None
    comment: str | None


class AdministrationCreate(AdministrationBase):
    pass


class Administration(AdministrationBase):
    id: int
    db_timestamp: dt

    class Config:
        orm_mode = True
        schema_extra = {  # TODO what about 'id' and 'db_timestamp', which are allocated after DB transaction? (cont.)
            # TODO (cont.) REFERENCE: https://fastapi.tiangolo.com/ko/tutorial/schema-extra-example/#pydantic-schema_extra
            "administration_record": {
                "": ""
            }
        }
# endregion