from typing import Optional, List
from sqlmodel import Field, Relationship, SQLModel
from shared.auth.models.user import UserDB

class DiaryUserLink(SQLModel, table=True):
    diary_id: int = Field(foreign_key="diarydb.id", primary_key=True)
    user_id: int = Field(foreign_key="userdb.id", primary_key=True)

class DiaryDB(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True) 
    title: str
    messages_history: Optional[str] = None
    owners: List[UserDB] = Relationship(back_populates="diaries", link_model=DiaryUserLink)

UserDB.model_rebuild()
UserDB.diaries: List[DiaryDB] = Relationship(back_populates="owners", link_model=DiaryUserLink)