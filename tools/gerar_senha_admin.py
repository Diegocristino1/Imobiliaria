"""Gera ADMIN_PASSWORD_HASH para o painel /admin (variável de ambiente)."""
from __future__ import annotations

import getpass
import sys

from werkzeug.security import generate_password_hash


def main() -> int:
    if len(sys.argv) > 1:
        senha = sys.argv[1]
    else:
        senha = getpass.getpass("Nova senha do administrador: ")
        confirma = getpass.getpass("Confirme a senha: ")
        if senha != confirma:
            print("As senhas não coincidem.", file=sys.stderr)
            return 1
    if len(senha) < 6:
        print("Use ao menos 6 caracteres.", file=sys.stderr)
        return 1
    print(generate_password_hash(senha))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
