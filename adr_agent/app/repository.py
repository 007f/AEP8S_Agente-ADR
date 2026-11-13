"""Infraestrutura: persistência em pasta de arquivos .md."""
import re
import unicodedata
from pathlib import Path
from .domain import aplicar_status


def _dir(p: str) -> Path:
    d = Path(p).expanduser().resolve()
    if not d.is_dir(): raise ValueError(f"Pasta não encontrada: {d}")
    return d


def _num(nome: str):
    m = re.match(r"ADR-(\d+)", nome, re.I)
    return int(m.group(1)) if m else None


def listar(pasta: str) -> list[dict]:
    out = []
    for f in sorted(_dir(pasta).glob("*.md")):
        n = _num(f.name)
        if not n: continue  # ignora o modelo (ADR-0000) e arquivos fora do padrão
        t = f.read_text(encoding="utf-8")
        st, ti = re.search(r"\*\*Status:\*\*\s*(.+)", t), re.search(r"^#\s*(.+)", t, re.M)
        out.append({"arquivo": f.name, "titulo": ti.group(1).strip() if ti else f.stem,
                    "status": st.group(1).strip() if st else "?", "texto": t})
    return out


def proximo_numero(pasta: str) -> int:
    nums = [n for f in _dir(pasta).glob("*.md") if (n := _num(f.name)) is not None]
    return max(nums, default=0) + 1


def nome_arquivo(numero: int, titulo: str) -> str:
    s = unicodedata.normalize("NFKD", titulo).encode("ascii", "ignore").decode().lower()
    return f"ADR-{numero:04d}-{re.sub(r'[^a-z0-9]+', '-', s).strip('-')[:60]}.md"


def salvar(pasta: str, arquivo: str, md: str) -> str:
    p = _dir(pasta) / Path(arquivo).name
    if p.exists(): raise FileExistsError(f"{p.name} já existe; não sobrescrevo ADRs existentes")
    p.write_text(md, encoding="utf-8")
    return p.name


def mudar_status(pasta: str, arquivo: str, novo: str, aprovador: str) -> None:
    p = _dir(pasta) / Path(arquivo).name
    p.write_text(aplicar_status(p.read_text(encoding="utf-8"), novo, aprovador), encoding="utf-8")
