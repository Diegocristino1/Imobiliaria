from __future__ import annotations

import re
import unicodedata
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
from app.formatacao import TIPO_IMOVEL_LABEL
from app.media_store import (
    delete_static_file,
    dump_json_list,
    parse_json_list,
    save_images,
    save_videos,
)
from app.models import Imovel

bp_admin = Blueprint("admin", __name__, url_prefix="/admin")

TIPOS_IMOVEL = list(TIPO_IMOVEL_LABEL.keys())


def _static_root() -> Path:
    return Path(current_app.static_folder or "static")


def _slugify(text: str) -> str:
    t = unicodedata.normalize("NFKD", text)
    t = t.encode("ascii", "ignore").decode("ascii")
    t = re.sub(r"[^a-z0-9\s-]", "", t.lower())
    t = re.sub(r"[\s_-]+", "-", t).strip("-")
    return (t[:100] if t else "imovel")


def _slug_unico(base: str) -> str:
    slug = base[:120]
    n = 2
    while Imovel.query.filter_by(slug=slug).first():
        slug = f"{base[:110]}-{n}"[:120]
        n += 1
    return slug


def _parse_float(raw: str | None, default: float = 0.0) -> float:
    if not raw or not str(raw).strip():
        return default
    s = str(raw).strip()
    if "," in s:
        s = s.replace(".", "").replace(",", ".")
    else:
        s = s.replace(",", "")
    try:
        return float(s)
    except ValueError:
        return default


def _parse_int(raw: str | None, default: int = 0) -> int:
    if not raw or not str(raw).strip():
        return default
    try:
        return max(0, int(float(str(raw).strip().replace(",", "."))))
    except ValueError:
        return default


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


@bp_admin.route("/imovel/novo", methods=["GET", "POST"])
@exigir_admin
def novo_imovel():
    if request.method == "POST":
        titulo = (request.form.get("titulo") or "").strip()
        descricao = (request.form.get("descricao") or "").strip()
        bairro = (request.form.get("bairro") or "").strip()
        cidade = (request.form.get("cidade") or "Planaltina").strip()
        estado = (request.form.get("estado") or "DF").strip().upper()[:2]
        endereco = (request.form.get("endereco") or "").strip()
        tipo = (request.form.get("tipo") or "casa").strip().lower()
        if tipo not in TIPOS_IMOVEL:
            tipo = "casa"

        erros: list[str] = []
        if not titulo:
            erros.append("Informe o título do imóvel.")
        if not descricao:
            erros.append("Informe a descrição.")
        if not bairro:
            erros.append("Informe o bairro.")
        if not endereco:
            erros.append("Informe o endereço ou referência de localização.")

        arquivos = request.files.getlist("fotos")
        if not any(f and f.filename for f in arquivos):
            erros.append("Envie ao menos uma foto do imóvel.")

        if erros:
            for msg in erros:
                flash(msg, "error")
            return render_template(
                "admin/novo_imovel.html",
                tipos=TIPOS_IMOVEL,
                form=request.form,
            )

        slug = _slug_unico(_slugify(titulo))
        static_root = _static_root()
        try:
            novos = save_images(static_root, slug, arquivos, None, None)
        except ValueError as e:
            flash(str(e), "error")
            return render_template(
                "admin/novo_imovel.html",
                tipos=TIPOS_IMOVEL,
                form=request.form,
            )

        if not novos:
            flash("Não foi possível salvar as fotos.", "error")
            return render_template(
                "admin/novo_imovel.html",
                tipos=TIPOS_IMOVEL,
                form=request.form,
            )

        imovel = Imovel(
            slug=slug,
            titulo=titulo,
            descricao=descricao,
            preco=_parse_float(request.form.get("preco")),
            tipo=tipo,
            area_m2=_parse_float(request.form.get("area_m2")),
            quartos=_parse_int(request.form.get("quartos")),
            banheiros=_parse_int(request.form.get("banheiros")),
            vagas=_parse_int(request.form.get("vagas")),
            bairro=bairro,
            cidade=cidade,
            estado=estado,
            endereco=endereco,
            destaque=bool(request.form.get("destaque")),
            imagem_principal=novos[0],
            imagens_json=dump_json_list(novos),
            videos_json=dump_json_list([]),
        )
        db.session.add(imovel)
        db.session.commit()
        flash(f"Imóvel «{titulo}» cadastrado com {len(novos)} foto(s).", "success")
        return redirect(url_for("admin.imovel", imovel_id=imovel.id))

    return render_template("admin/novo_imovel.html", tipos=TIPOS_IMOVEL, form=None)


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
                    imovel.imagem_principal = galeria[0] if galeria else ""
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
