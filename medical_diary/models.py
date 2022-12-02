from sqlalchemy import BOOLEAN, Column, ForeignKey, Integer, String, Date, DateTime, Enum, MetaData
from sqlalchemy.orm import relationship

# from .database import Base, engine
# from medical_diary.database import Base, engine
from database import Base, engine


# Enumerated types and binding it with engine using metadata.
__meta_data__ = MetaData(bind=engine)
times_of_day = Enum("MORNING", "NOON", "NIGHT", "ELSE", name="times_of_day", metadata=__meta_data__)
administration_results = Enum("DONE", "SKIPPED", "MISSED", name="administration_results", metadata=__meta_data__)


class Clinic(Base):
    __tablename__ = "clinic"

    id = Column(Integer, primary_key=True, index=True)
    specialties = Column(String,)
    clinic_name = Column(String,)

    prescription = relationship("Prescription", back_populates="clinic")    # 1:M
    # <NOTE: 'models.py'에서 아래 부분을 이용해 연결하려고 하니, parent/child table 간의 관계가 문제시 되는거 같았다.
    # 이게 직접적인 관계가 있지 않아서인지, 아니면 '__tablename__'과의 연관성 때문에 복수형에 's'를 붙여서 name space에 문제가
    # 있었던건지, 또 아니면 이런 식의 쌍방은 허용하지 않아서인지는 잘 모르겠지만
    # (연결 고리는 'Prescription'이지만 순서상으론 'Clinic'이 최상위라고 할 수 있다) 아무튼 여기 뿐만 아니라
    # 'Administration' 쪽도 함께 끊어주니 정상적으로 동작을 수행했다.
    # </NOTE DONE@2022-12-02_1035>
    # administration = relationship("Administration", back_populates="clinic")    # 1:M


class Prescription(Base):
    __tablename__ = "prescription"

    id = Column(Integer, primary_key=True, index=True)
    clinic_id = Column(Integer, ForeignKey("clinic.id"))
    prescription_date = Column(Date,)  # TODO datetime format usage in SQLAlchemy
    number_of_days = Column(Integer)
    parent = Column(Integer)  # | None,)  # TODO nullable
    child = Column(Integer)  # | None,)  # TODO nullable
    note = Column(String)  # | None,)  # TODO nullable

    clinic = relationship("Clinic", back_populates="prescription")  # 1:1
    administration = relationship("Administration", back_populates="prescription")  # 1:M


class Administration(Base):
    __tablename__ = "administration"

    id = Column(Integer, primary_key=True, index=True)
    prescription_id = Column(Integer, ForeignKey("prescription.id"))  # TODO nullable
    datetime = Column(DateTime,)
    exact_time = Column(BOOLEAN, default=True)
    time_of_day = Column('time_of_day', times_of_day)  # , metadata=__meta_data__)  # TODO place 'None' where?
    administration_result = Column('administration_result', administration_results)  # , metadata=__meta_data__)  # TODO place 'None' where?
    pack_no = Column(Integer)  # | None,)  # TODO nullable
    message = Column(String)  # | None,)  # TODO nullable
    comment = Column(String)  # | None,)  # TODO nullable
    db_timestamp = Column(String)  # Column(DateTime,)

    # 2 below relationships are defined in composite. - 복합키처럼 두 가지 모두 정해야 하나를 지칭함.  TODO 내용을 재정비할 필요성 있음.
    prescription = relationship("Prescription", back_populates="administration")  # '1:1'(not unique)
    # clinic = relationship("Clinic", back_populates="administration")  # '1:1'(not unique)
