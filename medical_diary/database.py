from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# separate db auth key from the project
try:
    from credentials.credential import db_key
except ImportError:
    db_key = "user:password"  # A default value
# print(db_key)


DATABASE_TYPE = "PostgreSQL"
SQLALCHEMY_DATABASE_URL = f"postgresql://{db_key}@localhost/medication"  # TODO Credential/Security/Authentication

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,  # connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
