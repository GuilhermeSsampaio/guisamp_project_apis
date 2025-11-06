from datetime import datetime
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from sqlmodel import select
from shared.db.config_db import SessionDep
from ..utils.padroes import encontrar_acordes, limpar_letra, montar_cifra
from ..models.MusicalComposition import MusicalComposition, MusicalCompositionCreate, MusicalCompositionRead

router = APIRouter(prefix="/musical_compositions")

# READ - listar todas
@router.get("/list", response_model=list[MusicalComposition])
def get_musical_compositions(session: SessionDep):
    """Lista as composições musicais cadastradas"""
    musical_compositions = session.exec(select(MusicalComposition)).all()
    return musical_compositions
    
@router.post("/create_music", response_model=MusicalCompositionRead)
def create_musical_composition(music_composition_data: MusicalCompositionCreate, session: SessionDep):
    acordes_lista = encontrar_acordes(music_composition_data.content)
    acordes_string = ", ".join(acordes_lista)  # ← Converter lista para string
    
    new_musical_composition = MusicalComposition(
        title=music_composition_data.title,
        author=music_composition_data.author,
        content=music_composition_data.content,
        lyrics=limpar_letra(music_composition_data.content),
        chords_line=acordes_string,  # ← String em vez de lista
        complete_musical_notation=montar_cifra(music_composition_data.content)
    )
    session.add(new_musical_composition)
    session.commit()
    session.refresh(new_musical_composition)
    return new_musical_composition

@router.get("/view/{composition_id}", response_class=HTMLResponse)
def view_composition(composition_id: int, session: SessionDep):
    """Visualizar cifra formatada como página HTML"""
    composition = session.get(MusicalComposition, composition_id)
    if not composition:
        raise HTTPException(status_code=404, detail="Composição não encontrada")
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{composition.title} - {composition.author}</title>
        <style>
            body {{ font-family: 'Courier New', monospace; padding: 20px; }}
            .cifra {{ 
                white-space: pre; 
                background: #f5f5f5; 
                padding: 15px; 
                border-radius: 5px;
                line-height: 1.5;
            }}
            .title {{ color: #333; margin-bottom: 10px; }}
        </style>
    </head>
    <body>
        <h1 class="title">{composition.title}</h1>
        <h3>Por: {composition.author}</h3>
        <div class="cifra">{composition.complete_musical_notation}</div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

