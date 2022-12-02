# MedicalDiary
Medical diary application based on Python 3.10+, FastAPI, SQLAlchemy, PostgreSQL, to practice web framework, ORM, REST API, and so on. Of course, I'd use this app for my health care irl. 🥴

## Dependencies/Specifications
* Python 3.10.5 (Windows NT x64)
* FastAPI 0.87+ (implying minor documentation updates)
* PostgreSQL 14
* SQLAlchemy 1.4.44
### ... and additionally
* IDE: PyCharm Pro 2022.2.3
* Anaconda: conda 22.9.0 / conda-build 3.23.1 / conda-forge (for the integration of the environment, using 'pip' is avoided)

## Milestones
What I've found is...
* *FastAPI* is a micro/light-weight web framework like flask, and not to build a formal API nor for functional programming.
  * With HTTP, 'CRUD' operations can be handled via HTTP requests.
  * ASGI server is used for production.(*uvicorn* is the very example in tutorials)
  * Deeply based on *starlette*,
  * using *Pydantic* for validations of values
  * and SQLAlchemy as an ORM,
  * and OpenAPI is supported for (generating) documentations.
* I adopted to use *FastAPI* framework to get access to my personal medical record DB, that I created earlier to practice the DBMS.
* database/model/schema for FastAPI has been arranged from that of the tutorials to my DB, and building up APIs on the main/crud part.
* It is quite easy to use enumeration types, date&time and nested data types, not just simple values like numbers or string. 


## References
* https://github.com/tiangolo/fastapi
* https://fastapi.tiangolo.com/
  * (with my gratitude to those good examples and nice explanations 😘)