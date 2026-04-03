"""Servidor de desenvolvimento.

Produção: use gunicorn ou waitress.

Este arquivo tenta usar o Python do `.venv` automaticamente, para evitar
o erro `ModuleNotFoundError: No module named 'flask'` quando o usuário
rodar `python run.py` com o Python do sistema.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _try_reexec_with_venv(argv: list[str]) -> None:
    root = Path(__file__).resolve().parent
    venv_python = root / ".venv" / "Scripts" / "python.exe"
    if not venv_python.exists():
        raise

    running_in_venv = Path(sys.executable).resolve() == venv_python.resolve()
    if running_in_venv:
        # Já estamos no venv e ainda assim falhou importação: não faz sentido reexecutar.
        raise

    # Roda o mesmo script com o interpretador do venv.
    subprocess.check_call([str(venv_python), str(Path(__file__).resolve()), *argv])


try:
    from app import create_app
except ModuleNotFoundError as e:
    # Se o pacote faltar no Python atual, relança usando o Python do venv.
    _try_reexec_with_venv(sys.argv[1:])
    raise SystemExit(0)
except Exception:
    # Mantém o comportamento padrão para outros erros.
    raise

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
