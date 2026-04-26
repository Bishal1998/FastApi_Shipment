from fastapi import APIRouter

from app.api.dependencies import SellerServiceDep
from app.api.schemas.seller import CreateSeller, ReadSeller

router = APIRouter(
    prefix="/seller",
    tags=["Seller"],
)


@router.post("/signup", response_model=ReadSeller)
async def signup(data: CreateSeller, service: SellerServiceDep):
    return await service.add(data)
