from __future__ import annotations

from datetime import datetime

from app import db


class Imovel(db.Model):
    __tablename__ = "imoveis"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(120), unique=True, nullable=False, index=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # casa, apartamento, terreno, cobertura
    area_m2 = db.Column(db.Float, nullable=False)
    quartos = db.Column(db.Integer, nullable=False, default=0)
    banheiros = db.Column(db.Integer, nullable=False, default=0)
    vagas = db.Column(db.Integer, nullable=False, default=0)
    bairro = db.Column(db.String(120), nullable=False)
    cidade = db.Column(db.String(120), nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    endereco = db.Column(db.String(255), nullable=False)
    destaque = db.Column(db.Boolean, default=False, nullable=False)
    imagem_principal = db.Column(db.String(500), nullable=False)
    imagens_json = db.Column(db.Text, default="[]")  # JSON array of URLs
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<Imovel {self.slug}>"
