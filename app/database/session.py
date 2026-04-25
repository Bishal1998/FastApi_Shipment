from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel

engine = create_engine(
    "sqlite:///shipments.db",
    echo=True,
    connect_args={"check_same_thread": False}
)

def create_db_and_tables():
    from .models import Shipment
    SQLModel.metadata.create_all(bind=engine)

def get_session():
    with Session(bind=engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]