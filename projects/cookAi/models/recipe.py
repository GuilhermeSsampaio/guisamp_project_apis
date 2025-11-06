from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from pydantic import BaseModel

if TYPE_CHECKING:
    from shared.auth.models.user import UserDB

class Recipe(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    title: Optional[str] = None
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    owner: Optional["UserDB"] = Relationship(back_populates="recipes")

# Modelos para API
class RecipeCreate(BaseModel):
    content: str
    title: Optional[str] = None

class RecipeRead(BaseModel):
    id: int
    content: str
    title: Optional[str] = None
    created_at: datetime
    owner_id: Optional[int] = None