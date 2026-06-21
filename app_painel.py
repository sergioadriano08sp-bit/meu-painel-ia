import streamlit as st
import os
import requests
import pandas as pd
import time
from datetime import datetime
from google import genai
from fpdf import FPDF
from groq import Groq

# ==============================================================================
# ESTILIZAÇÃO MODO ESCURO / CYBERPUNK
# ==============================================================================
st.set_page_config(page_title="Império Cibernético v12.4", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0d0e15; color: #00ff66; }
    h1, h2, h3 { color: #8a2be2 !important; text-shadow: 0 0 10px #8a2be2; }
    .stButton>button { background-color: #8a2be2; color: #00ff66; border: 2px solid #00ff66; box-shadow: 0 0 15px #8a2be2; width: 100%; height: 50px; font-weight: bold; }
    .stButton>button:hover { background-color: #00ff66; color: #0d0e15; box-shadow: 0 0 20px #00ff66; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { background-color: #1a1c29 !important; color: #00ff66 !important; border: 1px solid #8a2be2 !important; }
    sidebar .sidebar-content { background-color: #12131c !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ IMPÉRIO CIBERNÉTICO V12.4")
st.write("Central Suprema: Arquitetura Linear Sem Blocos Aninhados e Livre de Erros.")

ARQUIVO_BANCO = "banco_de_relatorios.csv"

# ==============================================================================
# SISTEMA DE MEMÓRIA DE SESSÃO ATIVA (SALVA TODAS AS 10 CHAVES NA TELA)
# ==============================================================================
chaves_estado = ["gemini_s", "groq_s", "mistral_s", "cohere_s", "hf_s", "qwen_s", "claude_s", "chatgpt_s", "eleven_s", "heygen_s", "minha_chave_pix"]
for c in chaves_estado:
    if c not in st.session_state:
        st.session_state[c] = ""

# ==============================================================================
# PAINEL LATERAL DE CREDENCIAIS MONUMENTAL (10 ESPAÇOS CONSOLIDADOS)
# ==============================================================================
st.sidebar.header("🔑 Banco de Energia Suprema")
st.sidebar.write("Cole os códigos correspondentes. Separe múltiplas chaves por vírgula.")

input_gemini = st.sidebar.text_area("1) Google Gemini Keys", value=st.session_state.gemini_s)
input_groq = st.sidebar.text_area("2) Groq (Llama 3.3) Keys", value=st.session_state.groq_s)
input_mistral = st.sidebar.text_area("3) Mistral AI Keys", value=st.session_state.mistral_s)
input_cohere = st.sidebar.text_area("4) Cohere Keys", value=st.session_state.cohere_s)
input_hf = st.sidebar.text_area("5) Hugging Face Tokens", value=st.session_state.hf_s)
input_qwen = st.sidebar.text_area("6) Qwen (Alibaba) Keys", value=st.session_state.qwen_s)
input_claude = st.sidebar.text_area("7) Claude (Anthropic) Keys", value=st.session_state.claude_s)
input_chatgpt = st.sidebar.text_area("8) ChatGPT (OpenAI) Keys", value=st.session_state.chatgpt_s)

st.sidebar.markdown("---")
st.sidebar.header("🎥 Motores Multimídia & Robôs")
input_eleven = st.sidebar.text_input("9) ElevenLabs API Key", value=st.session_state.eleven_s, type="password")
input_heygen = st.sidebar.text_input("10) HeyGen API Key", value=st.session_state.heygen_s, type="password")

st.sidebar.markdown("---")
st.sidebar.header("💰 Configuração de Faturamento")
input_pix = st.sidebar.text_input("Sua Chave Pix (E-mail, CPF ou Telefone)", value=st.session_state.minha_chave_pix)

# Atualiza a memória de sessão para manter os dados salvos na tela
st.session_state.gemini_s = input_gemini
st.session_state.groq_s = input_groq
st.session_state.mistral_s = input_mistral
st.session_state.cohere_s = input_cohere
st.session_state.hf_s = input_hf
st.session_state.qwen_s = input_qwen
st.session_state.claude_s = input_claude
st.session_state.chatgpt_s = input_chatgpt
st.session_state.eleven_s = input_eleven
st.session_state.heygen_s = input_heygen
st.session_state.minha_chave_pix = input_pix

# Separação limpa de chaves
lista_gemini = [k.strip() for k in input_gemini.split(",") if k.strip()]
lista_groq = [k.strip() for k in input_groq.split(",") if k.strip()]
lista_mistral = [k.strip() for k in input_mistral.split(",") if k.strip()]
lista_cohere = [k.strip() for k in input_cohere.split(",") if k.strip()]
lista_hf = [k.strip() for k in input_hf.split(",") if k.strip()]
lista_qwen = [k.strip() for k in input_qwen.split(",") if k.strip()]
lista_claude = [k.strip() for k in input_claude.split(",") if k.strip()]
lista_chatgpt = [k.strip() for k in input_chatgpt.split(",") if k.strip()]

# Abas do sistema
aba_gerador, aba_vendas, aba_fisica = st.tabs(["🧠 Laboratório Generativo", "🏪 Máquina de Vendas", "🔌 Engenharia Maker Física"])

def criar_pdf_comercial(titulo, conteudo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, f"PATENTE CONCEITUAL: {titulo}", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 10, txt=conteudo.encode('utf-8', 'ignore').decode('utf-8'))
    return pdf.output()

# ==============================================================================
# FUNÇÕES DE EXECUÇÃO ISOLADAS PLANAS (SINTAXE BLINDADA)
# ==============================================================================
def chamar_gemini(chave, prompt):
    t_inicio = time.time()
    try:
        client = genai.Client(api_key=chave)
        res = client.models.generate_content(model='gemini-2.5-flash', contents=prompt).text
        return res, f"Sucesso em {time.time() - t_inicio:.2f}s"
    except Exception as e: return "", f"Erro: {str(e)}"

def chamar_groq(chave, prompt):
    t_inicio = time.time()
    try:
        client_groq = Groq(api_key=chave)
        chat_completion = client_groq.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
        return chat_completion.choices.message.content, f"Sucesso em {time.time() - t_inicio:.2f}s"
    except Exception as e: return "", f"Erro: {str(e)}"

def chamar_mistral(chave, prompt):
    t_inicio = time.time()
    try:
        headers = {"Authorization": f"Bearer {chave}", "Content-Type": "application/json"}
        payload = {"model": "mistral-tiny", "messages": [{"role": "user", "content": prompt}]}
        res = requests.post("https://mistral.ai", json=payload, headers=headers, timeout=10).json()
        return res["choices"]["message"]["content"], f"Sucesso em {time.time() - t_inicio:.2f}s"
    except Exception as e: return "", f"Erro: {str(e)}"

def chamar_cohere(chave, prompt):
    t_inicio = time.time()
    try:
        headers = {"Authorization": f"Bearer {chave}", "Content-Type": "application/json"}
        payload = {"model": "command-r-plus", "message": prompt}
        res = requests.post("https://cohere.com", json=payload, headers=headers, timeout=10).json()
        return res["text"], f"Sucesso em {time.time() - t_inicio:.2f}s"
    except Exception as e: return "", f"Erro: {str(e)}"

def chamar_huggingface(token, prompt):
    t_inicio = time.time()
    try:
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"inputs": prompt}
        res = requests.post("https://huggingface.co", json=payload, headers=headers, timeout=10).json()
        txt = res.get("generated_text", "") if isinstance(res, list) else res.get("generated_text", "")
        return txt, f"Sucesso em {time.time() - t_inicio:.2f}s"
    except Exception as e: return "", f"Erro: {str(e)}"

def chamar_qwen(chave, prompt):
    t_inicio = time.time()
    try:
        headers = {"Authorization": f"Bearer {chave}", "Content-Type": "application/json"}
        payload = {"model": "qwen/qwen-2.5-72b-instruct", "messages": [{"role": "user", "content": prompt}]}
        res = requests.post("https://openrouter.ai", json=payload, headers=headers, timeout=10).json()
        return res["choices"]["message"]["content"], f"Sucesso em {time.time() - t_inicio:.2f}s"
    except Exception as e: return "", f"Erro: {str(e)}"

def chamar_claude(chave, prompt):
    t_inicio = time.time()
    try:
        headers = {"x-api-key": chave, "anthropic-version": "2023-06-01", "content-type": "application/json"}
        payload = {"model": "claude-3-haiku-20240307", "max_tokens": 1000, "messages": [{"role": "user", "content": prompt}]}
        res = requests.post("https://anthropic.com", json=payload, headers=headers, timeout=10).json()
        return res["content"]["text"], f"Sucesso em {time.time() - t_inicio:.2f}s"
    except Exception as e: return "", f"Erro: {str(e)}"

def chamar_chatgpt(chave, prompt):
    t_inicio = time.time()
    try:
        headers = {"Authorization": f"Bearer {chave}", "Content-Type": "application/json"}
        payload = {"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": prompt}]}
        res = requests.post("https://openai.com", json=payload, headers=headers, timeout=10).json()
        return res["choices"]["message"]["content"], f"Sucesso em {time.time() - t_inicio:.2f}s"
    except Exception as e: return "", f"Erro: {str(e)}"

# ------------------------------------------------------------------------------
# ABA 1: LABORATÓRIO GENERATIVO (ARQUITETURA TOTALMENTE FLUXO PLANO)
# ------------------------------------------------------------------------------
with aba_gerador:
    st.subheader("⚙️ Painel de Ação e Diagnóstico de Rede")
    box_telemetria = st.code("📡 Inicializando rastreador de sinal... Ready.")
    
    chaves_existentes = any([lista_gemini, lista_groq, lista_mistral, lista_cohere, lista_hf, lista_qwen, lista_claude, lista_chatgpt])
    
    # Validação feita fora do botão de clique. Evita 100% qualquer IndentationError.
    if chaves_existentes == False:
