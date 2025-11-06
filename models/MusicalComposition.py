from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Optional

# Modelo da tabela
class MusicalComposition(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    title: str = Field(index=True)
    author: str = Field(index=True)
    content: str = Field(description="Cifra musical com acordes no formato .C@")
    lyrics: Optional[str] = Field(default=None, description="Letra limpa sem acordes")
    chords_line: Optional[str] = Field(default=None, description="Linha de acordes formatada")
    complete_musical_notation: Optional[str] = Field(default=None, description="Cifra completa formatada")

# Modelo para INPUT (criar composição)
class MusicalCompositionCreate(SQLModel):
    title: str
    author: str
    content: str
    # SEM id e created_at - não permite enviar

# Modelo para OUTPUT (resposta da API)  
class MusicalCompositionRead(SQLModel):
    id: int  # Sempre presente na resposta
    title: str
    author: str
    content: str
    lyrics: Optional[str] = None
    chords_line: Optional[str] = None
    complete_musical_notation: Optional[str] = None
    created_at: datetime