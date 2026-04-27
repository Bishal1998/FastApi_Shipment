from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import SellerServiceDep
from app.api.schemas.seller import CreateSeller, ReadSeller
from app.core.security import oauth2_bearer
from app.utils import decode_access_token

router = APIRouter(
    prefix="/seller",
    tags=["Seller"],
)


@router.post("/signup", response_model=ReadSeller)
async def signup(data: CreateSeller, service: SellerServiceDep):
    return await service.add(data)


@router.post("/login")
async def login(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: SellerServiceDep,
):
    token = await service.login(request_form.username, request_form.password)
    return {"access_token": token, "type": "jwt"}


@router.get("/me")
async def me(token: Annotated[str, Depends(oauth2_bearer)]):
    data = decode_access_token(token)

    if data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    return {"detail": "Successfully Authenticated"}
