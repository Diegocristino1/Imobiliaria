from __future__ import annotations

import json
import re
from pathlib import Path

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

IMG_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
VIDEO_EXT = {".mp4", ".webm", ".mov", ".m4v"}
MAX_IMG_BYTES = 12 * 1024 * 1024
MAX_VIDEO_BYTES = 80 * 1024 * 1024


def parse_json_list(raw: str | None) -> list[str]:
    if not raw:
        return []
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return []
    if not isinstance(data, list):
        return []
    return [str(x).strip() for x in data if str(x).strip()]


def dump_json_list(items: list[str]) -> str:
    return json.dumps(items, ensure_ascii=False)


def media_folder_slug(slug: str) -> str:
    safe = re.sub(r"[^a-z0-9-]", "", slug.lower())
    return safe or "imovel"


def _folder_from_rel_path(rel_path: str) -> str | None:
    rel = rel_path.replace("\\", "/").lstrip("/")
    if rel.startswith("static/"):
        rel = rel[7:]
    parts = rel.split("/")
    if len(parts) >= 4 and parts[0] == "img" and parts[1] == "imoveis":
        return parts[2]
    if len(parts) >= 4 and parts[0] == "video" and parts[1] == "imoveis":
        return parts[2]
    return None


def resolve_imovel_folder(slug: str, imagem_principal: str | None, imagens_json: str | None) -> str:
    for path in [imagem_principal, *parse_json_list(imagens_json)]:
        if path:
            folder = _folder_from_rel_path(path)
            if folder:
                return folder
    return media_folder_slug(slug)


def imovel_img_dir(static_root: Path, folder: str) -> Path:
    d = static_root / "img" / "imoveis" / folder
    d.mkdir(parents=True, exist_ok=True)
    return d


def imovel_video_dir(static_root: Path, folder: str) -> Path:
    d = static_root / "video" / "imoveis" / folder
    d.mkdir(parents=True, exist_ok=True)
    return d


def _next_indexed_name(folder: Path, ext: str) -> str:
    ext = ext.lower()
    nums = []
    for f in folder.iterdir():
        if f.is_file() and f.suffix.lower() == ext:
            stem = f.stem
            if stem.isdigit():
                nums.append(int(stem))
    n = max(nums, default=0) + 1
    return f"{n:02d}{ext}"


def rel_img_path(folder: str, filename: str) -> str:
    return f"img/imoveis/{folder}/{filename}"


def rel_video_path(folder: str, filename: str) -> str:
    return f"video/imoveis/{folder}/{filename}"


def save_upload(
    file: FileStorage,
    dest_dir: Path,
    allowed_ext: set[str],
    max_bytes: int,
    rel_builder,
) -> str:
    if not file or not file.filename:
        raise ValueError("Nenhum arquivo enviado.")
    original = secure_filename(file.filename)
    if not original or "." not in original:
        raise ValueError("Nome de arquivo inválido.")
    ext = Path(original).suffix.lower()
    if ext not in allowed_ext:
        raise ValueError(f"Formato não permitido ({ext}).")
    file.stream.seek(0, 2)
    size = file.stream.tell()
    file.stream.seek(0)
    if size > max_bytes:
        raise ValueError("Arquivo muito grande.")
    name = _next_indexed_name(dest_dir, ext)
    path = dest_dir / name
    file.save(path)
    return rel_builder(name)


def save_images(
    static_root: Path,
    slug: str,
    files: list[FileStorage],
    imagem_principal: str | None = None,
    imagens_json: str | None = None,
) -> list[str]:
    sub = resolve_imovel_folder(slug, imagem_principal, imagens_json)
    folder = imovel_img_dir(static_root, sub)
    paths: list[str] = []
    for f in files:
        if f and f.filename:
            paths.append(
                save_upload(
                    f,
                    folder,
                    IMG_EXT,
                    MAX_IMG_BYTES,
                    lambda name, sub=sub: rel_img_path(sub, name),
                )
            )
    return paths


def save_videos(
    static_root: Path,
    slug: str,
    files: list[FileStorage],
    imagem_principal: str | None = None,
    imagens_json: str | None = None,
) -> list[str]:
    sub = resolve_imovel_folder(slug, imagem_principal, imagens_json)
    folder = imovel_video_dir(static_root, sub)
    paths: list[str] = []
    for f in files:
        if f and f.filename:
            paths.append(
                save_upload(
                    f,
                    folder,
                    VIDEO_EXT,
                    MAX_VIDEO_BYTES,
                    lambda name, sub=sub: rel_video_path(sub, name),
                )
            )
    return paths


def delete_static_file(static_root: Path, rel_path: str) -> None:
    rel = rel_path.lstrip("/").replace("\\", "/")
    if rel.startswith("static/"):
        rel = rel[7:]
    if not (rel.startswith("img/imoveis/") or rel.startswith("video/imoveis/")):
        return
    full = static_root / rel
    if full.is_file():
        full.unlink()
