"""Controller (MVC): recebe requisições e aciona os serviços. Sem prompts nem regras de aprovação."""
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from . import repository as repo, services
from .domain import validar_markdown
from .llm import LLMError, make_adapter

app = FastAPI(title="Agente de ADR")


class Cfg(BaseModel):
    provider: str
    model: str
    api_key: str
    dir: str
    messages: list[dict] = []


class SaveReq(BaseModel):
    dir: str
    arquivo: str
    markdown: str


class StatusReq(BaseModel):
    dir: str
    arquivo: str
    status: str = "Aceito"
    aprovador: str


@app.exception_handler(LLMError)
async def _llm(_: Request, e: LLMError): return JSONResponse({"detail": str(e)}, 502)


@app.exception_handler(ValueError)
async def _val(_: Request, e: ValueError): return JSONResponse({"detail": str(e)}, 400)


@app.exception_handler(FileExistsError)
async def _exists(_: Request, e: FileExistsError): return JSONResponse({"detail": str(e)}, 409)


@app.get("/api/adrs")
def listar(dir: str):
    return [{k: v for k, v in a.items() if k != "texto"} for a in repo.listar(dir)]


@app.post("/api/chat")
async def chat(r: Cfg):
    resp, pronto = await services.conversar(make_adapter(r.provider, r.api_key, r.model), r.messages, r.dir)
    return {"resposta": resp, "pronto": pronto}


@app.post("/api/generate")
async def generate(r: Cfg):
    return await services.gerar(make_adapter(r.provider, r.api_key, r.model), r.messages, r.dir)


@app.post("/api/save")
def save(r: SaveReq):
    erros = validar_markdown(r.markdown)
    if erros: raise ValueError("; ".join(erros))
    return {"arquivo": repo.salvar(r.dir, r.arquivo, r.markdown)}


@app.post("/api/status")
def status(r: StatusReq):
    repo.mudar_status(r.dir, r.arquivo, r.status, r.aprovador)
    return {"ok": True}


app.mount("/", StaticFiles(directory=Path(__file__).parent.parent / "static", html=True))
