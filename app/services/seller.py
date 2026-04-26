from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.seller import CreateSeller
from app.database.models import Seller

import bcrypt

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
