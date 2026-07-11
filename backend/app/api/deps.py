from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional

from app.core.config import settings
from app.db.session import get_db
from app.db.models import User, ApiKey
from app.schemas.user import TokenPayload
from app.core.security import ALGORITHM
import hashlib

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
        if token_data.sub is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    result = await db.execute(select(User).where(User.id == token_data.sub))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user

async def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user

async def verify_api_key(
    api_key: Optional[str] = Security(api_key_header),
    db: AsyncSession = Depends(get_db)
) -> ApiKey:
    if not api_key:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Missing API Key")
    
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    result = await db.execute(select(ApiKey).where(ApiKey.key_hash == key_hash))
    db_api_key = result.scalars().first()
    
    if not db_api_key:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API Key")
    return db_api_key
