# Agente de ADR — AEP8S

Agente de IA que ajuda uma equipe de software a registrar **decisões arquiteturais** em ADRs (*Architecture Decision Records*). O usuário conversa com o agente sobre a decisão, o agente pergunta o que falta e gera um rascunho de ADR em Markdown, no modelo da equipe, para revisão humana.

O agente **não aprova decisões**: toda ADR gerada sai com status **Proposto**, e aceitar ou rejeitar é sempre uma ação de uma pessoa da equipe.

Projeto acadêmico (AEP) relacionado à **ODS 9 — Indústria, Inovação e Infraestrutura**: preservar o conhecimento técnico sobre as escolhas de arquitetura apoia a manutenção e a evolução do software.

## Sumário

- [Funcionalidades](#funcionalidades)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Requisitos](#requisitos)
- [Instalação e execução](#instalação-e-execução)
- [Como usar](#como-usar)
- [Configuração do modelo de IA](#configuração-do-modelo-de-ia)
- [Arquitetura](#arquitetura)
- [Regras garantidas pelo código](#regras-garantidas-pelo-código)
- [Testes](#testes)
- [Limitações conhecidas](#limitações-conhecidas)
- [Diferenças em relação à especificação](#diferenças-em-relação-à-especificação)
- [Equipe](#equipe)

## Funcionalidades

- Lê uma pasta de ADRs existentes (`.md`) e usa essas ADRs como contexto da nova decisão.
- Conduz uma entrevista curta (até 3 perguntas por mensagem) até ter informação suficiente.
- Gera a ADR com todas as seções do modelo: Contexto e problema, Fatores de decisão, Opções consideradas, Resultado da decisão, Prós e contras, Consequências, Confirmação e Links.
- Marca como **sugestão da IA** o que não foi dito pelo usuário e transforma informação ausente em **pendência**.
- Aponta relações com ADRs anteriores e avisa quando a ADR citada ainda não está Aceita.
- Salva o rascunho revisado na pasta, **sem nunca sobrescrever** uma ADR existente.
- Permite aprovar ou rejeitar uma ADR Proposta, registrando quem decidiu e quando.
- Funciona com vários provedores de IA: Groq, Google Gemini, OpenAI, Anthropic e Ollama (local).

## Estrutura do repositório

```
AEP8S_Agente-ADR/
├── adr_agent/                         # código do agente
│   ├── app/
│   │   ├── main.py                    # Controller: endpoints da API (FastAPI)
│   │   ├── services.py                # Aplicação: conversa, geração e prompts
│   │   ├── domain.py                  # Domínio: entidade ADR, Builder do Markdown, regras de status
│   │   ├── repository.py              # Infraestrutura: leitura e gravação dos arquivos .md
│   │   └── llm.py                     # Infraestrutura: Adapter para os provedores de IA
│   ├── static/index.html              # View: interface no navegador
│   ├── adrs/ADR-0000 - Modelo.md      # modelo de ADR da equipe
│   └── requirements.txt
├── Especificação do Agente_ADR/       # especificação do agente (.md e .pdf)
└── AEP-TESTE/                         # registro de testes (.md e .pdf)
```

## Requisitos

- **Python 3.13 ou mais recente.** Os testes foram feitos com Python 3.15, mas por ser muito recente pode faltar pacote pronto; se a instalação falhar, use o 3.13.
- **Uma chave de API** de um provedor de IA. A equipe usa o **Groq** (plano gratuito), com o modelo `openai/gpt-oss-120b`. A chave pode ser criada em [console.groq.com](https://console.groq.com).
- Navegador web.

## Instalação e execução

### Windows (CMD ou PowerShell)

```bat
git clone https://github.com/007f/AEP8S_Agente-ADR.git
cd AEP8S_Agente-ADR\adr_agent
py -m pip install -r requirements.txt
py -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

> Use `py -m pip` e `py -m uvicorn`. Se aparecer *"pip não é reconhecido"*, o Python não está no PATH: reinstale marcando a opção *Add Python to PATH*. Se aparecer *"No module named uvicorn"*, faltou o passo do `pip install`.

### Linux / macOS

```bash
git clone https://github.com/007f/AEP8S_Agente-ADR.git
cd AEP8S_Agente-ADR/adr_agent
python3 -m pip install -r requirements.txt
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Com o servidor rodando, abra **http://127.0.0.1:8000** no navegador. Para parar o servidor, use `Ctrl+C` no terminal.

> O servidor deve ser iniciado **dentro da pasta `adr_agent`**: o caminho `./adrs` informado na interface é relativo a ela.

## Como usar

1. **Configure o provedor.** No topo da página, escolha o provedor (ex.: *Groq*), confira o modelo (`openai/gpt-oss-120b`) e cole a chave de API. A chave não é gravada em disco; ela é enviada apenas nas chamadas ao provedor.
2. **Carregue a pasta.** Informe a pasta das ADRs (padrão `./adrs`) e clique em **Carregar pasta**. As ADRs existentes aparecem na coluna da esquerda, com o status de cada uma.
3. **Converse.** Clique em **Nova conversa** e descreva a decisão: o problema, o contexto, as alternativas consideradas, a escolhida e o porquê, quem decide, quem foi consultado e quem só será informado. `Ctrl+Enter` envia a mensagem.
4. **Gere o rascunho.** Quando o agente indicar que há informação suficiente, clique em **Gerar ADR**. No Groq gratuito, espere cerca de **1 minuto** antes de gerar (veja [Configuração do modelo de IA](#configuração-do-modelo-de-ia)).
5. **Revise.** O rascunho aparece à direita, editável, com as pendências acima dele. Corrija o que o modelo inventou ou entendeu errado. Itens marcados como *sugestão da IA* devem ser confirmados ou removidos pela equipe.
6. **Salve.** Clique em **Salvar na pasta (status Proposto)**. O nome do arquivo é gerado a partir do número e do título, por exemplo `ADR-0002-rodar-testes-principais-no-gemini.md`.
7. **Aprove ou rejeite.** Na lista, clique em **Aprovar / Rejeitar** na ADR Proposta, informe o nome do responsável e responda à pergunta: **OK = Aceito** e **Cancelar = Rejeitado**. O sistema grava no arquivo um comentário como `<!-- Aceito por Felipe em 2026-11-13 -->`.

As pendências e as possíveis relações com outras ADRs ficam num comentário HTML (`<!-- ... -->`) no fim do arquivo salvo.

## Configuração do modelo de IA

| Provedor | Modelo padrão na interface | Observação |
|---|---|---|
| Groq | `openai/gpt-oss-120b` | Recomendado pela equipe: gratuito e rápido |
| Google Gemini | `gemini-3.8-flash` | Gratuito, mas instável nos testes (erros 503 e tempo esgotado) |
| OpenAI | `gpt-4o` | Exige crédito pago na API |
| Anthropic | `claude-sonnet-5-5` | Exige crédito pago na API |
| Ollama (local) | `llama3.1` | Não usa chave; precisa do Ollama rodando em `localhost:11434` |

O campo do modelo é editável: se o provedor aposentar um modelo, basta digitar o nome novo.

**Limite do Groq gratuito.** O plano gratuito permite cerca de 8.000 tokens por minuto. A geração da ADR é um pedido grande, então espere cerca de 1 minuto depois da conversa antes de clicar em **Gerar ADR**. Se o limite for atingido, o agente espera o tempo indicado pelo Groq e tenta de novo automaticamente.

**Nível de raciocínio (`GROQ_REASONING`).** Com o `gpt-oss` no Groq, a variável de ambiente `GROQ_REASONING` controla quanto o modelo "pensa" antes de responder: `low` (padrão, gasta menos tokens), `medium` ou `high`. Defina a variável **no mesmo terminal** e depois inicie o servidor:

| Terminal | Comando |
|---|---|
| CMD | `set GROQ_REASONING=medium` |
| PowerShell | `$env:GROQ_REASONING="medium"` |
| Linux / macOS | `export GROQ_REASONING=medium` |

Nos testes, `medium` melhorou a marcação das sugestões e a seção Confirmação, mas não eliminou invenções (teste T25).

## Arquitetura

Arquitetura em camadas com MVC, conforme a especificação:

```
Navegador (static/index.html)          View
        │  HTTP / JSON
main.py — endpoints FastAPI            Controller
        │
services.py — conversa e geração       Aplicação (Strategy)
        │                 │
domain.py — ADR e regras  llm.py — provedores de IA   Domínio / Infraestrutura (Adapter)
        │
repository.py — arquivos .md           Infraestrutura
```

| Padrão | Onde | Para quê |
|---|---|---|
| Builder (GoF) | `ADRBuilder` em `domain.py` | Monta o Markdown seção a seção, exatamente no modelo da equipe |
| Adapter (GoF) | `llm.py` | Uma interface interna única (`complete`) para Anthropic e para os provedores compatíveis com a API da OpenAI (OpenAI, Gemini, Groq, Ollama) |
| Strategy (GoF) | `ElaborarStrategy` em `services.py` | Encapsula o modo de operação; hoje há a elaboração de ADR nova (a revisão está prevista) |
| Information Expert (GRASP) | entidade `ADR` em `domain.py` | A própria ADR verifica suas pendências estruturais e as transições de status |
| MVC | `index.html` / `main.py` / `domain.py` | O Controller só recebe e repassa; não monta prompts nem aprova decisões |

### API

| Método | Endpoint | Função |
|---|---|---|
| GET | `/api/adrs?dir=<pasta>` | Lista as ADRs da pasta com título e status |
| POST | `/api/chat` | Envia a conversa e recebe a próxima resposta do agente |
| POST | `/api/generate` | Gera o rascunho da ADR a partir da conversa |
| POST | `/api/save` | Valida as seções e salva o arquivo (recusa sobrescrever) |
| POST | `/api/status` | Muda o status de uma ADR, respeitando as transições permitidas |

## Regras garantidas pelo código

Estas regras não dependem do modelo de IA:

- Título obrigatório; se o modelo devolver JSON inválido, o agente pede a correção uma vez antes de mostrar o erro.
- Toda ADR nova sai com status **Proposto**.
- Pendências automáticas para campos vazios: decisores, consultados, informados, fatores de decisão, consequências positivas e negativas, riscos, impacto e confirmação; também para menos de duas opções, falta da opção *status quo*, mais de uma opção de *status quo* e opção escolhida que não está na lista.
- ADR citada que não existe na pasta ou que ainda não está **Aceita** gera a pendência *"ADR-NNNN está Proposto: esta ADR depende de uma decisão que ainda não está em vigor"*.
- Ao salvar, o sistema confere as seções obrigatórias e o status, e **nunca sobrescreve** um arquivo existente.
- Transições de status permitidas:

| Status atual | Pode ir para |
|---|---|
| Proposto | Aceito ou Rejeitado |
| Aceito | Obsoleto ou Substituído |
| Rejeitado, Obsoleto, Substituído | nenhum (estados finais) |

Qualquer outra mudança é recusada com o erro `Transição inválida: <atual> → <novo>`, inclusive quando a API é chamada diretamente, sem a interface (teste T24).

## Testes

O registro completo está em [`AEP-TESTE/Registro de Testes - Agente de ADR.md`](<AEP-TESTE/Registro de Testes - Agente de ADR.md>) (também em PDF). São 27 testes (T01 a T27), cada um com quatro campos: **Modelo**, **Como foi testado**, **Resultado** e **Crítica**.

Resumo:

- **Funções do sistema:** salvar, bloquear sobrescrita, aprovar, rejeitar e recusar transições inválidas foram aprovados (T14, T15, T22, T23 e T24).
- **Relação entre ADRs:** a pendência aparece quando a ADR citada está Proposta e não aparece quando está Aceita (T21 e T26).
- **Qualidade do conteúdo:** depende do modelo e da revisão humana. Os rascunhos com o Groq foram, em geral, *aprovados com ressalvas*.
- **Gemini:** instável; no T27 não conseguiu gerar a ADR nem fora da rede da faculdade.

## Limitações conhecidas

- **O modelo de IA pode inventar detalhes** plausíveis (ferramentas, critérios, equipes) sem marcá-los como sugestão. A revisão humana antes de salvar é obrigatória.
- Respostas de LLM variam: a mesma conversa pode gerar ADRs diferentes.
- Erros recorrentes observados: consequências ou *Necessidade de revisão* em branco, justificativa reescrita, troca de consultados e informados, contradições resolvidas em silêncio e *status quo* duplicado com nomes diferentes (a checagem automática só reconhece o termo "status quo" no nome da opção).
- Falhas de rede e tempo esgotado (limite fixo de 180 segundos) não são repetidas automaticamente; só erros 5xx e 429 são.
- O comentário de pendências não é atualizado quando o rascunho é editado à mão.
- A aprovação é permitida mesmo com campos `[A definir]` no texto.
- Não há autenticação: o servidor foi feito para rodar só em `127.0.0.1`, na máquina do usuário.
- Ainda não é possível editar uma ADR já salva pela interface.
- Ao atualizar o agente, **não substitua a pasta `adrs` inteira**, para não apagar ADRs salvas.

## Diferenças em relação à especificação

O protótipo implementa o fluxo principal da especificação, com algumas simplificações:

| Especificação | Protótipo |
|---|---|
| Interface em React | Página HTML com JavaScript puro (`static/index.html`) |
| Persistência em PostgreSQL, com versões | Arquivos `.md` numa pasta; o histórico pode ser mantido com Git |
| Estratégias de elaborar e revisar ADR | Só a elaboração está implementada; a revisão está prevista |

## Equipe

- Erick Oliveira de Souza
- Helder Augusto Kusagari Fukita
- Andrei Luiz Silva
- Felipe Saueressig Mello

A especificação completa do agente está em [`Especificação do Agente_ADR`](<Especificação do Agente_ADR/Especificação do Agente_ ADR.md>).
