import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-altere-em-producao")
    SITE_NAME = os.environ.get("SITE_NAME", "Valdemir Pereira Imóveis")
    # Apenas dígitos, com DDI (Brasil: 55). Ex.: 5511987654321 — use WHATSAPP_NUMBER em produção.
    WHATSAPP_NUMBER = os.environ.get("WHATSAPP_NUMBER", "5561992029010")
    INSTAGRAM_URL = os.environ.get(
        "INSTAGRAM_URL",
        "https://www.instagram.com/reel/DUWAZtqEQS8/?igsh=MXNqM253bTJ4ZGc2ZQ==",
    )
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "instance", "imoveis.db"),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
