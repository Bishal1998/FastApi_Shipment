
import bcrypt
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.api.schemas.seller import CreateSeller
from app.database.models import Seller

import jwt

from datetime import datetime, timedelta

from app.config import jwt_settings

# # Verify password
# bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password)


class SellerService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, data: CreateSeller) -> Seller:

        new_seller = Seller(
            **data.model_dump(exclude={"password"}),
            hashed_password=bcrypt.hashpw(
                data.password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8"),
        )

        self.session.add(new_seller)
        await self.session.commit()
        await self.session.refresh(new_seller)
        return new_seller

    async def login(self, email : str, password : str) -> str:
        
        result = await self.session.execute(
            select(Seller).where(Seller.email == email)
        )
        seller = result.scalar()

        if seller is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Seller with email: {email} not found") 
        
        password_matched = bcrypt.checkpw(password.encode("utf-8"), seller.hashed_password.encode("utf-8"))

        if not password_matched:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Incorrect password")
        
        token = jwt.encode(
            payload = {
                "user" : {
                    "id" : seller.id,
                    "email" : seller.email
                },
                "exp": datetime.now() + timedelta(hours=1),
            },
            algorithm=jwt_settings.JWT_ALGORITHM,
            key = jwt_settings.JWT_SECRET_KEY
        )

        return token
        

