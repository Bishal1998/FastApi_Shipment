from sqlalchemy import create_engine
from sqlmodel import SQLModel


engine = create_engine(
    "sqlite:///shipments.db",
    echo=True,
    connect_args={"check_same_thread": False}
)

def create_db_and_tables():
    from .models import Shipment
    SQLModel.metadata.create_all(bind=engine)
