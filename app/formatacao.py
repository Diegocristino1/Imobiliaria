TIPO_IMOVEL_LABEL = {
    "casa": "Casa",
    "apartamento": "Apartamento",
    "terreno": "Terreno",
    "cobertura": "Cobertura",
}


def format_brl(value: float | None) -> str:
    if value is None:
        return "—"
    if float(value) <= 0:
        return "Sob consulta"
    neg = value < 0
    n = abs(int(round(float(value) * 100)))
    inteiro, cent = divmod(n, 100)
    grupos: list[str] = []
    resto = inteiro
    while resto >= 1000:
        resto, g = divmod(resto, 1000)
        grupos.append(f"{g:03d}")
    grupos.append(str(resto))
    corpo = ".".join(reversed(grupos))
    texto = f"R$ {corpo},{cent:02d}"
    return f"- {texto}" if neg else texto


def label_tipo(tipo: str | None) -> str:
    if not tipo:
        return "Imóvel"
    return TIPO_IMOVEL_LABEL.get(tipo.lower(), tipo.replace("_", " ").title())


def media_url(value: str | None) -> str:
    """URLs http(s) inalteradas; caminhos relativos a `static/` (ex.: img/imoveis/foto.jpg)."""
    from flask import url_for

    if value is None:
        return ""
    v = str(value).strip()
    if not v:
        return ""
    if v.startswith(("http://", "https://", "//")):
        return v
    fn = v.lstrip("/")
    if fn.startswith("static/"):
        fn = fn[7:]
    return url_for("static", filename=fn)
