from pydantic import BaseModel, EmailStr
from typing import Optional, List

# ---------------------------------------
# ✅ User Schemas
# ---------------------------------------
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    archetype_id: int
    tier_id: int


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    archetype_id: int
    tier_id: int

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ---------------------------------------
# ✅ Token Schemas
# ---------------------------------------
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    sub: Optional[str] = None


# ---------------------------------------
# ✅ Archetype & Tier Schemas
# ---------------------------------------
class ArchetypeResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True


class TierResponse(BaseModel):
    id: int
    name: str
    level: int
    description: str

    class Config:
        orm_mode = True


# ---------------------------------------
# ✅ Coalition Schemas (creator_id removed)
# ---------------------------------------
class CoalitionBase(BaseModel):
    name: str
    description: Optional[str] = None
    focus: Optional[str] = None
    location: Optional[str] = None


class CoalitionCreate(CoalitionBase):
    pass  # no creator_id anymore


class CoalitionMember(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class CoalitionsOut(CoalitionBase):
    id: int
    members: List[CoalitionMember] = []

    class Config:
        orm_mode = True


# ---------------------------------------
# ✅ Collab Circle Schemas
# ---------------------------------------
class CollabCreate(BaseModel):
    user_a_username: str
    user_b_username: str
    project_name: Optional[str] = None


class CollabResponse(BaseModel):
    collaborator_username: str
    project_name: Optional[str]
    status: str
    verified_at: Optional[str] = None

    class Config:
        orm_mode = True










