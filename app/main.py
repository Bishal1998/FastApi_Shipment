from typing import Any
from fastapi import FastAPI, status, HTTPException
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
    shipment = next((s for s in shipments if s["id"] == id), None)

    if not shipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Shipment with id {id} not found")
    return shipment

@app.post("/shipment")
def create_shipment(data : dict) -> dict[str, Any]:

    weight = data["weight"]
    content = data["content"]

    if weight > 25:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Maximum allowed weight is 25 kg.")

    new_id = shipments[-1]["id"] + 1

    shipments.append({
        "id": new_id,
        "weight": weight,
        "content": content,
        "status": "Placed"
    })

    return {"id": new_id, "message": "Shipment created successfully"}

@app.put("/shipment/{id}")
def update_shipment(id :int, weight : float, content: str, status: str) -> dict[str, Any]:
    shipment = next((s for s in shipments if s["id"] == id), None)

    if not shipment:
        raise HTTPException(status_code=404, detail=f"Shipment with id {id} not found")

    if weight > 25:
        raise HTTPException(status_code=406, detail="Maximum allowed weight is 25 kg.")

    shipment["weight"] = weight
    shipment["content"] = content
    shipment["status"] = status

    return {"message": f"Shipment with id {id} updated successfully"}

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