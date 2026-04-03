import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Com o pacote `app`, o root padrão do Flask é a pasta `app/`; templates e static ficam na raiz do projeto.
_ROOT = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))


def create_app(config_object: str | object = "app.config.Config") -> Flask:
    app = Flask(
        __name__,
        template_folder=os.path.join(_ROOT, "templates"),
        static_folder=os.path.join(_ROOT, "static"),
        instance_relative_config=True,
    )
    if isinstance(config_object, str):
        app.config.from_object(config_object)
    else:
        app.config.from_object(config_object)

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)

    from app.routes import bp_main, bp_imoveis

    app.register_blueprint(bp_main)
    app.register_blueprint(bp_imoveis, url_prefix="/imoveis")

    from app.formatacao import format_brl, label_tipo, media_url

    app.jinja_env.filters["brl"] = format_brl
    app.jinja_env.filters["tipo_label"] = label_tipo
    app.jinja_env.filters["media_url"] = media_url

    @app.template_global()
    def whatsapp_com_texto(texto: str | None = None):
        """Gera link wa.me com mensagem personalizada (ex.: interesse em um imóvel)."""
        from urllib.parse import quote

        from flask import current_app

        raw = (current_app.config.get("WHATSAPP_NUMBER") or "").strip()
        digits = "".join(c for c in raw if c.isdigit())
        if not digits:
            return None
        msg = quote((texto or "Olá! Gostaria de falar com um corretor.").strip(), safe="")
        return f"https://wa.me/{digits}?text={msg}"

    @app.errorhandler(404)
    def pagina_nao_encontrada(_e):
        from flask import render_template

        return render_template("errors/404.html"), 404

    @app.context_processor
    def inject_globals():
        from datetime import datetime
        from urllib.parse import quote

        from flask import current_app

        cfg = current_app.config
        site_name = cfg.get("SITE_NAME") or "Valdemir Pereira Imóveis"
        ig = (cfg.get("INSTAGRAM_URL") or "").strip()
        raw = (cfg.get("WHATSAPP_NUMBER") or "").strip()
        digits = "".join(c for c in raw if c.isdigit())
        whatsapp_href = None
        if digits:
            texto = quote("Olá! Gostaria de falar com um corretor.", safe="")
            whatsapp_href = f"https://wa.me/{digits}?text={texto}"
        return {
            "ano_atual": datetime.now().year,
            "site_name": site_name,
            "whatsapp_href": whatsapp_href,
            "instagram_href": ig or None,
        }

    with app.app_context():
        db.create_all()
        from app import seed

        seed.ensure_sample_data()

    return app
