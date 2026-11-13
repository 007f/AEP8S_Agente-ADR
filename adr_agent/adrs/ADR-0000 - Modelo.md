# ADR-0001: \[Título curto no imperativo ou substantivo — ex: "Uso de PostgreSQL como banco primário"\]

* **Status:** Proposto  
* **Data:** 2026-10-20  
* **Decisores:** \[nomes/roles\]  
* **Consultados:** \[nomes/roles — quem foi ouvido mas não decide\]  
* **Informados:** \[nomes/roles — quem só precisa saber\]  
* **Substitui:** \[ADR-XXXX, se aplicável\]  
* Relacionados:

## Contexto e problema

Descreva o cenário técnico, de negócio e as restrições que tornam essa decisão necessária. Inclua: escala esperada, prazo, orçamento, requisitos regulatórios, competências do time, dívida técnica existente. 

Seja factual e neutro. Aqui não se defende solução, apenas se descreve o problema. Ex: "O sistema atual processa 200 req/s e precisa suportar 5.000 req/s em 12 meses. O time tem pouca experiência com operação distribuída."

## Fatores de decisão

Critérios objetivos usados para comparar as opções:  
\- Custo total de operação  
\- Curva de aprendizado do time  
\- Requisitos de consistência transacional  
\- Portabilidade entre provedores de nuvem  
\- Licenciamento

## Opções consideradas

### Opção 1: \[Nome\]

Descrição breve da abordagem.

### Opção 2: \[Nome\]

Descrição breve da abordagem.

### Opção 3: \[Não fazer nada / manter status quo\]

Sempre inclua — às vezes a melhor decisão é não mudar.

## Resultado da decisão

**Escolhida: Opção X, porque \[razão principal em 1-2 frases\].**

Detalhe aqui o que exatamente será feito, limites da decisão (o que ela NÃO cobre) e critérios de sucesso mensuráveis.

## Prós e contras das opções

### Opção 1

* 👍 \[pró\]  
* 👎 \[contra\]

### Opção 2

* 👍 \[pró\]  
* 👎 \[contra\]

## Consequências

* **Positivas:** \[o que melhora\]  
* **Negativas:** \[o que piora, o que se aceita como trade-off\]  
* **Riscos:** \[risco → mitigação\]  
* **Impacto:** \[módulos, times, sistemas afetados\]  
* **Necessidade de revisão:** \[gatilho que reabre a discussão — ex: "se o volume passar de 50k req/s"\]

## Confirmação

Como saberemos, na prática, que a decisão foi implementada e está funcionando? Ex: "Alerta de latência p95 no Grafana; revisão trimestral de custo de infra."

## Links

* \[Issue/épico relacionado\]  
* \[Prova de conceito\]  
* \[Documentação externa relevante\]

