from typing import Any
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()

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


@app.get("/shipment/{id}")
def get_shipment(id:int) -> dict[str, Any]:
    for shipment in shipments:
        if shipment["id"] == id:
            shipment_found =  shipment
        else:
            shipment_found = {"error": "Shipment not found"}
    return shipment_found

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