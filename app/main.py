from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import Any

from fastapi import FastAPI, HTTPException
from scalar_fastapi import get_scalar_api_reference

from app.database.models import Shipment

from .database.session import SessionDep, create_db_and_tables
from .schemas import CreateShipment, ReadShipment, ShipmentStatus, UpdateShipment


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
   create_db_and_tables()
   yield

app = FastAPI(lifespan=lifespan_handler)

shipments = [
    {
        "id": 10270,
        "weight": 15,
        "content": "Glass",
        "status": "Placed"
    },
    {
        "id": 10271,
        "weight": 20,
        "content": "Electronics",
        "status": "In Transit"
    },
    {
        "id": 10272,
        "weight": 8.5,
        "content": "Documents",
        "status": "Delivered"
    },
    {
        "id": 10273,
        "weight": 12,
        "content": "Clothing",
        "status": "Placed"
    },
    {
        "id": 10274,
        "weight": 25.5,
        "content": "Furniture",
        "status": "In Transit"
    },
    {
        "id": 10275,
        "weight": 5,
        "content": "Toys",
        "status": "Delivered"
    }
]

@app.get("/shipment/latest")
def get_latest_shipment() -> dict[str, Any]:
    latest = shipments[-1]
    return latest

@app.get("/shipment/{id}", response_model=ReadShipment)
def get_shipment_by_id(id : int, session : SessionDep) :
    shipment = session.get(Shipment, id)

    if not shipment:
        raise HTTPException(status_code=404, detail=f"Shipment with id {id} not found")

    return shipment 

@app.post("/shipment", response_model= ReadShipment)
def create_shipment(data : CreateShipment, session : SessionDep):

    new_shipment = Shipment(
        **data.model_dump(),
        status = ShipmentStatus.PLACED,
        estimated_delivery = datetime.now() + timedelta(days=7)
    )
    
    session.add(new_shipment)
    session.commit()
    session.refresh(new_shipment)

    return new_shipment

@app.patch("/shipment/{id}", response_model=ReadShipment)
def patch_update_shipment(id : int, data: UpdateShipment, session: SessionDep):

    shipment = session.get(Shipment, id)

    if not shipment:
        raise HTTPException(status_code=404, detail=f"Shipment with id {id} not found")
    shipment.sqlmodel_update(data.model_dump(exclude_none=True))
    session.add(shipment)
    session.commit()
    session.refresh(shipment)
    return shipment 

@app.delete("/shipment/{id}")
def delete_shipment(id : int, session: SessionDep) -> dict[str, Any]:
    shipment = session.get(Shipment, id)

    if not shipment:
        raise HTTPException(status_code=404, detail=f"Shipment with id {id} not found")

    session.delete(shipment)
    session.commit()

    return {"message": f"Shipment with id {id} deleted successfully"}

@app.get("/")
def get_root():
    return {"message": "Hello, World!"}

@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
        #  this here
        servers=[
            {
                "url": "http://localhost:8000",
                "description": "Local server",
            },
        ]
    )