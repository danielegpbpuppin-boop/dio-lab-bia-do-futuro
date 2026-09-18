import json
import streamlit as st
import pandas as pd
import requests
import os

# ===================== CONFIGURAÇÃO ====================
HF_API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
HF_HEADERS = {"Authorization": f"Bearer {os.getenv('HF_TOKEN', '')}"}  # opcional, se tiver token

# ============ CARREGAR DADOS ===========
perfil = json.load(open('./data/perfil_investidor.json', encoding="utf-8"))
transacoes = pd.read_csv('./data/transacoes.csv', encoding="utf-8")
historico = pd.read_csv('./data/historico_atendimento.csv', encoding="utf-8")
produtos = json.load(open('./data/produtos_financeiros.json', encoding="utf-8"))

# =============== MONTAR CONTEXTO ============
contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}
TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

# ============= SYSTEM PROMPT ================
SYSTEM_PROMPT = """
Você é AFIN, um assistente financeiro interativo, empático e didático.

Seu objetivo é tornar conceitos de finanças pessoais mais acessíveis,
traduzindo-os em exemplos práticos do dia a dia e utilizando dados do próprio cliente
para facilitar a compreensão, sem oferecer recomendações de investimento.

Regras:
1. Só usa dados fornecidos no contexto.
2. Não recomenda investimentos específicos.
3. Admite quando não sabe algo.
4. Foca apenas em educar e não aconselhar.
5. Explica conceitos com exemplos do cotidiano.
"""

# ====================== CHAMAR API =============
def perguntar(msg):
    prompt = f"{SYSTEM_PROMPT}\n\nContexto do Cliente:\n{contexto}\n\nPergunta: {msg}"
    response = requests.post(HF_API_URL, headers=HF_HEADERS, json={"inputs": prompt})
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return f"Erro na API: {response.status_code} - {response.text}"

# ============== INTERFACE ============
st.title("AFIN - Seu Auxiliar Financeiro")

if pergunta := st.chat_input("Sua dúvida sobre finanças..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("Pensando..."):
        resposta = perguntar(pergunta)
        st.chat_message("assistant").write(resposta)
