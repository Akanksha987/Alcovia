from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import auth
from app.deps import get_db
from app.models import User
from app.schemas import Token, UserCreate, UserOut, UserLogin
from app.utils.jwt_handler import create_access_token
from app.utils.security import get_password_hash

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(payload: UserCreate, session: AsyncSession = Depends(get_db)) -> User:
    existing_user = await auth.get_user_by_email(session, payload.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user = User(email=payload.email, hashed_password=get_password_hash(payload.password))
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@router.post("/login", response_model=Token)
async def login(payload: UserLogin, session: AsyncSession = Depends(get_db)) -> Token:
    user = await auth.authenticate_user(session, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    token = create_access_token({"sub": user.email})
    return Token(access_token=token)

