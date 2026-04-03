"""Uso: python tools/preflight_deploy.py — checagens rápidas antes do deploy."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import create_app  # noqa: E402
from app.models import Imovel  # noqa: E402


def main() -> int:
    app = create_app()
    c = app.test_client()
    fail: list[tuple] = []

    def get(path: str, code: int = 200) -> None:
        r = c.get(path, follow_redirects=True)
        if r.status_code != code:
            fail.append((path, code, r.status_code))

    for p in ["/", "/sobre", "/contato", "/privacidade", "/imoveis/"]:
        get(p, 200)

    with app.app_context():
        slugs = [x.slug for x in Imovel.query.order_by(Imovel.id).all()]

    for s in slugs:
        get(f"/imoveis/{s}", 200)
    get("/imoveis/nao-existe-xyz", 404)

    static = Path(app.static_folder)
    for rel in ["css/styles.css", "js/main.js", "img/site/capa.png"]:
        r = c.get("/static/" + rel)
        if r.status_code != 200:
            fail.append(("/static/" + rel, 200, r.status_code))

    missing: list[str] = []
    with app.app_context():
        for im in Imovel.query.all():
            paths = [im.imagem_principal] + json.loads(im.imagens_json or "[]")
            for rel in paths:
                if not rel or rel.startswith(("http://", "https://")):
                    continue
                rel = rel.lstrip("/")
                if rel.startswith("static/"):
                    rel = rel[7:]
                fp = static.joinpath(*rel.split("/"))
                if not fp.is_file():
                    missing.append(str(fp))

    ok = not fail and not missing
    print("Rotas e estáticos críticos:", "OK" if not fail else f"FALHA {fail}")
    print("Imagens referenciadas no banco:", "OK" if not missing else f"{len(missing)} ausentes")
    for m in missing[:25]:
        print(" ", m)
    print("Imóveis:", slugs)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
