# 

| Nome | R.A. |
| :---- | :---- |
| **Felipe Saueressig Mello** | **23167656-2** |
| **Erick Oliveira de souza**  | **23223824-2** |
| **Helder Augusto Kusagari Fukita** | **23197574-2** |
| **Andrei Luiz Silva**  | **23087472-2** |

# **Registro de Testes \- Agente de ADR**

Nov 13, 2026 · Felipe Saueressig Mello

Projeto: agente de IA para desenvolvimento de ADRs

Link Repositorio: [https\://github.com/007f/AEP8S\_Agente-ADR](https://github.com/007f/AEP8S_Agente-ADR). 

## **1\. Objetivo e ambiente**

Este documento registra os testes realizados no Agente de ADR: uma aplicação local (servidor FastAPI em 127.0.0.1:8000, interface no navegador) que lê uma pasta de ADRs em Markdown, conversa com o usuário sobre a decisão e gera o arquivo da ADR no modelo da equipe, usando a chave de API de um LLM externo informada pelo próprio usuário.

Cada teste tem quatro campos obrigatórios: **Modelo** (o LLM usado, ou “Não se aplica” quando o teste não chama LLM), **Como foi testado**, **Resultado** e **Crítica**.

Escala de resultado: **Aprovado** (sem falhas relevantes); **Aprovado com ressalvas** (falhas que a revisão humana corrige antes de salvar); **Reprovado** (falha que impede o uso ou perde informação importante); **Inconclusivo** (teste inválido ou incompleto); **Pendente** (ainda não executado).

Observações: as respostas de um LLM variam de uma execução para outra, então a mesma conversa pode gerar ADRs diferentes; todos os dados dos roteiros são fictícios; a avaliação do professor, relatada pela equipe, foi de que o sistema está bom o bastante e que a qualidade final passa a depender do modelo de IA e do usuário.

Critério para sugestões do modelo (a partir do T21): um professor avaliador informou que, como o sistema permite ao usuário editar a ADR antes de salvar e de aprovar, é aceitável que partes do rascunho sejam sugestões do modelo, **desde que estejam marcadas como sugestão**. Item inferido sem marcação, papéis trocados, conteúdo copiado de outra ADR e marcação no item errado continuam contando como falha.

Modelos que efetivamente geraram conteúdo: Groq, openai/gpt-oss-120b (em todos os testes com Groq) e Google Gemini, gemini-3.8-flash (modelo gratuito, o único do Gemini usado). OpenAI, Anthropic, gemini-2.5-flash e llama-3.3-70b-versatile não chegaram a gerar conteúdo (T01, T02 e T04).

A partir do T21, a sequência de testes roda sem nenhuma alteração de código, para que as comparações valham, em Windows com Python 3.15, Groq openai/gpt-oss-120b com raciocínio low e a pasta ./adrs. As ADRs criadas são removidas da pasta após cada teste para não influenciar o seguinte, então a numeração pode recomeçar. ADR-A e ADR-B são rótulos internos de análise, não números de arquivo.

## **2\. Roteiros**

### **2.1 Roteiro padrão (ADR de PIN por e-mail)**

Três mensagens enviadas em sequência, com a pasta de ADRs sem outras decisões: (1) contexto e problema: login só com e-mail e senha, compartilhamento de senhas, incidente de notas alteradas, cerca de 1.200 usuários, prazo de 6 semanas, time de 5 pessoas; (2) alternativas: manter só senha, PIN por SMS, PIN por e-mail, TOTP descartado, preferência pelo e-mail e fatores de decisão; (3) detalhes: PIN de 6 dígitos válido por 10 minutos, bloqueio após 5 tentativas, BFF (ADR-0021), riscos e mitigações, decisores, consultados e informados, metas de sucesso, revisão em 3 meses e ticket EPS-600.

### **2.2 Roteiro de relação entre ADRs (escolha do modelo de IA)**

**ADR-A** (escolha do modelo de IA para os testes; salva como ADR-0001 e revisada por humano), três mensagens:

1. “Preciso registrar a escolha do modelo de IA que a gente vai usar pra testar o agente de ADR. Hoje cada teste usa um modelo diferente e fica difícil comparar. Na faculdade o firewall deixa o Gemini bem lento, e a OpenAI e a Anthropic pedem crédito que a gente não tem.”  
2. “Olhamos quatro caminhos: o Gemini 3.8 Flash grátis, o Groq com o gpt-oss-120b, um modelo local no Ollama ou pagar crédito na OpenAI. Vamos de Groq com o gpt-oss-120b, porque é grátis e responde rápido até na rede da faculdade. O Ollama a gente deixa pra depois. O ruim é o limite de 8 mil tokens por minuto.”  
3. “Pra dar certo, 9 de cada 10 gerações têm que sair com JSON válido. O risco é bater no limite e travar, então a gente espera 1 minuto entre uma geração e outra. Quem decide é o grupo, o professor foi consultado e os outros colegas só ficam sabendo. Revisamos se o Groq tirar esse modelo ou se a gente trocar de rede. Ticket TST-12.”

**ADR-B** (decisão ligada à ADR-A), duas mensagens em uma nova conversa:

1. “Quero registrar uma decisão ligada à anterior: quando a gente estiver em casa, sem o firewall da faculdade, vai rodar os testes também no Gemini 3.8 Flash grátis, só pra comparar com o Groq. Testar em um modelo só pode esconder problema.”  
2. “Pensamos em três jeitos: continuar só com o Groq, rodar tudo nos dois ou rodar nos dois só os testes principais. Vamos rodar só os principais, porque o Gemini grátis também tem limite e é mais lento. O grupo decide e o professor será avisado. Revisamos daqui a um mês. Ticket TST-15.”

## **3\. Resumo dos resultados**

| ID | Teste | Modelo | Resultado |
| :---- | :---- | :---- | :---- |
| T01 | Chaves OpenAI e Anthropic | OpenAI e Anthropic | Reprovado (causa externa) |
| T02 | Gemini 2.5 Flash | gemini-2.5-flash | Reprovado (modelo aposentado) |
| T03 | Gemini 3.8 Flash | gemini-3.8-flash (gratuito) | Aprovado com ressalvas |
| T04 | Groq Llama 3.3 | llama-3.3-70b-versatile | Reprovado (modelo inexistente) |
| T05 | Conversa com ADR existente | Groq gpt-oss-120b | Aprovado com ressalvas |
| T06 | Informações complexas e conflitantes | gemini-3.8-flash e Groq gpt-oss-120b | Aprovado (relato da equipe) |
| T07 | Geração, rodada 1 | Groq gpt-oss-120b | Aprovado com ressalvas |
| T08 | Geração, rodada 2 | Groq gpt-oss-120b | Aprovado com ressalvas |
| T09 | Geração, rodada 3 | Groq gpt-oss-120b | Aprovado com ressalvas |
| T10 | Geração, rodada 4 | Groq gpt-oss-120b | Reprovado |
| T11 | Geração, rodada 5 | Groq gpt-oss-120b | Aprovado com ressalvas |
| T12 | Geração, rodada 6 | Groq gpt-oss-120b | Aprovado com ressalvas |
| T13 | Geração, rodada 7 | Groq gpt-oss-120b | Aprovado com ressalvas |
| T14 | Salvar ADR | Não se aplica | Aprovado |
| T15 | Bloqueio de sobrescrita | Não se aplica | Aprovado |
| T16 | Aprovar ADR | Não se aplica | Aprovado com ressalvas |
| T17 | Relação entre ADRs, 1ª execução | Groq gpt-oss-120b | Reprovado |
| T18 | Relação entre ADRs, 2ª execução | Groq gpt-oss-120b | Inconclusivo |
| T19 | Testes de código | Não se aplica | Aprovado |
| T20 | Instalação no Windows | Não se aplica | Aprovado após ajustes |
| T21 | Relação entre ADRs com ADR Aceita (ADR-A e ADR-B) | Groq gpt-oss-120b | Aprovado com ressalvas |
| T22 | Aprovar ADR (reteste) | Não se aplica | Aprovado |
| T23 | Rejeitar ADR | Não se aplica | Aprovado |
| T24 | Transição inválida pela API | Não se aplica | Aprovado |
| T25 | Raciocínio médio x baixo (ADR-A) | Groq gpt-oss-120b, raciocínio medium | Aprovado com ressalvas |
| T26 | Relação entre ADRs com ADR citada Proposta | Groq gpt-oss-120b, raciocínio low | Aprovado com ressalvas |
| T27 | Gemini fora da rede da faculdade (ADR-A) | gemini-3.8-flash (gratuito) | Reprovado (causa externa) |

## **4\. Testes detalhados**

### **T01 — Chaves OpenAI e Anthropic**

**Modelo:** OpenAI e Anthropic (Claude), com o modelo padrão do campo em cada caso.

**Como foi testado:** chave de API da conta informada na página e envio da mensagem inicial da conversa.

**Resultado:** Reprovado por causa externa. A OpenAI devolveu erro 429 insufficient\_quota (conta sem créditos) e a Anthropic apresentou o mesmo problema de saldo (relato da equipe). O agente exibiu o erro e preservou a mensagem digitada.

**Crítica:** o tratamento de erro funcionou, mas o teste não avalia a qualidade dos modelos. A API paga exige crédito próprio, diferente de uma assinatura de chat. Esses dois provedores ficaram sem avaliação de conteúdo.

### **T02 — Gemini 2.5 Flash**

**Modelo:** Google Gemini, gemini-2.5-flash.

**Como foi testado:** chave do Google AI Studio e envio da mensagem inicial.

**Resultado:** Reprovado. A API retornou 404 informando que o modelo não está mais disponível para novos usuários e indicou o substituto gemini-3.8-flash. A troca no campo de modelo resolveu, e o padrão do projeto foi atualizado.

**Crítica:** nomes de modelos envelhecem rápido. O campo editável e a mensagem da própria API permitiram corrigir sem alterar o código, mas o usuário precisa saber o nome atual. Melhoria possível: listar os modelos disponíveis do provedor.

### **T03 — Gemini 3.8 Flash**

**Modelo:** Google Gemini, gemini-3.8-flash (modelo gratuito).

**Como foi testado:** várias conversas e gerações de ADR. Após os primeiros erros, foi adicionada repetição automática (até 3 novas tentativas, com espera de 2, 5 e 10 segundos) para falhas 500, 502, 503 e 504\.

**Resultado:** Aprovado com ressalvas. Quando respondia, a qualidade foi considerada boa pela equipe. Porém ocorreram erros 503 de alta demanda várias vezes, e em parte das tentativas as repetições se esgotaram sem sucesso.

**Crítica:** a instabilidade vem do provedor e não do agente. A repetição reduz o problema, mas não o elimina. A saída prática foi alternar para outro provedor. As saídas geradas por esse modelo não foram anexadas a este registro.

### **T04 — Groq Llama 3.3**

**Modelo:** Groq, llama-3.3-70b-versatile.

**Como foi testado:** chave do Groq e envio da mensagem inicial.

**Resultado:** Reprovado. A API retornou 404 model\_not\_found. O modelo foi trocado por openai/gpt-oss-120b, nome encontrado em um artigo de terceiros de agosto de 2026 que lista os modelos em produção do Groq.

**Crítica:** mesmo problema do T02. Como a fonte do nome novo era de terceiros, o ideal é confirmar na página oficial de modelos do Groq.

### **T05 — Conversa com ADR existente na pasta**

**Modelo:** Groq, openai/gpt-oss-120b.

**Como foi testado:** pasta com a ADR-0031 (reestruturação do front-end). Primeiro prompt: “preciso fazer uma ADR sobre a separação dos componentes entre front web e mobile”, seguido de uma conversa de acompanhamento.

**Resultado:** Aprovado com ressalvas. O agente leu a pasta, perguntou na ordem do modelo (contexto, fatores de decisão, decisores), tratou o que faltava como pendência e não inventou fatos. Na continuação usou a ADR-0031 como contexto, mas fez perguntas demais, com títulos e emojis, e perguntou coisas que poderia inferir da própria ADR (por exemplo, que o @repo/ui concentra os componentes web).

**Crítica:** o prompt foi ajustado: no máximo 3 perguntas numeradas, sem títulos ou emojis, inferir fatos das ADRs anteriores e pedir confirmação. As duas ADRs mais recentes passaram a entrar quase completas no prompt, como referência de estilo.

### **T06 — Informações complexas, conflitantes e faltantes**

**Modelo:** Google Gemini, gemini-3.8-flash (gratuito), e Groq, openai/gpt-oss-120b.

**Como foi testado:** conversas com informações extensas, contraditórias ou incompletas, para observar como o agente as interpreta.

**Resultado:** Aprovado, segundo a avaliação da equipe, que considerou as respostas satisfatórias. As exceções foram indisponibilidades temporárias do servidor do provedor.

**Crítica:** as conversas e os rascunhos desse teste não estão anexados a este registro e devem ser incluídos como evidência. Em teste posterior (T18) o agente resolveu uma contradição em silêncio, o que levou a um ajuste de prompt.

### **T07 — Geração de ADR, rodada 1 (versão inicial)**

**Modelo:** Groq, openai/gpt-oss-120b.

**Como foi testado:** roteiro padrão de 3 mensagens e clique em Gerar ADR.

**Resultado:** Aprovado com ressalvas. Estrutura completa, status Proposto, opção de status quo, TOTP descartado e decisores como cargos, sem nomes inventados. Falhas: mitigação inventada (“Treinamento pré-lançamento e FAQ”), inferências apresentadas como fato, Confirmação em branco apesar de metas informadas, justificativa com várias frases, hífens especiais em “e-mail” e uma pendência incorreta.

**Crítica:** o agente organiza bem, mas inventa detalhes plausíveis, e por isso a revisão humana é indispensável. Foram criadas regras para não inventar, marcar sugestões da IA, normalizar a justificativa e trocar os hífens. O rascunho foi editado e salvo.

### **T08 — Geração de ADR, rodada 2**

**Modelo:** Groq, openai/gpt-oss-120b.

**Como foi testado:** mesmo roteiro, com a versão corrigida da rodada 1\.

**Resultado:** Aprovado com ressalvas. Melhoraram a justificativa, os hífens, a Confirmação e a ausência de mitigação inventada. Novas falhas: título vazio, TOTP ausente, escopo (“Fora do escopo”) ausente e uma desvantagem do SMS listada como vantagem. Também ocorreu erro 429 do Groq (limite de 8.000 tokens por minuto; o pedido tinha 5.372 tokens).

**Crítica:** corrigir um problema abriu outros. Foram adicionados título obrigatório com nova tentativa automática, regras para incluir opções descartadas e escopo, e um esquema de geração mais compacto (de 2.396 para 1.329 caracteres).

### **T09 — Geração de ADR, rodada 3**

**Modelo:** Groq, openai/gpt-oss-120b.

**Como foi testado:** mesmo roteiro, com as correções da rodada 2\.

**Resultado:** Aprovado com ressalvas. Título correto, TOTP descartado com os motivos, escopo presente, Confirmação preenchida e sem mitigação inventada. Falhas: justificativa duplicada (“porque escolhida: PIN por e-mail, porque...”), escala (1.200 usuários, maioria mobile) ausente do Contexto, Impacto descrito como resultado esperado e não como módulos e times afetados, atributos do SMS sem base no que foi dito e pendências que eram ideias do modelo. Salvo como ADR-0001-implementar-segundo-fator-via-pin-por-email.md.

**Crítica:** os fatores de decisão curtos eram fiéis às palavras do usuário, então não eram defeito. A justificativa duplicada foi uma regressão do próprio prompt, corrigida no código.

### **T10 — Geração de ADR, rodada 4**

**Modelo:** Groq, openai/gpt-oss-120b.

**Como foi testado:** mesmo roteiro, com repetidas tentativas de Gerar ADR.

**Resultado:** Reprovado. O chat escreveu a ADR inteira na conversa, em vez de uma resposta curta com o marcador de pronto, e afirmou coisas sem base (professores consultados, ausência de pendências). Gerar ADR falhou seis vezes seguidas com erro 429, pelo limite de 8.000 tokens por minuto do plano gratuito do Groq (pedidos entre 4.901 e 6.981 tokens).

**Crítica:** causas: histórico de conversa inflado e modelo de raciocínio que consome tokens ao pensar. Correções: proibir ADR completa no chat (até 120 palavras), cortar respostas antigas do agente em 600 caracteres, usar raciocínio baixo no gpt-oss, não reenviar o JSON inválido na nova tentativa e esperar e repetir em 429 por limite de uso. Na prática, é preciso esperar cerca de 1 minuto antes de gerar.

### **T11 — Geração de ADR, rodada 5**

**Modelo:** Groq, openai/gpt-oss-120b, com raciocínio baixo.

**Como foi testado:** mesmo roteiro, após as correções do T10.

**Resultado:** Aprovado com ressalvas. Sem erro de limite. Falhas: Professores como Consultados e Informados em branco, duas opções de status quo, Consequências positivas e negativas em branco sem pendência registrada, dashboard e alertas inventados na Confirmação e ticket EPS-600 ausente.

**Crítica:** a economia de tokens coincidiu com queda de qualidade, e como duas mudanças foram feitas juntas (raciocínio baixo e histórico cortado) não dá para atribuir a causa com certeza. Foram criadas a variável GROQ\_REASONING, para comparar níveis de raciocínio, e checagens no código que geram pendências para campos vazios e status quo duplicado.

### **T12 — Geração de ADR, rodada 6**

**Modelo:** Groq, openai/gpt-oss-120b, com raciocínio padrão (baixo).

**Como foi testado:** mesmo roteiro, com as novas pendências e regras de prompt.

**Resultado:** Aprovado com ressalvas. Acertos: professores em Informados, ADR-0021 e EPS-600 em Relacionados, uma só opção de status quo, TOTP presente e Confirmação sem invenções. Falhas: time de produto em Consultados (deveria ser Informado), o problema (compartilhamento de senhas e incidente) ausente do Contexto, SMS tratado como descartado em vez de evolução futura e atributos genéricos sem marcação.

**Crítica:** foi o melhor rascunho até então. Como o modelo varia entre execuções, a equipe optou por parar de ajustar o prompt por rendimento decrescente e manter a revisão humana como proteção final.

### **T13 — Geração de ADR, rodada 7**

**Modelo:** Groq, openai/gpt-oss-120b, com raciocínio padrão.

**Como foi testado:** mesmo roteiro, após reforço do prompt (contexto com o problema, consultados e informados, evolução futura).

**Resultado:** Aprovado com ressalvas. Consultados e Informados corretos, incidente no Contexto e bloco de pendências gerado automaticamente. Falhas: Consequências positivas e negativas em branco (3ª vez), “relatórios de login” inventado, atributos do SMS sem base e compartilhamento de senhas fora do Contexto. Foi salva e depois aprovada (T14 a T16).

**Crítica:** as pendências automáticas funcionaram como rede de segurança. O modelo continua deixando consequências em branco, o que levou à revisão da instrução sobre positivas e negativas.

### **T14 — Salvar ADR na pasta**

**Modelo:** Não se aplica (função do sistema, sem chamada ao LLM).

**Como foi testado:** clique em Salvar após revisar e editar o rascunho no painel.

**Resultado:** Aprovado. O arquivo foi gravado com nome derivado do título (ADR-0001-implementar-pin-por-email-como-segunda-etapa-de-login.md) e conteúdo igual ao do painel, incluindo as edições manuais.

**Crítica:** o comentário de pendências não se atualiza quando o usuário edita o texto e fica como foi gerado. O salvamento valida as seções do modelo e o status.

### **T15 — Bloqueio de sobrescrita**

**Modelo:** Não se aplica.

**Como foi testado:** tentativa de salvar de novo uma ADR com nome já existente na pasta.

**Resultado:** Aprovado. O sistema bloqueou a operação e não alterou o arquivo existente.

**Crítica:** comportamento esperado e importante para proteger o histórico de decisões. Ainda não há edição de ADR existente, que está planejada.

### **T16 — Aprovar ADR**

**Modelo:** Não se aplica.

**Como foi testado:** botão Aprovar na lista de ADRs com status Proposto, informando o nome do responsável.

**Resultado:** Aprovado com ressalvas. A aprovação funcionou: o status mudou e foi registrado um comentário com nome e data.

**Crítica:** o sistema deixou aprovar uma ADR que ainda tinha campos em branco e pendências. Recomendação: bloquear a aprovação enquanto houver “\[A definir\]”, mantendo a rejeição liberada; a decisão ainda cabe à equipe. Rejeitar e a transição inválida (aprovar ADR já aceita) não foram testados.

### **T17 — Relação entre ADRs, 1ª execução**

**Modelo:** Groq, openai/gpt-oss-120b.

**Como foi testado:** ADR-0001 salva com status Proposto na pasta; duas mensagens sobre adicionar SMS como segundo canal do PIN (ticket EPS-640).

**Resultado:** Reprovado. A ADR-0001 não apareceu em Relacionados, não houve comentário de conflitos, detalhes da ADR-0001 foram copiados como se fossem desta decisão, uma métrica (entrega de SMS ≥ 98%) veio de um exemplo da pergunta do agente e não do usuário, e a justificativa saiu duplicada. O teste mostrou que o sistema não distinguia ADR Proposta de Aceita.

**Crítica:** foram implementadas a pendência automática quando uma ADR citada não existe na pasta ou não está Aceita, e as regras de prompt: só ADR Aceita vale, ADRs anteriores servem de contexto e perguntas do agente não são fatos. A normalização da justificativa também foi reforçada.

### **T18 — Relação entre ADRs, 2ª execução**

**Modelo:** Groq, openai/gpt-oss-120b.

**Como foi testado:** mesmo roteiro do SMS, após as correções do T17.

**Resultado:** Inconclusivo. A pasta estava sem a ADR-0001 (o rascunho saiu como ADR-0001 e a ADR-0021 foi apontada como não encontrada, o que confirma a nova regra) e a conversa incluiu a 3ª mensagem do roteiro do e-mail (EPS-600), gerando um rascunho híbrido. Mesmo assim, o agente resolveu contradições em silêncio (revisão em 3 em vez de 2 meses; EPS-600 em vez de EPS-640), afirmou “não há restrição de prazo” sem base, criou duas opções de status quo e usou “necessidade de telefone”, vinda de uma pergunta sua.

**Crítica:** a causa foi operacional: a pasta de ADRs foi substituída ao atualizar o agente e não havia botão para iniciar nova conversa. Foram adicionados o botão Nova conversa e regras para registrar divergências como pendência. O reteste foi feito depois: com a ADR citada Aceita no T21 (parte 2\) e com ela Proposta no T26.

### **T19 — Testes de código em ambiente de desenvolvimento**

**Modelo:** Não se aplica (testes sem chamada ao LLM).

**Como foi testado:** execução manual de scripts para: normalização da justificativa em vários formatos, pendências de relação entre ADRs (Proposta, Aceita e inexistente), troca do hífen especial, rejeição de título vazio, tamanho do esquema compacto (2.396 para 1.329 caracteres), limite de contexto (12.200 caracteres), corte do histórico, parâmetro de raciocínio enviado só ao Groq com gpt-oss e não ao Gemini, e compilação dos arquivos.

**Resultado:** Aprovado, após duas correções: a regra da justificativa falhou em “A opção...” e em “oferecer ambos os canais, porque...”, e um teste usou título curto demais e foi refeito.

**Crítica:** os testes foram scripts manuais, sem suíte automatizada. Sugestão: transformá-los em testes pytest para repetir a cada mudança.

### **T20 — Instalação e execução no Windows**

**Modelo:** Não se aplica.

**Como foi testado:** instalação e execução em dois computadores com Windows.

**Resultado:** Aprovado após ajustes. No primeiro, o pip não era reconhecido (Python fora do PATH) e foi preciso instalar o Python e usar py \-m pip. No segundo, apareceu “No module named uvicorn” porque as dependências não estavam instaladas.

**Crítica:** o README deve trazer os passos para Windows com py \-m pip e py \-m uvicorn. O Python 3.15 é muito recente e pode faltar pacote pronto; recomenda-se o 3.13. Ao atualizar o agente, não substituir a pasta adrs inteira, para não apagar ADRs salvas.

### **T21 — Relação entre ADRs com ADR Aceita (parte 1: ADR-A; parte 2: ADR-B)**

**Modelo:** Groq, openai/gpt-oss-120b, raciocínio low.

**Como foi testado:** nova conversa com as três mensagens do roteiro 2.2 (ADR-A), pasta de teste sem outras ADRs, e clique em Gerar ADR. O rascunho foi revisado por humano e salvo como ADR-0001 “Escolha do modelo de IA para testes de ADR”, status Proposto.

**Resultado:** Aprovado com ressalvas. O rascunho trouxe a estrutura completa no modelo, mas com falhas que a revisão humana corrigiu: a marcação de “sugestão da IA” invertida (no item errado), Confirmação e Necessidade de revisão em branco, embora o usuário tenha informado o critério (9 de cada 10 gerações com JSON válido) e o gatilho (Groq retirar o modelo ou troca de rede), e algumas invenções \[detalhar quais\]. Na versão revisada, a única opção marcada como sugestão da IA é o status quo, que o usuário não citou, e ficou uma pendência: prós e contras do Ollama “\[A definir\]”.

**Crítica:** os erros repetem padrões já observados (consequências e confirmação em branco, invenções). Pelo critério do professor, sugestão marcada é aceitável, mas marcação no item errado é falha, porque afirma algo falso sobre a origem do conteúdo. O rascunho original do agente deve ser anexado como evidência, já que este registro só tem a versão revisada.

**Parte 2 — ADR-B com a ADR-0001 Aceita**

**Modelo:** Groq, openai/gpt-oss-120b, raciocínio low.

**Como foi testado:** pasta ./adrs com a ADR-0001 Aceita (T22). Nova conversa com as duas mensagens da ADR-B (roteiro 2.2), espera de cerca de 1 minuto e Gerar ADR. O agente fez 3 perguntas após a 1ª mensagem e marcou pronto após a 2ª. O rascunho foi salvo sem edição como ADR-0002-rodar-testes-principais-em-gemini-3-8-flash-alem-do-groq.md, para ser usado no teste de rejeição.

**Resultado:** Aprovado com ressalvas. Acertos na relação entre ADRs: ADR-0001 em Relacionados (deduzida de “ligada à anterior”), Substitui vazio, nenhuma pendência “ADR-0001 está …” (ela está Aceita) e nada copiado da ADR-0001 (sem critério 9/10, espera de 1 minuto ou TST-12). Papéis corretos: grupo em Decisores, professor só em Informados e Consultados “\[A definir\]” com pendência. As três opções do usuário, a decisão, TST-15 e a revisão em 1 mês estão certos, e a Confirmação ficou em branco com pendência, sem invenção. Falhas: (1) status quo duplicado: “Manter só Groq” e “Manter status quo” são a mesma opção, e a checagem do código não detectou porque só uma delas tem “status quo” no nome; (2) várias invenções sem a marcação “(sugestão da IA)”: pipeline de CI (em O que será feito, Riscos e Impacto; o projeto não tem CI), coletar e armazenar resultados por modelo, os três critérios de sucesso (incluindo “analisadas dentro de 1 dia”), as mitigações “monitorar uso e abortar execuções” e “ajustar timeout e agendar fora do horário de pico”, “time de desenvolvimento” no Impacto e prós genéricos (“sem limites adicionais”, “nenhum esforço adicional”, “rápido em casa”); (3) “modelo local ou outras opções” em Fora do escopo, que o usuário não disse e lembra o Ollama da ADR-0001; (4) justificativa reescrita (“balanceia comparação e uso de recursos”) em vez do motivo dado (o Gemini grátis também tem limite e é mais lento); (5) sem comentário de relações/conflitos explicando que a ADR-B complementa a ADR-0001.

**Crítica:** o objetivo do teste foi atingido: a relação com uma ADR Aceita foi reconhecida sem gerar pendência falsa e sem copiar conteúdo da ADR anterior, o que não acontecia no T17. Por outro lado, o volume de invenções não marcadas foi alto, e algumas descrevem uma infraestrutura que não existe (CI), então este rascunho não poderia ser aprovado sem revisão. Pelo critério de aceite, o problema não é o modelo sugerir, e sim sugerir sem marcar. A pendência “Estabelecer mecanismo de monitoramento” também é ideia do modelo, o que reforça a decisão em aberto de rotular essas pendências como sugestões do agente. A checagem de status quo duplicado só olha o nome da opção, então não pega casos como este.

### **T22 — Aprovar ADR (reteste)**

**Modelo:** Não se aplica (função do sistema, sem chamada ao LLM).

**Como foi testado:** pasta ./adrs com a ADR-0001 do T21 em status Proposto. Clique em Aprovar/Rejeitar na lista, nome do responsável Felipe e OK na pergunta (Aceito). Windows, Python 3.15, sem alteração de código.

**Resultado:** Aprovado. Após a ação, a lista mostrou a ADR-0001 com status Aceito e sem o botão Aprovar/Rejeitar. O arquivo recebeu o status Aceito e, ao final, o comentário “Aceito por Felipe em 2026-11-13”; o restante do conteúdo ficou inalterado.

**Crítica:** a aprovação funcionou como no T16. A ADR aprovada ainda tinha “\[A definir\]” e uma pendência, o que mantém em aberto a decisão de bloquear a aprovação nesses casos. Como a ADR-0001 foi aprovada antes de gerar a ADR-B, o caso “ADR citada ainda Proposta” não foi retestado nesta sequência; a equipe optou por testar a ADR-B com a ADR-0001 já Aceita.

### **T23 — Rejeitar ADR**

**Modelo:** Não se aplica (função do sistema, sem chamada ao LLM).

**Como foi testado:** pasta ./adrs com a ADR-0002 “Rodar testes principais em Gemini 3.8 Flash além do Groq” (gerada no T21, parte 2\) em status Proposto. Clique em Aprovar/Rejeitar na lista, nome do responsável Felipe e Cancelar na pergunta (Rejeitado). Windows, Python 3.15, sem alteração de código. Observação: a decisão é feita em duas caixas do navegador. A primeira pede o nome com o texto “Nome do responsável pela decisão:”. A segunda é uma caixa de confirmação com o texto “OK \= Aceito \| Cancelar \= Rejeitado”, ou seja, OK aprova e Cancelar rejeita. Se o usuário deixar o nome vazio ou cancelar a primeira caixa, nada é alterado.

**Resultado:** Aprovado. A lista passou a mostrar a ADR-0002 com status Rejeitado e sem o botão Aprovar/Rejeitar; a ADR-0001 continuou Aceita. O arquivo recebeu o status Rejeitado e, ao final, o comentário “Rejeitado por Felipe em 2026-11-13”; o restante do conteúdo ficou idêntico ao rascunho salvo no T21, parte 2\.

**Crítica:** completa o teste de aprovação que ficou pendente no T16. A rejeição usa a caixa OK/Cancelar do navegador, em que Cancelar significa Rejeitado; isso pode confundir o usuário, que costuma entender Cancelar como desistir da ação.

### **T24 — Transição inválida pela API**

**Modelo:** Não se aplica (função do sistema, sem chamada ao LLM).

**Como foi testado:** com o servidor rodando, chamadas diretas ao endpoint /api/status pelo CMD do Windows (curl), sem passar pela interface, que só mostra o botão Aprovar/Rejeitar para ADRs Propostas. Duas tentativas de mudar para Aceito: na ADR-0002, que está Rejeitada (T23), e na ADR-0001, que já está Aceita (T22). Antes, foi registrado o SHA256 dos dois arquivos com certutil, para conferir depois que não foram alterados (ADR-0001: 8bc57c23…a380ca; ADR-0002: 340dd239…e0da771db). Comando usado (ADR-0002): curl \-s \-w "\\nHTTP %{http\_code}\\n" \-X POST http\://127.0.0.1:8000/api/status \-H "Content-Type: application/json" \-d "{"dir":"./adrs","arquivo":"ADR-0002-rodar-testes-principais-em-gemini-3-8-flash-alem-do-groq.md","status":"Aceito","aprovador":"Teste"}". Windows, Python 3.15, sem alteração de código.

**Resultado:** Aprovado. As duas tentativas foram recusadas com HTTP 400 e mensagem clara: “Transição inválida: Rejeitado → Aceito” (ADR-0002) e “Transição inválida: Aceito → Aceito” (ADR-0001). O SHA256 dos dois arquivos após o teste foi idêntico ao de antes, confirmando que nenhum arquivo foi alterado pelas tentativas recusadas.

**Crítica:** a regra de transições está no servidor (domínio), e não só na interface, então não pode ser contornada chamando a API diretamente. Rejeitado funciona como estado final. Pela leitura do código (não testado), um nome de arquivo inexistente deve gerar erro 500 genérico em vez de uma mensagem clara; fica como melhoria futura. A API não tem autenticação, o que é aceitável por rodar só em localhost, e o campo aprovador aceita qualquer nome.

### **T25 — Raciocínio médio x baixo (ADR-A)**

**Modelo:** Groq, openai/gpt-oss-120b, raciocínio medium (GROQ\_REASONING=medium).

**Como foi testado:** servidor parado, variável definida no CMD com set GROQ\_REASONING=medium e servidor iniciado de novo na mesma janela. As ADRs foram retiradas da pasta ./adrs (em vez de usar uma pasta nova), então o rascunho saiu como ADR-0001 e não havia outra ADR para referenciar. Nova conversa com as 3 mensagens da ADR-A (roteiro 2.2) e Gerar ADR, sem salvar. Diferença em relação ao roteiro: as perguntas do agente levaram a uma 4ª mensagem do usuário (“Proposta; o link será inserido manualmente; o responsável será Felipe e seu cargo é PO”). Windows, Python 3.15, sem alteração de código.

**Resultado:** Aprovado com ressalvas. Acertos: Decisores (grupo), Consultados (professor) e Informados (colegas) corretos; as quatro alternativas do usuário presentes; Ollama como evolução futura; só o status quo marcado como sugestão da IA (no rascunho em baixo a marcação tinha saído invertida); Confirmação preenchida com o critério do usuário (9 em 10 com JSON válido); primeiro risco correto (bater no limite → esperar 1 minuto); TST-12 presente. Segundo a equipe, as perguntas do chat e o entendimento da conversa foram melhores que em baixo. Falhas: (1) Necessidade de revisão “\[A definir\]”, embora o usuário tenha dado os gatilhos, e sem pendência, porque o código não checa esse campo (mesma falha do rascunho em baixo); (2) os gatilhos de revisão viraram um risco sem sentido (“Groq remover modelo → revisar e trocar de rede”); (3) justificativa duplicada (“porque escolhida por ser grátis…”), que a normalização do código não corrige quando o texto começa com “Escolhida por” sem a palavra “porque”; (4) invenções sem marcação: “logs de uso do Groq” e “contagem de tokens” na Confirmação e nos critérios, “não será alterado o limite de tokens” em Fora do escopo, “pipeline de testes, time de desenvolvimento” no Impacto e “nenhum custo adicional” no status quo; (5) critério de sucesso, limite de tokens e espera de 1 minuto colocados no Contexto e nos Fatores de decisão, que deviam descrever só o problema; (6) pendências fora do escopo do sistema (“definir data de aprovação”, “registrar assinatura de Felipe (PO)”), criadas a partir das perguntas do próprio agente sobre status e aprovação, que são ações humanas no sistema.

**Crítica:** o raciocínio médio corrigiu a marcação de sugestão e preencheu a Confirmação, mas manteve a revisão em branco e as invenções sem marcação. A comparação é apenas indicativa: foi uma execução de cada nível, a conversa em médio teve uma mensagem a mais e o rascunho original em baixo não está anexado (só a versão revisada). O agente perguntou o status da ADR e a data de aprovação, que o sistema já define (sempre Proposto, aprovação humana), e isso gerou pendências inúteis. Falta registrar se houve erro 429 ou demora maior com o raciocínio médio, que gasta mais tokens. Melhorias possíveis no código, fora desta sequência de testes: pendência automática para revisão vazia e normalização de justificativas que começam com “Escolhida por”.

### **T26 — Relação entre ADRs com a ADR citada ainda Proposta**

**Modelo:** Groq, openai/gpt-oss-120b, raciocínio low (servidor reiniciado com GROQ\_REASONING=low após o T25).

**Como foi testado:** pasta ./adrs só com a ADR-0001 revisada (ADR-A gerada em low no T21) em status Proposto, conferido na lista. Nova conversa com as 2 mensagens da ADR-B (roteiro 2.2), espera de cerca de 1 minuto e Gerar ADR. O rascunho foi salvo como ADR-0002-rodar-testes-principais-no-gemini-3-8-flash-em-casa-e-no-gro.md. Windows, Python 3.15, sem alteração de código. Observação: antes, por curiosidade, a equipe repetiu o teste em raciocínio medium e, segundo o relato, também apareceu a pendência “ADR-0001 está Proposto”; esse rascunho não foi anexado.

**Resultado:** Aprovado com ressalvas. O ponto central funcionou: ADR-0001 em Relacionados e a pendência automática “ADR-0001 está Proposto: esta ADR depende de uma decisão que ainda não está em vigor” no painel e no arquivo. Também corretos: grupo em Decisores, professor só em Informados, Consultados “\[A definir\]” com pendência, as três opções, TST-15, revisão em 1 mês e nada copiado da ADR-0001 (sem critério 9/10, espera de 1 minuto ou TST-12). No chat, o agente usou a ADR-0001 para inferir que o Groq é usado na faculdade. Falhas: (1) o chat não avisou que a ADR-0001 ainda não foi aprovada, como o prompt pede, e o Contexto diz que “a ADR-0001 padronizou o uso do Groq”, tratando como em vigor uma decisão só proposta; (2) sem comentário de relações/conflitos explicando a dependência, que ficou coberta só pela regra do código; (3) a opção escolhida foi reinterpretada como “Gemini em casa e Groq na faculdade” (inclusive no título), quando o usuário disse que em casa os testes principais rodariam também no Gemini para comparar com o Groq; (4) status quo duplicado de novo (“Manter só Groq” e “Manter status quo”), sem pendência; (5) invenções sem marcação: os três critérios de sucesso (incluindo “100% dos testes principais dentro de um mês”), a Confirmação (relatório comparativo “entregue e aprovado” e métricas no TST-15), “uso de outros modelos” em Fora do escopo, e “módulo de testes automatizados, times de desenvolvimento e QA, ambientes de CI” no Impacto; (6) as mitigações dos riscos foram inventadas, mas marcadas como “(pendência)” no texto, sem entrar no bloco de pendências; (7) justificativa reescrita (“permite comparar resultados críticos sem sobrecarregar o Gemini”) em vez do motivo dado.

**Crítica:** fecha o caso que estava pendente desde o T17 (Reprovado) e o T18 (Inconclusivo): com a ADR citada ainda Proposta, o sistema agora aponta a dependência. Esse resultado vem da regra no código, que não depende do modelo; o modelo, sozinho, não avisou da dependência nem no chat nem no comentário de conflitos. Comparado com a ADR-B do T21 (ADR-0001 Aceita), a pendência apareceu só quando devia, o que confirma que a regra distingue Proposta de Aceita. Os erros de conteúdo repetem os do T21, parte 2 (status quo duplicado, invenções de CI e equipes, justificativa reescrita), e desta vez houve também uma Confirmação inventada e uma mudança de sentido na opção escolhida, que só a revisão humana pega.

### **T27 — Gemini 3.8 Flash fora da rede da faculdade (ADR-A)**

**Modelo:** Google Gemini, gemini-3.8-flash (gratuito).

**Como foi testado:** em casa, com internet própria e sem o firewall da faculdade, em outro computador com Windows. Pasta ./adrs vazia, nova conversa com as 3 mensagens da ADR-A (roteiro 2.2) e Gerar ADR, para comparar com o Groq em low (T21) e medium (T25). Quando aparecia uma falha, a mesma ação foi repetida, como faria um usuário comum. Uma tentativa anterior no mesmo dia, que falhou com erro 503, não foi contada como teste. Sem alteração de código.

**Resultado:** Reprovado (causa externa). Cada resposta do chat levou cerca de 2 minutos; duas mensagens falharam com “Falha de rede ao chamar a API” e só foram respondidas no reenvio. As três tentativas de Gerar ADR falharam com a mesma mensagem, após 2 a 3 minutos de espera cada uma. O log do servidor registrou 5 respostas 502 Bad Gateway (2 em /api/chat e 3 em /api/generate) e 3 respostas 200 em /api/chat. Nenhum rascunho foi gerado, então o conteúdo não pôde ser comparado com o do Groq. No chat, o modelo encerrou a entrevista após a 2ª mensagem e, depois da 3ª, apontou como pendentes os nomes dos integrantes, embora os papéis já tivessem sido informados.

**Crítica:** a mensagem de erro sem detalhe e a espera de 2 a 3 minutos indicam que o tempo limite de 180 segundos do agente foi atingido (dedução pela leitura do código e pelos tempos; a causa exata não aparece no log). O problema ocorreu fora do firewall, então não se deve só à rede da faculdade: o Gemini gratuito respondeu lento demais para gerar a ADR. Isso confirma a instabilidade vista no T03 e reforça a decisão da ADR-0001 de padronizar os testes no Groq. Observações do código, sem alteração nesta sequência: erros de rede e de tempo limite não são repetidos automaticamente (só os códigos 5xx e 429), o tempo limite é fixo e a mensagem de erro não diz se foi tempo esgotado ou conexão perdida. Os testes T28 e T29, que também dependiam do Gemini, não foram executados.

## **5\. Testes não executados**

| Modelo | Como será testado | Resultado | Crítica |
| :---- | :---- | :---- | :---- |
| Gemini | T28 (ADR-B com a ADR-0001 Proposta, para comparar com o T26) e T29 (limite de uso com o roteiro padrão do PIN por e-mail, para comparar com os erros 429 do Groq no T08 e no T10), ambos com o gemini-3.8-flash | Não executado | Dependiam do Gemini, que não conseguiu gerar a ADR no T27. A equipe encerrou o registro concentrando-se no Groq. |
| Ollama (local) | Roteiro padrão, para avaliar um modelo local sem chave | Não será executado | A equipe decidiu concentrar os testes no Groq gpt-oss-120b. O Ollama segue como evolução futura, como registrado na ADR-0001, e o modo local sem chave não foi avaliado. |

## **6\. Conclusões**

O fluxo do sistema (ler a pasta, conversar, gerar no modelo, salvar sem sobrescrever e aprovar) funcionou nos testes. A qualidade do conteúdo gerado depende do modelo e da revisão humana, o que confirma a avaliação do professor. Falhas recorrentes dos modelos: deixar consequências em branco, inferir detalhes que o usuário não disse e resolver contradições em silêncio. Parte delas foi reduzida com checagens no código (pendências automáticas), que não dependem do modelo.

O T21 repetiu esses padrões e acrescentou a marcação de sugestão no item errado. Pelo critério do professor avaliador, sugestões marcadas são aceitáveis porque o usuário revisa antes de salvar e aprovar; o que continua exigindo atenção é conteúdo não marcado ou marcado de forma errada.

Na sequência T21 a T27, executada sem alteração de código, as funções do sistema foram aprovadas: aprovar (T22), rejeitar (T23) e bloquear transições inválidas pela API, sem alterar os arquivos (T24). A regra de relação entre ADRs, que falhou no T17, funcionou: a pendência aparece quando a ADR citada está Proposta (T26) e não aparece quando está Aceita (T21, parte 2). Esse acerto vem do código; o modelo, sozinho, não avisou da dependência. O raciocínio médio melhorou a marcação de sugestões e a Confirmação, mas não eliminou invenções (T25), e o Gemini não conseguiu gerar a ADR nem fora da rede da faculdade (T27). Erros que continuam: status quo duplicado com nomes diferentes, invenções sem marcação (CI, equipes, critérios de sucesso), justificativa reescrita e Necessidade de revisão em branco. Melhorias identificadas para depois desta sequência: pendência automática para revisão vazia, normalização de justificativas que começam com “Escolhida por”, nova tentativa automática em falhas de rede e mensagem clara para tempo esgotado.

Limitações deste registro: só o Groq com gpt-oss-120b tem registro detalhado de várias rodadas; Gemini, OpenAI e Anthropic não têm comparação documentada, a equipe decidiu não testar o Ollama nesta etapa e concentrar-se no Groq, e o único teste com o Gemini nesta sequência (T27) não gerou ADR por falhas de conexão; e os resultados de LLM podem mudar em outra execução.