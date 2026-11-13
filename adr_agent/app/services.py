"""Aplicação: orquestra conversa e geração. Strategy para elaborar (revisar entra depois)."""
import json
import re
from . import repository as repo
from .domain import ADR, ADRDraft, montar_markdown

REGRAS = """Regras: use SOMENTE o que o usuário informou; nunca invente fatos, números, nomes, aprovações ou justificativas.
Alternativas que VOCÊ sugerir devem ser identificadas como sugestões da IA. Sempre inclua a opção 'não fazer nada / manter status quo'.
Informação ausente vira pendência. Compare com as ADRs anteriores e aponte relações ou conflitos possíveis (a decisão final é humana). Responda em português."""

SYSTEM_CHAT = f"""Você é um agente que ajuda uma equipe a documentar UMA decisão arquitetural em uma ADR.
A ADR terá: contexto e problema; fatores de decisão; opções (incluindo status quo); decisão escolhida e porquê; prós e contras; consequências (positivas, negativas, riscos, impacto, gatilho de revisão); confirmação; links; decisores/consultados/informados.
Conduza uma entrevista curta e objetiva: no máximo 3 perguntas numeradas por mensagem, priorizando o que falta, sem títulos, sem emojis e sem repetir o que o usuário já respondeu.
Use as ADRs anteriores para INFERIR fatos (tecnologias, pacotes, convenções) e peça confirmação, por exemplo: 'Pelo ADR-0031, entendi que X; está correto?', em vez de perguntar do zero.
Primeiro pergunte quais alternativas a equipe considerou. Só sugira alternativas se o usuário não tiver nenhuma, e diga que são sugestões suas. {REGRAS}
NUNCA escreva a ADR, tabelas ou resumo completo na conversa e use no máximo 120 palavras por mensagem. Quando já houver informação suficiente (problema, contexto, opções e decisão), diga em 1-2 frases o que ainda ficará pendente e termine com o marcador [PRONTO]. Só ADRs com status Aceito estão em vigor; Proposto ainda não foi aprovada. Se a nova decisão depender de uma ADR que não está Aceita, avise em uma frase.
ADRs anteriores:
"""

SYSTEM_GERAR = """Gere os campos de uma ADR a partir da conversa. Responda SOMENTE com um objeto JSON válido (sem markdown) conforme este JSON Schema:
{schema}
{regras}
Escreva com a concretude e o nível de detalhe das ADRs anteriores mais recentes: no campo detalhe use Markdown (subseções com ###, listas) para dizer exatamente o que será feito, os limites da decisão e os critérios de sucesso; em riscos use o formato 'risco → mitigação'; cite ADRs relacionadas pelo número (ex.: ADR-0031) em relacionados e use substitui só se uma ADR anterior for realmente substituída.
Obrigatório: titulo curto e descritivo da decisão, nunca vazio. Inclua em opcoes TODAS as alternativas que o usuário citou, inclusive as descartadas (diga na descrição que foi descartada e o motivo dado). Em detalhe use três subseções: ### O que será feito, ### Fora do escopo (o que o usuário disse que a decisão NÃO cobre) e ### Critérios de sucesso (os mensuráveis que o usuário citou). No contexto inclua a escala (número de usuários, plataformas) e as restrições citadas (prazo, tamanho e experiência do time). impacto = módulos, times e sistemas afetados, não o resultado esperado. Cada fator de decisão deve ser uma frase curta com as palavras do usuário. Em pros coloque só vantagens e em contras só desvantagens, sem repetir um item nos dois.
Consultados = quem foi ouvido ANTES da decisão ('consultamos'); informados = quem apenas será avisado depois ('serão avisados'); nunca troque. Inclua só UMA opção de status quo, mesmo que o usuário diga 'não fazer nada' e 'manter só senha'. Em relacionados coloque as ADRs e tickets citados (ADR-NNNN, EPS-NNN) e em links os tickets, documentos e URLs citados. Em positivas e negativas liste as consequências que o usuário mencionou (ex.: aumento de chamados de suporte é consequência negativa). Em confirmacao e nos critérios de sucesso use só métricas, rotinas e ferramentas que o usuário citou; nunca invente dashboards, alertas, ferramentas ou tendências.
O contexto deve explicar o problema e a motivação que o usuário citou (incidentes, pedidos, riscos), além do cenário atual e das restrições. Se uma frase diz 'consultamos A e B, e C será avisado', C é informado, não consultado. Uma opção que o usuário deixou como evolução futura deve ser registrada como 'evolução futura', não como descartada. Em pros e contras use só o que o usuário disse ou o que decorre diretamente disso; não acrescente atributos genéricos da tecnologia (ex.: 'entrega rápida', 'maior segurança') que ele não mencionou.
Só ADRs anteriores com status Aceito estão em vigor; Proposto ainda não foi aprovada; Rejeitado, Obsoleto e Substituído não valem. Use as ADRs anteriores apenas como contexto e para relações: não copie delas critérios, escopo, limites ou ações como se fossem desta decisão, a menos que o usuário os tenha repetido; cite-as por número. Em relacionados inclua SEMPRE as ADRs anteriores com as quais esta decisão se relaciona (ex.: ADR-0001) e em conflitos explique a relação (complementa, altera, substitui, contradiz) e se depende de ADR ainda não Aceita. Perguntas e exemplos feitos pelo agente no histórico NÃO são fatos: use só o que o usuário disse.
Se o usuário disser coisas contraditórias (prazos, tickets, decisores diferentes), não escolha em silêncio: use o dado mais recente e registre a divergência em pendencias. Não afirme ausência de restrições ('não há restrição de prazo') se o usuário não disse. A opção que mantém a situação atual (ex.: 'manter só o e-mail') já é o status quo: não crie outra. positivas = o que melhora com a decisão (em geral o problema que ela resolve, como o usuário descreveu); negativas = custos e trade-offs que o usuário mencionou ou aceitou.
Campos específicos: justificativa = UMA frase curta que completa 'Escolhida: <opção>, porque ...', começando em minúscula e sem ponto final. Escreva apenas o motivo, sem repetir as palavras 'Escolhida' nem 'porque'. confirmacao = como saber, na prática, que a decisão foi implementada e funciona (métricas, alertas, revisão), usando as metas que o usuário citou; deixe vazio só se ele não citou nenhuma.
Em pros, contras, riscos, mitigações, etapas e critérios inclua apenas o que o usuário disse. Todo item que você inferiu deve terminar com '(sugestão da IA)'. Não invente mitigações: se o usuário não citou uma, registre o risco e coloque a mitigação em pendencias.
ADRs anteriores:
{adrs}"""


def _enxuto(h):
    """Corta as respostas antigas do agente; a informação útil está nas mensagens do usuário."""
    return [{**m, "content": m["content"][:600]} if m["role"] == "assistant" else m for m in h]


def _adrs_txt(adrs, recente):
    """As 2 ADRs mais recentes entram quase completas (referência de estilo); as demais, resumidas."""
    sel = adrs[-15:]
    return "\n\n".join(f"### {a['arquivo']} [{a['status']}]\n{a['texto'][:recente if k >= len(sel) - 2 else 400]}"
                        for k, a in enumerate(sel)) or "(nenhuma)"


def _compacto(o):
    """Remove title/default do JSON Schema para gastar menos tokens."""
    if isinstance(o, dict): return {k: _compacto(v) for k, v in o.items() if k not in ("title", "default")}
    if isinstance(o, list): return [_compacto(v) for v in o]
    return o


def _pendencias_relacoes(adr, adrs):
    """Regra no código: ADR citada precisa existir na pasta e estar Aceita para estar em vigor."""
    por_num = {int(m.group(1)): a for a in adrs if (m := re.match(r"ADR-(\d+)", a["arquivo"]))}
    refs = sorted({int(n) for n in re.findall(r"ADR-(\d+)", " ".join(adr.relacionados + [adr.substitui]).replace("\u2011", "-"))})
    out = []
    for n in refs:
        a = por_num.get(n)
        if not a: out.append(f"ADR-{n:04d} citada, mas não encontrada na pasta de ADRs")
        elif a["status"] != "Aceito": out.append(f"ADR-{n:04d} está {a['status']}: esta ADR depende de uma decisão que ainda não está em vigor")
    return out


class ElaborarStrategy:
    def prompt(self, adrs: list[dict]) -> str:
        return SYSTEM_GERAR.format(schema=json.dumps(_compacto(ADRDraft.model_json_schema()), ensure_ascii=False, separators=(",", ":")),
                                   regras=REGRAS, adrs=_adrs_txt(adrs, 3500))


ESTRATEGIAS = {"elaborar": ElaborarStrategy()}


async def conversar(llm, historico, pasta):
    r = await llm.complete(SYSTEM_CHAT + _adrs_txt(repo.listar(pasta), 3500), _enxuto(historico))
    return r.replace("[PRONTO]", "").strip(), "[PRONTO]" in r


async def gerar(llm, historico, pasta, modo="elaborar"):
    adrs = repo.listar(pasta)
    sistema = ESTRATEGIAS[modo].prompt(adrs)
    msgs = _enxuto(historico) + [{"role": "user", "content": "Gere agora a ADR em JSON, com base apenas na conversa."}]
    erro = None
    for _ in range(2):
        if erro: msgs.append({"role": "user", "content": f"JSON inválido ({erro}). Responda só com o JSON corrigido."})
        txt = await llm.complete(sistema, msgs)
        try:
            draft = ADRDraft.model_validate_json(txt[txt.index("{"): txt.rindex("}") + 1])
            break
        except ValueError as e:  # inclui ValidationError do Pydantic
            erro = str(e)[:300]
            msgs.append({"role": "assistant", "content": "(resposta anterior inválida)"})
    else:
        raise ValueError("O modelo não devolveu uma ADR válida. Tente novamente; a conversa foi preservada.")
    adr = ADR(numero=repo.proximo_numero(pasta), **draft.model_dump())
    adr.pendencias = list(dict.fromkeys(adr.pendencias + adr.pendencias_estruturais() + _pendencias_relacoes(adr, adrs)))
    return {"arquivo": repo.nome_arquivo(adr.numero, adr.titulo), "markdown": montar_markdown(adr),
            "pendencias": adr.pendencias, "conflitos": adr.conflitos}
