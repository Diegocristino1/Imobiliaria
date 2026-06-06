from __future__ import annotations

from pathlib import Path

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from app import db
from app.admin_auth import (
    admin_logado,
    exigir_admin,
    login_admin,
    logout_admin,
    verificar_senha_admin,
)
from app.media_store import (
    delete_static_file,
    dump_json_list,
    parse_json_list,
    save_images,
    save_videos,
)
from app.models import Imovel

bp_admin = Blueprint("admin", __name__, url_prefix="/admin")


def _static_root() -> Path:
    return Path(current_app.static_folder or "static")


@bp_admin.route("/login", methods=["GET", "POST"])
def login():
    if admin_logado():
        return redirect(url_for("admin.painel"))
    if request.method == "POST":
        senha = (request.form.get("senha") or "").strip()
        if verificar_senha_admin(senha, current_app.config["ADMIN_PASSWORD_HASH"]):
            login_admin()
            dest = request.args.get("next") or url_for("admin.painel")
            if not dest.startswith("/admin"):
                dest = url_for("admin.painel")
            return redirect(dest)
        flash("Senha incorreta.", "error")
    return render_template("admin/login.html")


@bp_admin.route("/logout")
def logout():
    logout_admin()
    flash("Sessão encerrada.", "success")
    return redirect(url_for("admin.login"))


@bp_admin.route("/")
@exigir_admin
def painel():
    imoveis = Imovel.query.order_by(Imovel.titulo).all()
    return render_template("admin/painel.html", imoveis=imoveis)


@bp_admin.route("/imovel/<int:imovel_id>", methods=["GET", "POST"])
@exigir_admin
def imovel(imovel_id: int):
    imovel = db.session.get(Imovel, imovel_id)
    if not imovel:
        flash("Imóvel não encontrado.", "error")
        return redirect(url_for("admin.painel"))

    static_root = _static_root()
    galeria = parse_json_list(imovel.imagens_json)
    videos = parse_json_list(imovel.videos_json)

    if request.method == "POST":
        acao = request.form.get("acao", "")

        if acao == "upload_fotos":
            arquivos = request.files.getlist("fotos")
            try:
                novos = save_images(
                    static_root,
                    imovel.slug,
                    arquivos,
                    imovel.imagem_principal,
                    imovel.imagens_json,
                )
                if not novos:
                    flash("Selecione ao menos uma foto.", "error")
                else:
                    galeria = galeria + novos
                    if not imovel.imagem_principal or imovel.imagem_principal not in galeria:
                        imovel.imagem_principal = novos[0]
                    imovel.imagens_json = dump_json_list(galeria)
                    db.session.commit()
                    flash(f"{len(novos)} foto(s) adicionada(s).", "success")
            except ValueError as e:
                flash(str(e), "error")

        elif acao == "upload_videos":
            arquivos = request.files.getlist("videos")
            try:
                novos = save_videos(
                    static_root,
                    imovel.slug,
                    arquivos,
                    imovel.imagem_principal,
                    imovel.imagens_json,
                )
                if not novos:
                    flash("Selecione ao menos um vídeo.", "error")
                else:
                    videos = videos + novos
                    imovel.videos_json = dump_json_list(videos)
                    db.session.commit()
                    flash(f"{len(novos)} vídeo(s) adicionado(s).", "success")
            except ValueError as e:
                flash(str(e), "error")

        elif acao == "principal":
            path = (request.form.get("path") or "").strip()
            if path in galeria:
                imovel.imagem_principal = path
                db.session.commit()
                flash("Foto principal atualizada.", "success")
            else:
                flash("Foto inválida.", "error")

        elif acao == "remover_foto":
            path = (request.form.get("path") or "").strip()
            if path in galeria:
                galeria = [p for p in galeria if p != path]
                imovel.imagens_json = dump_json_list(galeria)
                if imovel.imagem_principal == path:
                    imovel.imagem_principal = galeria[0] if galeria else imovel.imagem_principal
                delete_static_file(static_root, path)
                db.session.commit()
                flash("Foto removida.", "success")

        elif acao == "remover_video":
            path = (request.form.get("path") or "").strip()
            if path in videos:
                videos = [p for p in videos if p != path]
                imovel.videos_json = dump_json_list(videos)
                delete_static_file(static_root, path)
                db.session.commit()
                flash("Vídeo removido.", "success")

        return redirect(url_for("admin.imovel", imovel_id=imovel.id))

    galeria = parse_json_list(imovel.imagens_json)
    videos = parse_json_list(imovel.videos_json)
    return render_template(
        "admin/imovel.html",
        imovel=imovel,
        galeria=galeria,
        videos=videos,
    )
