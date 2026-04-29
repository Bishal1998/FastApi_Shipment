from fastapi.security import OAuth2PasswordBearer

oauth2_seller = OAuth2PasswordBearer(tokenUrl="seller/login")
oauth2_delivery_partner = OAuth2PasswordBearer(tokenUrl="partner/login")
