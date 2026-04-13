from typing import Optional

from pydantic import BaseModel, EmailStr


class ContactCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None


class ContactResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None

    model_config = {"from_attributes": True}
