from .database import Base, engine, SessionLocal
from .models import Content

Base.metadata.create_all(bind=engine)

conteudos = [
    {
        "title": "Alimentação dos animais",
        "category": "Alimentação",
        "content_type": "educativo",
        "summary": "Conheça a importância de uma alimentação adequada.",
        "body": (
            "As necessidades nutricionais variam conforme a espécie, "
            "idade e condição do animal. Utilize alimentos apropriados "
            "e procure orientação veterinária para definir a dieta."
        ),
    },
    {
        "title": "Higiene e cuidados básicos",
        "category": "Higiene",
        "content_type": "educativo",
        "summary": "Entenda os cuidados de higiene na rotina do pet.",
        "body": (
            "Mantenha os recipientes de água e alimento limpos, "
            "observe a higiene do ambiente e adapte os cuidados "
            "às necessidades de cada animal."
        ),
    },
    {
        "title": "Primeiros passos para novos tutores",
        "category": "Primeiros cuidados",
        "content_type": "guia",
        "summary": "Orientações para quem está começando a cuidar de um pet.",
        "body": (
            "Prepare um ambiente seguro, disponibilize água limpa, "
            "ofereça alimentação apropriada e organize uma avaliação "
            "com um médico-veterinário para receber orientações "
            "sobre vacinação, prevenção e cuidados individuais."
        ),
    },
    {
        "title": "Preparando a casa para receber um animal",
        "category": "Adaptação",
        "content_type": "guia",
        "summary": "Como preparar um ambiente seguro e acolhedor.",
        "body": (
            "Organize um espaço tranquilo, retire objetos perigosos "
            "do alcance do animal e disponibilize local de descanso, "
            "água e alimentação. Faça a adaptação gradualmente."
        ),
    },
]


def inserir_conteudos():
    with SessionLocal() as db:
        for item in conteudos:
            existente = db.query(Content).filter(
                Content.title == item["title"]
            ).first()

            if existente is None:
                db.add(Content(**item))

        db.commit()

    print("Conteúdos iniciais verificados com sucesso.")


if __name__ == "__main__":
    inserir_conteudos()