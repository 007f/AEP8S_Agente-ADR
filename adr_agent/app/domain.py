"""Domínio: entidade ADR (Information Expert) e Builder do Markdown no modelo."""
import re
from datetime import date
from pydantic import BaseModel, Field

STATUS = ("Proposto", "Aceito", "Rejeitado", "Obsoleto", "Substituído")
TRANSICOES = {"Proposto": {"Aceito", "Rejeitado"}, "Aceito": {"Obsoleto", "Substituído"}}
SECOES = ["## Contexto e problema", "## Fatores de decisão", "## Opções consideradas",
          "## Resultado da decisão", "## Prós e contras das opções", "## Consequências",
          "## Confirmação", "## Links"]
TBD = "[A definir]"


class Opcao(BaseModel):
    nome: str
    descricao: str
    pros: list[str] = []
    contras: list[str] = []
    sugerida_pela_ia: bool = False  # True = sugestão do modelo, não avaliada pela equipe


class ADRDraft(BaseModel):
    """Campos que o LLM preenche."""
    titulo: str = Field(min_length=3)
    decisores: list[str] = []
    consultados: list[str] = []
    informados: list[str] = []
    substitui: str = ""
    relacionados: list[str] = []
    contexto: str
    fatores: list[str] = []
    opcoes: list[Opcao] = []
    escolhida: str = ""
    justificativa: str = ""
    detalhe: str = ""
    positivas: list[str] = []
    negativas: list[str] = []
    riscos: list[str] = []
    impacto: str = ""
    revisao: str = ""
    confirmacao: str = ""
    links: list[str] = []
    pendencias: list[str] = []
    conflitos: list[str] = []


class ADR(ADRDraft):
    numero: int
    status: str = "Proposto"  # o agente nunca cria ADR já aprovada
    data: str = Field(default_factory=lambda: date.today().isoformat())

    def pendencias_estruturais(self) -> list[str]:
        p = []
        if not self.decisores: p.append("Decisores não informados")
        if len(self.opcoes) < 2: p.append("Menos de duas opções consideradas")
        if not any(re.search(r"status quo|não fazer nada|manter", o.nome, re.I) for o in self.opcoes):
            p.append("Falta a opção 'não fazer nada / manter status quo'")
        if self.escolhida not in [o.nome for o in self.opcoes]:
            p.append("Opção escolhida não corresponde a nenhuma opção listada")
        if not self.fatores: p.append("Fatores de decisão não informados")
        for campo, msg in (("consultados", "Consultados não informados"), ("informados", "Informados não informados"),
                           ("positivas", "Consequências positivas não informadas"), ("negativas", "Consequências negativas não informadas"),
                           ("riscos", "Riscos não informados"), ("impacto", "Impacto não informado")):
            if not getattr(self, campo): p.append(msg)
        if sum(bool(re.search(r"status quo|não fazer nada", o.nome, re.I)) for o in self.opcoes) > 1:
            p.append("Há mais de uma opção de status quo; unifique")
        if not self.confirmacao: p.append("Critério de confirmação não informado")
        return p


class ADRBuilder:
    """Builder: monta o Markdown seção a seção, exatamente no modelo."""
    def __init__(self, adr: ADR):
        self.a, self.p = adr, []

    @staticmethod
    def _l(items): return "\n".join(f"* {i}" for i in items) if items else f"* {TBD}"
    @staticmethod
    def _j(items): return ", ".join(items) if items else TBD

    def cabecalho(self):
        a = self.a
        self.p.append(f"# ADR-{a.numero:04d}: {a.titulo}\n\n* **Status:** {a.status}\n* **Data:** {a.data}\n"
                      f"* **Decisores:** {self._j(a.decisores)}\n* **Consultados:** {self._j(a.consultados)}\n"
                      f"* **Informados:** {self._j(a.informados)}\n* **Substitui:** {a.substitui or '—'}\n"
                      f"* **Relacionados:** {', '.join(a.relacionados) or '—'}")
        return self

    def contexto(self):
        self.p.append(f"## Contexto e problema\n\n{self.a.contexto or TBD}\n\n## Fatores de decisão\n\n{self._l(self.a.fatores)}")
        return self

    def opcoes(self):
        blocos = []
        for i, o in enumerate(self.a.opcoes, 1):
            nota = "\n\n_Sugestão do modelo de IA — não avaliada pela equipe._" if o.sugerida_pela_ia else ""
            blocos.append(f"### Opção {i}: {o.nome}\n\n{o.descricao}{nota}")
        self.p.append("## Opções consideradas\n\n" + ("\n\n".join(blocos) or TBD))
        return self

    def resultado(self):
        a = self.a
        just = (a.justificativa or TBD).strip()
        m = re.search(r"\bporque\s+", just, re.I)
        if m and m.start() <= 100: just = just[m.end():]  # remove "Escolhida: X, porque" repetido
        just = just.strip().rstrip(".") or TBD
        w = just.split()[0]
        if w[0].isupper() and not (len(w) > 1 and w.isupper()): just = just[0].lower() + just[1:]  # preserva siglas
        self.p.append(f"## Resultado da decisão\n\n**Escolhida: {a.escolhida or TBD}, porque {just}.**\n\n{a.detalhe}".rstrip())
        return self

    def pros_contras(self):
        blocos = []
        for i, o in enumerate(self.a.opcoes, 1):
            ls = [f"* 👍 {x}" for x in o.pros] + [f"* 👎 {x}" for x in o.contras]
            blocos.append(f"### Opção {i}\n\n" + ("\n".join(ls) or f"* {TBD}"))
        self.p.append("## Prós e contras das opções\n\n" + "\n\n".join(blocos))
        return self

    def consequencias(self):
        a = self.a
        self.p.append("## Consequências\n\n"
                      f"* **Positivas:** {'; '.join(a.positivas) or TBD}\n* **Negativas:** {'; '.join(a.negativas) or TBD}\n"
                      f"* **Riscos:** {'; '.join(a.riscos) or TBD}\n* **Impacto:** {a.impacto or TBD}\n"
                      f"* **Necessidade de revisão:** {a.revisao or TBD}")
        return self

    def rodape(self):
        a = self.a
        self.p.append(f"## Confirmação\n\n{a.confirmacao or TBD}\n\n## Links\n\n{self._l(a.links)}")
        notas = []
        if a.pendencias: notas.append("Pendências:\n" + "\n".join(f"- {x}" for x in a.pendencias))
        if a.conflitos: notas.append("Possíveis relações/conflitos com ADRs anteriores (avaliação humana):\n" + "\n".join(f"- {x}" for x in a.conflitos))
        if notas: self.p.append("<!--\n" + "\n\n".join(notas) + "\n-->")
        return self

    def build(self) -> str:
        return "\n\n".join(self.p) + "\n"


def montar_markdown(adr: ADR) -> str:
    return (ADRBuilder(adr).cabecalho().contexto().opcoes().resultado()
            .pros_contras().consequencias().rodape().build()).replace("\u2011", "-")


def validar_markdown(md: str) -> list[str]:
    erros = [f"Seção ausente: {s}" for s in SECOES if s not in md]
    m = re.search(r"\*\*Status:\*\*\s*(.+)", md)
    if not m or m.group(1).strip() not in STATUS:
        erros.append(f"Status inválido ou ausente (use: {', '.join(STATUS)})")
    return erros


def aplicar_status(md: str, novo: str, aprovador: str) -> str:
    m = re.search(r"(\*\*Status:\*\*\s*)(.+)", md)
    if not m: raise ValueError("ADR sem campo Status")
    atual = m.group(2).strip()
    if novo not in TRANSICOES.get(atual, set()):
        raise ValueError(f"Transição inválida: {atual} → {novo}")
    if not aprovador.strip(): raise ValueError("Informe o nome do responsável pela decisão")
    md = md[:m.start(2)] + novo + md[m.end(2):]
    return md.rstrip() + f"\n\n<!-- {novo} por {aprovador.strip()} em {date.today().isoformat()} -->\n"
