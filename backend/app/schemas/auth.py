from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    email: str
    oauth_provider: str | None = None
    created_at: datetime
    last_login: datetime
    notification_enabled: bool
    notification_time: str

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_user(cls, user) -> "UserResponse":
        return cls(
            id=user.id,
            email=user.email,
            oauth_provider=user.oauth_provider,
            created_at=user.created_at,
            last_login=user.last_login,
            notification_enabled=user.notification_enabled,
            notification_time=user.notification_time.strftime("%H:%M") if user.notification_time else "08:00",
        )


class AuthResponse(BaseModel):
    user: UserResponse
    access_token: str


class TokenData(BaseModel):
    user_id: str
