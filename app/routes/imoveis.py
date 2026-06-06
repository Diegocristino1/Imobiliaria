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
    from app.media_store import parse_json_list

    galeria = parse_json_list(imovel.imagens_json)
    if not galeria:
        galeria = [imovel.imagem_principal] if imovel.imagem_principal else []
    videos = parse_json_list(imovel.videos_json)
    similares = (
        Imovel.query.filter(Imovel.id != imovel.id, Imovel.cidade == imovel.cidade)
        .limit(3)
        .all()
    )
    return render_template(
        "imoveis/detalhe.html",
        imovel=imovel,
        galeria=galeria,
        videos=videos,
        similares=similares,
    )
