# Agente de ADR (local)

    pip install -r requirements.txt
    uvicorn app.main:app --host 127.0.0.1 --port 8000
    # abra http://127.0.0.1:8000

1. Escolha provedor/modelo, cole a chave de API (não é gravada em disco) e informe a pasta das ADRs.
2. Converse sobre a decisão; quando o agente indicar que há informação suficiente, clique em "Gerar ADR".
3. Revise/edite o rascunho e salve. Pendências e possíveis conflitos ficam num comentário HTML no fim do arquivo.
4. A aprovação (Aceito/Rejeitado) é sempre ação humana, pelo botão na lista.
