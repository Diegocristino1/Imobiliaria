"""Entrada preferida na Vercel — reexporta o WSGI (`wsgi.py`).

O diretório `app/` é o *pacote* do projeto; sem este ficheiro, o detector
da Vercel pode escolher um entrypoint errado.
"""

from wsgi import app

__all__ = ["app"]
