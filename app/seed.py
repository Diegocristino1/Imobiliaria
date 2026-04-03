import json
from pathlib import Path

from app import db
from app.models import Imovel

_VILA_SLUG = "casa-vila-de-fatima-planaltina"
_IMG_EXT = {".png", ".jpg", ".jpeg", ".webp"}


def _vila_fatima_sort_key(filename: str) -> tuple:
    stem = Path(filename).stem
    if stem.isdigit():
        return (0, int(stem))
    return (1, stem.lower())


def sync_vila_fatima_imagens_from_static(row: dict, static_root: Path) -> dict:
    """Se existir imagem na pasta da Vila de Fátima, atualiza principal + galeria no banco."""
    folder = static_root / "img" / "imoveis" / "vila-de-fatima"
    if not folder.is_dir():
        return row
    files = sorted(
        (f for f in folder.iterdir() if f.is_file() and f.suffix.lower() in _IMG_EXT),
        key=lambda p: _vila_fatima_sort_key(p.name),
    )
    if not files:
        return row
    rels = [f"img/imoveis/vila-de-fatima/{f.name}" for f in files]
    principal_rel = None
    for cand in ("08.png", "08.jpg", "08.jpeg", "08.webp"):
        if (folder / cand).is_file():
            principal_rel = f"img/imoveis/vila-de-fatima/{cand}"
            break
    if principal_rel is None and len(rels) >= 8:
        principal_rel = rels[7]
    elif principal_rel is None:
        principal_rel = rels[0]
    return {**row, "imagem_principal": principal_rel, "imagens_json": json.dumps(rels)}


def ensure_sample_data() -> None:
    # Se o banco já tiver dados com imagens antigas (Unsplash), substitui pelo catálogo real.
    # Assim você não precisa apagar manualmente `instance/imoveis.db`.
    if Imovel.query.first():
        tem_unsplash = Imovel.query.filter(Imovel.imagem_principal.like("https://images.unsplash.com/%")).first()
        if tem_unsplash:
            Imovel.query.delete()
            db.session.commit()

    descricao_buritis_iv = (
        "Uma casa na quadra 21-A Do Buritis IV. Em frente uma área verde arborizada.\n\n"
        "Contém\n"
        "* Área de frente\n"
        "* Sala mais cozinha americana.\n"
        "* Três quartos\n"
        "* Um banheiro\n"
        "* Área de serviço de fundo coberta\n"
        "* Um corredor na lateral.\n\n"
        "Documentação: Escritura a lavrar\n"
        "Valor: R$ 300.000,00"
    )

    descricao_vila_buritis = (
        "Essa casa fica localizada na quadra 02 da Vila Buritis.\n\n"
        "Contém:\n"
        "* 01 Sala ampla\n"
        "* 02 Banheiros, um com suíte.\n"
        "* 03 Quartos\n"
        "* Cozinha gourmet\n"
        "* Lote vazado todo construído\n"
        "* Espaço para mais construção na parte superior.\n\n"
        "Escritura ok\n\n"
        "Investimento: R$ 680.000,00"
    )

    descricao_chacara = (
        "Vendo uma chácara na área rural de Planaltina DF.\n"
        "Às margens da DF-230 próximo à casa da uva.\n"
        "Terreno todo cercado com duas nascentes com água em abundância.\n\n"
        "Metragem: 06 Hectares\n"
        "Documentada.\n\n"
        "Investimento: 650.000 mil Reais.\n\n"
        "Faça um agendamento com seu corretor.\n"
        "Valdemir Pereira"
    )

    descricao_arapoanga = (
        "Esse Lote de 900m² no Arapoanga é uma avenida comercial.\n\n"
        "Contém:\n"
        "* Três lojas\n"
        "* Estrutura para três pavimentos acima"
    )

    descricao_vila_fatima = (
        "Valdemir Pereira vende:\n"
        "Uma casa na Vila de Fátima com um pavimento acima.\n\n"
        "Na parte superior:\n"
        "02 duas kitnets com um quarto, sala e cozinha mais banheiro.\n\n"
        "Parte de baixo:\n"
        "• Garagem para dois veículos\n"
        "• Sala\n"
        "• 03 Quartos\n"
        "• Cozinha\n"
        "• Banheiro social\n"
        "• Área de serviço com um banheiro.\n\n"
        "Localização:\n"
        "• Próximo à UnB, Potiguar\n"
        "• Atacadão mercado.\n\n"
        "Documentação:\n"
        "Cessão de direito\n"
        "Aguardando escritura.\n\n"
        "Investimento:\n"
        "360.000 Mil\n\n"
        "Para maiores informações fale com seu Corretor.\n"
        "Valdemir Pereira\n"
        "Creci 32849"
    )

    amostras = [
        {
            "slug": "casa-buritis-iv-quadra-21a",
            "titulo": "Casa — Buritis IV (Quadra 21-A)",
            "descricao": descricao_buritis_iv,
            "preco": 300000.0,
            "tipo": "casa",
            "area_m2": 0.0,
            "quartos": 3,
            "banheiros": 1,
            "vagas": 0,
            "bairro": "Buritis IV",
            "cidade": "Planaltina",
            "estado": "DF",
            "endereco": "Quadra 21-A, Buritis IV",
            "destaque": True,
            "imagem_principal": "img/imoveis/buritis-iv/frente-1.png",
            "imagens_json": json.dumps(
                [
                    "img/imoveis/buritis-iv/frente-1.png",
                    "img/imoveis/buritis-iv/frente-2.png",
                    "img/imoveis/buritis-iv/cozinha.png",
                    "img/imoveis/buritis-iv/banheiro.png",
                ]
            ),
        },
        {
            "slug": "casa-vila-buritis-quadra-02",
            "titulo": "Casa — Vila Buritis (Quadra 02)",
            "descricao": descricao_vila_buritis,
            "preco": 680000.0,
            "tipo": "casa",
            "area_m2": 0.0,
            "quartos": 3,
            "banheiros": 2,
            "vagas": 0,
            "bairro": "Vila Buritis",
            "cidade": "Planaltina",
            "estado": "DF",
            "endereco": "Quadra 02, Vila Buritis",
            "destaque": True,
            "imagem_principal": "img/imoveis/vila-buritis-q02/sala.png",
            "imagens_json": json.dumps(
                [
                    "img/imoveis/vila-buritis-q02/sala.png",
                    "img/imoveis/vila-buritis-q02/cozinha-1.png",
                    "img/imoveis/vila-buritis-q02/cozinha-2.png",
                    "img/imoveis/vila-buritis-q02/quarto-1.png",
                    "img/imoveis/vila-buritis-q02/quarto-2.png",
                    "img/imoveis/vila-buritis-q02/banheiro-1.png",
                    "img/imoveis/vila-buritis-q02/garagem.png",
                ]
            ),
        },
        {
            "slug": "chacara-planaltina-df-230",
            "titulo": "Chácara — Área Rural de Planaltina (DF-230)",
            "descricao": descricao_chacara,
            "preco": 650000.0,
            "tipo": "terreno",
            "area_m2": 60000.0,
            "quartos": 0,
            "banheiros": 0,
            "vagas": 0,
            "bairro": "Área Rural",
            "cidade": "Planaltina",
            "estado": "DF",
            "endereco": "DF-230, próximo à Casa da Uva",
            "destaque": True,
            "imagem_principal": "img/imoveis/chacara-planaltina/chacara-1.png",
            "imagens_json": json.dumps(
                [
                    "img/imoveis/chacara-planaltina/chacara-1.png",
                    "img/imoveis/chacara-planaltina/chacara-2.png",
                    "img/imoveis/chacara-planaltina/chacara-3.png",
                    "img/imoveis/chacara-planaltina/nascente.png",
                ]
            ),
        },
        {
            "slug": "lote-comercial-arapoanga-900m2",
            "titulo": "Lote Comercial — Arapoanga (900m²)",
            "descricao": descricao_arapoanga,
            "preco": 0.0,
            "tipo": "terreno",
            "area_m2": 900.0,
            "quartos": 0,
            "banheiros": 0,
            "vagas": 0,
            "bairro": "Arapoanga",
            "cidade": "Planaltina",
            "estado": "DF",
            "endereco": "Avenida comercial, Arapoanga",
            "destaque": True,
            "imagem_principal": "img/imoveis/arapoanga-comercial/frente.png",
            "imagens_json": json.dumps(
                [
                    "img/imoveis/arapoanga-comercial/frente.png",
                    "img/imoveis/arapoanga-comercial/corredor-lojas.png",
                ]
            ),
        },
        {
            "slug": "casa-vila-de-fatima-planaltina",
            "titulo": "Casa — Vila de Fátima (pavimento superior + kitnets)",
            "descricao": descricao_vila_fatima,
            "preco": 360000.0,
            "tipo": "casa",
            "area_m2": 0.0,
            "quartos": 5,
            "banheiros": 4,
            "vagas": 2,
            "bairro": "Vila de Fátima",
            "cidade": "Planaltina",
            "estado": "DF",
            "endereco": "Vila de Fátima, Planaltina/DF — próximo à UnB, Potiguar e Atacadão",
            "destaque": True,
            "imagem_principal": "img/imoveis/vila-de-fatima/08.png",
            "imagens_json": json.dumps(
                [f"img/imoveis/vila-de-fatima/{n:02d}.png" for n in range(1, 13)]
            ),
        },
    ]

    static_root = Path(__file__).resolve().parents[1] / "static"
    amostras = [
        sync_vila_fatima_imagens_from_static(r, static_root) if r["slug"] == _VILA_SLUG else r
        for r in amostras
    ]

    for row in amostras:
        existing = Imovel.query.filter_by(slug=row["slug"]).first()
        if existing:
            for k, v in row.items():
                setattr(existing, k, v)
        else:
            db.session.add(Imovel(**row))
    db.session.commit()
