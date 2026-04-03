import json

from flask import Blueprint, abort, render_template

from app.models import Imovel

bp_imoveis = Blueprint("imoveis", __name__)


@bp_imoveis.route("/")
def listar():
    return render_template(
        "imoveis/lista.html",
        imoveis=Imovel.query.order_by(Imovel.destaque.desc(), Imovel.preco.desc()).all(),
    )


@bp_imoveis.route("/<slug>")
def detalhe(slug: str):
    imovel = Imovel.query.filter_by(slug=slug).first()
    if not imovel:
        abort(404)
    try:
        galeria = json.loads(imovel.imagens_json or "[]")
    except json.JSONDecodeError:
        galeria = [imovel.imagem_principal]
    similares = (
        Imovel.query.filter(Imovel.id != imovel.id, Imovel.cidade == imovel.cidade)
        .limit(3)
        .all()
    )
    return render_template(
        "imoveis/detalhe.html",
        imovel=imovel,
        galeria=galeria,
        similares=similares,
    )
