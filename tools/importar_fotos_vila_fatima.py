"""
Copia as 12 fotos da Vila de Fátima para static/img/imoveis/vila-de-fatima/ como 01.png ... 12.png.

Ordem de uso (escolha uma):
  1) Coloque manualmente 01.png ... 12.png em: assets_import/vila-fatima/
  2) Ou defina VILA_FATIMA_SRC apontando para a pasta assets do Cursor que contém os arquivos longos:
       set VILA_FATIMA_SRC=C:\\Users\\SEU_USUARIO\\.cursor\\projects\\c-Desenvolvedor-full-stack-Corretor-Imobiliario\\assets
       python tools/importar_fotos_vila_fatima.py
  3) Ou execute: .\\tools\\copiar_fotos_vila_fatima.ps1
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "static" / "img" / "imoveis" / "vila-de-fatima"
MANUAL = ROOT / "assets_import" / "vila-fatima"

# Nomes no diretório assets do Cursor — mapeamento casa1…casa12 → 01.png…12.png
_P = "c__Users_diego_AppData_Roaming_Cursor_User_workspaceStorage_efb4aad1fbdecb8b1c43e96ef8cd7fa1_images_"
CURSOR_NAMES = [
    f"{_P}casa1-7d2ecf11-5b86-45b9-96e5-a37b8624701c.png",
    f"{_P}casa2-9db686d8-5ea6-4447-aecc-c62e096f2d9e.png",
    f"{_P}casa3-2750345d-9b93-4423-964b-cbbd60f7e319.png",
    f"{_P}casa4-46f8543e-8eb2-43ee-ae53-ae5c1d505946.png",
    f"{_P}casa5-ee0beb27-f6eb-4d2e-b869-147fbe25cb97.png",
    f"{_P}casa6-c3ffda0c-cb25-40c8-9dde-590e252668ee.png",
    f"{_P}casa7-3b6073b9-b13a-4ef3-bb00-f25e0c79cdbe.png",
    f"{_P}casa8-f5e0e52b-7f78-4504-a105-02a79ac7b796.png",
    f"{_P}casa9-694f35c3-cd52-4803-b61d-ae06fef80a9f.png",
    f"{_P}casa10-c7639bff-d1c5-4d18-aaac-7de40a831e91.png",
    f"{_P}casa11-05817773-c5b3-463b-b979-60b49f6e4503.png",
    f"{_P}casa12-66788ba2-9e17-4ca8-9e15-65898e7a7b7b.png",
]

DEFAULT_CURSOR_ASSETS = (
    Path.home()
    / ".cursor"
    / "projects"
    / "c-Desenvolvedor-full-stack-Corretor-Imobiliario"
    / "assets"
)


def main() -> int:
    DEST.mkdir(parents=True, exist_ok=True)

    # Modo simples: já existem 01.png ... 12.png em assets_import/vila-fatima
    if (MANUAL / "01.png").is_file():
        for i in range(1, 13):
            src = MANUAL / f"{i:02d}.png"
            if not src.is_file():
                print(f"Faltando: {src}", file=sys.stderr)
                return 1
            shutil.copy2(src, DEST / f"{i:02d}.png")
        print(f"OK (manual): copiado de {MANUAL} -> {DEST}")
        return 0

    src_root = Path(os.environ.get("VILA_FATIMA_SRC", str(DEFAULT_CURSOR_ASSETS)))
    missing: list[str] = []
    for name in CURSOR_NAMES:
        src = src_root / name
        if not src.is_file():
            missing.append(str(src))
    if missing:
        print(
            "Nao encontrei estes arquivos (ajuste VILA_FATIMA_SRC ou use assets_import/vila-fatima/01.png ...):\n"
            + "\n".join(missing[:5])
            + ("\n..." if len(missing) > 5 else ""),
            file=sys.stderr,
        )
        return 1

    for i, name in enumerate(CURSOR_NAMES, start=1):
        shutil.copy2(src_root / name, DEST / f"{i:02d}.png")

    print(f"OK: 12 fotos em {DEST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
