from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Content
from .schemas import ContentResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="PetCare API",
    description="API de conteúdos educativos e guias para novos tutores.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8081",
        "http://127.0.0.1:8081",
    ],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "API do PetCare funcionando!"}


@app.get("/conteudos", response_model=list[ContentResponse])
def listar_conteudos(
    categoria: str | None = None,
    db: Session = Depends(get_db),
):
    consulta = db.query(Content).filter(
        Content.content_type == "educativo"
    )

    if categoria:
        consulta = consulta.filter(
            Content.category.ilike(categoria)
        )

    return consulta.order_by(Content.title).all()


@app.get("/guias", response_model=list[ContentResponse])
def listar_guias(
    db: Session = Depends(get_db),
):
    return (
        db.query(Content)
        .filter(Content.content_type == "guia")
        .order_by(Content.title)
        .all()
    )


@app.get("/conteudos/{content_id}", response_model=ContentResponse)
def obter_conteudo(
    content_id: int,
    db: Session = Depends(get_db),
):
    conteudo = db.query(Content).filter(
        Content.id == content_id
    ).first()

    if conteudo is None:
        raise HTTPException(
            status_code=404,
            detail="Conteúdo não encontrado."
        )

    return conteudo


@app.get("/buscar", response_model=list[ContentResponse])
def buscar_conteudo(
    q: str = Query(min_length=2, max_length=100),
    db: Session = Depends(get_db),
):
    termo = f"%{q}%"

    return (
        db.query(Content)
        .filter(
            Content.title.ilike(termo)
            | Content.summary.ilike(termo)
            | Content.body.ilike(termo)
        )
        .order_by(Content.title)
        .all()
    )