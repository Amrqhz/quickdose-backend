# schemas.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str
    plan_type: str 
    duration_months: int = 1

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class SubscriptionBase(BaseModel):
    plan_type: str
    end_date: datetime

class SubscriptionCreate(SubscriptionBase):
    pass

class Subscription(SubscriptionBase):
    id: int
    user_id: int
    start_date: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    subscriptions: List[Subscription] = []
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None