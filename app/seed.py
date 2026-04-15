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

    descricao_quintas_amanhecer = (
        "Valdemir Pereira vende: (um) lote todo murado com plantas frutíferas no Bairro Quintas do Amanhecer II.\n\n"
        "Metragem: 200 m²\n\n"
        "Documentação: escriturado.\n\n"
        "Ótimo lugar para o descanso.\n\n"
        "Investimento: R$ 60.000,00\n"
        "Aceita carro acima de R$ 40.000,00 como parte do pagamento.\n\n"
        "Para maiores informações fale comigo.\n"
        "(61) 99202-9010\n"
        "CRECI: 32849"
    )

    descricao_buritis_iv_lote_residencias = (
        "Valdemir Pereira vende: um lote com (02) duas residências gerando uma renda de R$ 1.500 mensais.\n\n"
        "Localização: Quadra 22 Conjunto I AE 04 Lote 01, Buritis IV.\n\n"
        "Metragem: 180 m²\n\n"
        "Documentação: cessão de direito.\n\n"
        "Investimento: R$ 230.000,00\n"
        "Aceita carro como parte de pagamento.\n\n"
        "Agende uma visita com seu corretor.\n\n"
        "Valdemir Pereira\n"
        "CRECI 32849\n"
        "(61) 99202-9010"
    )

    descricao_chacara_maria_barro = (
        "Valdemir Pereira, corretor de imóveis, vende: uma chácara na antiga Maria do Barro (horta comunitária).\n\n"
        "Local com água, luz e muitas plantas frutíferas.\n\n"
        "Metragem: 1.000 m² — ideal para descanso e lazer, com fácil acesso.\n\n"
        "Documentação: cessão de direito.\n\n"
        "Investimento: R$ 320.000,00\n\n"
        "Agende uma visita com seu corretor.\n\n"
        "Valdemir Pereira"
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
            "slug": "chacara-maria-do-barro-horta-comunitaria-1000m2",
            "titulo": "Chácara — Maria do Barro (horta comunitária, 1.000 m²)",
            "descricao": descricao_chacara_maria_barro,
            "preco": 320000.0,
            "tipo": "terreno",
            "area_m2": 1000.0,
            "quartos": 0,
            "banheiros": 0,
            "vagas": 0,
            "bairro": "Maria do Barro",
            "cidade": "Planaltina",
            "estado": "DF",
            "endereco": "Antiga Maria do Barro (horta comunitária), Planaltina/DF",
            "destaque": True,
            "imagem_principal": "img/cachara1.jpeg",
            "imagens_json": json.dumps(
                [
                    "img/cachara1.jpeg",
                    "img/chacara4.jpeg",
                    "img/arvores_chacara.jpeg",
                    "img/chacara3.jpeg",
                    "img/chacaraa.jpeg",
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
            "slug": "lote-quintas-do-amanhecer-ii-200m2",
            "titulo": "Lote — Quintas do Amanhecer II (200m², murado)",
            "descricao": descricao_quintas_amanhecer,
            "preco": 60000.0,
            "tipo": "terreno",
            "area_m2": 200.0,
            "quartos": 0,
            "banheiros": 0,
            "vagas": 0,
            "bairro": "Quintas do Amanhecer II",
            "cidade": "Planaltina",
            "estado": "DF",
            "endereco": "Bairro Quintas do Amanhecer II, Planaltina/DF",
            "destaque": True,
            "imagem_principal": "img/vale1.jpeg",
            "imagens_json": json.dumps(
                [
                    "img/vale1.jpeg",
                    "img/vale2.jpeg",
                    "img/vale3.jpeg",
                    "img/vale4.jpeg",
                    "img/vale5.jpeg",
                ]
            ),
        },
        {
            "slug": "lote-buritis-iv-q22-duas-residencias-renda",
            "titulo": "Lote — Buritis IV (2 residências, renda ~R$ 1.500)",
            "descricao": descricao_buritis_iv_lote_residencias,
            "preco": 230000.0,
            "tipo": "casa",
            "area_m2": 180.0,
            "quartos": 0,
            "banheiros": 0,
            "vagas": 0,
            "bairro": "Buritis IV",
            "cidade": "Planaltina",
            "estado": "DF",
            "endereco": "Quadra 22 Conjunto I, AE 04 Lote 01, Buritis IV, Planaltina/DF",
            "destaque": True,
            "imagem_principal": "img/b4.jpeg",
            "imagens_json": json.dumps(
                [
                    "img/b4.jpeg",
                    "img/b4-1.jpeg",
                    "img/b4-2.jpeg",
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
