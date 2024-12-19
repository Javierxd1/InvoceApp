import pytest
from fastapi.testclient import TestClient #Nos permite hacer acciones HTTP
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session
from app.main import app
from db import getSession

#Se añade una base de datos de testeo
sqlite_name = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_name}"

engine = create_engine(sqlite_url,
                       connect_args={"check_same_thread":False},
                       poolclass = StaticPool)

@pytest.fixture(name='session')
def session_fixture():
    SQLModel.metadata.create_all(engine) #Crea las tablas 
    with Session(engine) as session: #Define una sesiòn
        yield session #Permite ejecutar las variables en el fixture
    SQLModel.metadata.drop_all(engine) #Elimina las tablas creadas en las pruebas.

@pytest.fixture(name='client')
def client_fixture(session: Session):
    def get_session_override():
        return session
    app.dependency_overrides[getSession] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

