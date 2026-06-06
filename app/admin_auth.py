from __future__ import annotations

from functools import wraps

from flask import redirect, session, url_for
from werkzeug.security import check_password_hash


def admin_logado() -> bool:
    return bool(session.get("admin"))


def verificar_senha_admin(senha: str, password_hash: str) -> bool:
    return check_password_hash(password_hash, senha)


def login_admin() -> None:
    session["admin"] = True
    session.permanent = True


def logout_admin() -> None:
    session.pop("admin", None)


def exigir_admin(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not admin_logado():
            return redirect(url_for("admin.login", next=request_path()))
        return f(*args, **kwargs)

    return wrapper


def request_path() -> str:
    from flask import request

    return request.full_path if request.query_string else request.path
