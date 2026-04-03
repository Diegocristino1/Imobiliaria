from flask import Blueprint, render_template

from app.models import Imovel

bp_main = Blueprint("main", __name__)


@bp_main.route("/")
def index():
    destaques = Imovel.query.filter_by(destaque=True).order_by(Imovel.preco.desc()).limit(6).all()
    recentes = Imovel.query.order_by(Imovel.criado_em.desc()).limit(6).all()
    return render_template("index.html", destaques=destaques, recentes=recentes)


@bp_main.route("/sobre")
def sobre():
    return render_template("sobre.html")


@bp_main.route("/contato")
def contato():
    return render_template("contato.html")


@bp_main.route("/privacidade")
def privacidade():
    return render_template("privacidade.html")
