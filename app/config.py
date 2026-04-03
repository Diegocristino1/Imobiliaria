import os
import tempfile
from pathlib import Path


def _is_vercel() -> bool:
    return bool(os.environ.get("VERCEL") or os.environ.get("VERCEL_ENV"))


def database_uri() -> str:
    """URI do banco: PostgreSQL (DATABASE_URL), ou SQLite local, ou /tmp na Vercel (FS somente leitura)."""
    raw = (os.environ.get("DATABASE_URL") or "").strip()
    if raw:
        if raw.startswith("postgres://"):
            return "postgresql://" + raw[len("postgres://") :]
        return raw
    if _is_vercel():
        # Serverless: única área gravável é /tmp; instance/ do deploy é read-only.
        p = (Path(tempfile.gettempdir()) / "imoveis.db").resolve()
        return "sqlite:///" + p.as_posix()
    base = Path(__file__).resolve().parents[1] / "instance" / "imoveis.db"
    return "sqlite:///" + base.as_posix()


_DEFAULT_URI = database_uri()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-altere-em-producao")
    SITE_NAME = os.environ.get("SITE_NAME", "Valdemir Pereira Imóveis")
    # Apenas dígitos, com DDI (Brasil: 55). Ex.: 5511987654321 — use WHATSAPP_NUMBER em produção.
    WHATSAPP_NUMBER = os.environ.get("WHATSAPP_NUMBER", "5561992029010")
    INSTAGRAM_URL = os.environ.get(
        "INSTAGRAM_URL",
        "https://www.instagram.com/reel/DUWAZtqEQS8/?igsh=MXNqM253bTJ4ZGc2ZQ==",
    )
    SQLALCHEMY_DATABASE_URI = _DEFAULT_URI
    SQLALCHEMY_ENGINE_OPTIONS = (
        {"connect_args": {"check_same_thread": False}} if _DEFAULT_URI.startswith("sqlite") else {}
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
