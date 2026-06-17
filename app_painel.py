import streamlit as st
import os
import requests
import pandas as pd
import time
from datetime import datetime
from google import genai
from fpdf import FPDF
from groq import Groq

# Configuração da Página do Aplicativo (Visual do Celular)
st.set_page_config(page_title="Império Cibernético v10.1", page_icon="⚡", layout="centered")

# Estilização Cyberpunk
st.markdown("""
    <style>
    .stApp { background-color: #0d0e15; color: #00ff66; }
    h1, h2, h3 { color: #8a2be2 !important; text-shadow: 0 0 10px #8a2be2; }
    .stButton>button { background-color: #8a2be2; color: #00ff66; border: 2px solid #00ff66; box-shadow: 0 0 15px #8a2be2; }
    .stButton>button:hover { background-color: #00ff66; color: #0d0e15; box-shadow: 0 0 20px #00ff66; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { background-color: #1a1c29 !important; color: #00ff66 !important; border: 1px solid #8a2be2 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ IMPÉRIO CIBERNÉTICO V10.1")
st.write("Usina Suprema: Arquitetura Plana Blindada Contra Erros de Indentação.")

ARQUIVO_BANCO = "banco_de_relatorios.csv"

# Preservação de estados na memória de sessão
chaves_estado = ["gemini_s", "groq_s", "mistral_s", "cohere_s", "hf_s", "eleven_s", "heygen_s", "qwen_s", "claude_s", "chatgpt_s"]
for c in chaves_estado:
    if c not in st.session_state:
        st.session_state[c] = ""

# Painel Lateral de Credenciais
st.sidebar.header("🔑 Banco de Energia Suprema")
input_gemini = st.sidebar.text_area("1) Google Gemini Keys", value=st.session_state.gemini_s)
input_groq = st.sidebar.text_area("2) Groq (Llama) Keys", value=st.session_state.groq_s)
input_mistral = st.sidebar.text_area("3) Mistral AI Keys", value=st.session_state.mistral_s)
input_cohere = st.sidebar.text_area("4) Cohere Keys", value=st.session_state.cohere_s)
input_hf = st.sidebar.text_area("5) Hugging Face Tokens", value=st.session_state.hf_s)
input_qwen = st.sidebar.text_area("6) Qwen (Alibaba) Keys", value=st.session_state.qwen_s)
input_claude = st.sidebar.text_area("7) Claude (Anthropic) Keys", value=st.session_state.claude_s)
input_chatgpt = st.sidebar.text_area("8) ChatGPT (OpenAI) Keys", value=st.session_state.chatgpt_s)

st.sidebar.markdown("---")
input_eleven = st.sidebar.text_input("9) ElevenLabs API Key", value=st.session_state.eleven_s, type="password")
input_heygen = st.sidebar.text_input("10) HeyGen API Key", value=st.session_state.heygen_s, type="password")

# Salva na sessão
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

# Listas limpas de chaves
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
# FUNÇÕES DE EXECUÇÃO ISOLADAS (EVITA DESALINHAMENTO DE REDE)
# ==============================================================================
def chamar_gemini(chave, prompt):
    try:
        client = genai.Client(api_key=chave)
        return client.models.generate_content(model='gemini-2.5-flash', contents=prompt).text
    except: return ""

def chamar_groq(chave, prompt):
    try:
        client_groq = Groq(api_key=chave)
        return client_groq.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.1-8b-instant").choices.message.content
    except: return ""

def chamar_mistral(chave, prompt):
    try:
        headers = {"Authorization": f"Bearer {chave}", "Content-Type": "application/json"}
        payload = {"model": "mistral-tiny", "messages": [{"role": "user", "content": prompt}]}
        res = requests.post("https://mistral.ai", json=payload, headers=headers, timeout=10).json()
        return res["choices"]["message"]["content"]
    except: return ""

def chamar_cohere(chave, prompt):
    try:
        headers = {"Authorization": f"Bearer {chave}", "Content-Type": "application/json"}
        payload = {"model": "command-r-plus", "message": prompt}
        res = requests.post("https://cohere.com", json=payload, headers=headers, timeout=10).json()
        return res["text"]
    except: return ""

def chamar_huggingface(token, prompt):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"inputs": prompt}
        res = requests.post("https://huggingface.co", json=payload, headers=headers, timeout=10).json()
        if isinstance(res, list) and len(res) > 0: return res[0].get("generated_text", "")
        return res.get("generated_text", "")
    except: return ""

def chamar_qwen(chave, prompt):
    try:
        headers = {"Authorization": f"Bearer {chave}", "Content-Type": "application/json"}
        payload = {"model": "qwen/qwen-2.5-72b-instruct", "messages": [{"role": "user", "content": prompt}]}
        res = requests.post("https://openrouter.ai", json=payload, headers=headers, timeout=10).json()
        return res["choices"]["message"]["content"]
    except: return ""

def chamar_claude(chave, prompt):
    try:
        headers = {"x-api-key": chave, "anthropic-version": "2023-06-01", "content-type": "application/json"}
        payload = {"model": "claude-3-haiku-20240307", "max_tokens": 1000, "messages": [{"role": "user", "content": prompt}]}
        res = requests.post("https://anthropic.com", json=payload, headers=headers, timeout=10).json()
        return res["content"]["text"]
    except: return ""

def chamar_chatgpt(chave, prompt):
    try:
        headers = {"Authorization": f"Bearer {chave}", "Content-Type": "application/json"}
        payload = {"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": prompt}]}
        res = requests.post("https://openai.com", json=payload, headers=headers, timeout=10).json()
        return res["choices"]["message"]["content"]
    except: return ""

# ------------------------------------------------------------------------------
# ABA 1: EXECUÇÃO DO LABORATÓRIO (FLUXO TOTALMENTE PLANO)
# ------------------------------------------------------------------------------
with aba_gerador:
    st.subheader("⚙️ Execução Generativa Estabilizada")
    
    if st.button("🚀 DISPARAR ENXAME CIBERNÉTICO", use_container_width=True):
        if not any([lista_gemini, lista_groq, lista_mistral, lista_cohere, lista_hf, lista_qwen, lista_claude, lista_chatgpt]):
            st.error("❌ Erro: Insira pelo menos uma chave de inteligência artificial na barra lateral.")
        else:
            texto_completo = ""
            nome_produto = "Dispositivo Desconhecido"
            
            historico_total = "Nenhuma invenção criada ainda."
            if os.path.exists(ARQUIVO_BANCO):
                try:
                    df_h = pd.read_csv(ARQUIVO_BANCO)
                    if not df_h.empty:
                        col = "Invenção" if "Invenção" in df_h.columns else "Produto Identificado"
                        historico_total = ", ".join(df_h[col].astype(str).tolist())
                except: pass

            prompt_sistema = f"Tempo: {time.time()}. Histórico: [{historico_total}]. Projete um NOVO dispositivo ou motor focado em ENERGIA AUTOSSUSTENTÁVEL ou CIBERNÉTICA. Na PRIMEIRA LINHA responda obrigatoriamente: 'NOME: [Nome da Invenção]'."

            # Execução Sequencial Linear Plana - Sem aninhamento de chaves
            if not texto_completo and lista_gemini:
                st.info("🧠 Acionando Motor 1: Google Gemini...")
                for c in lista_gemini:
                    texto_completo = chamar_gemini(c, prompt_sistema)
                    if texto_completo: break

            if not texto_completo and lista_groq:
                st.info("⚠️ Acionando Motor 2: Groq Llama...")
                for c in lista_groq:
                    texto_completo = chamar_groq(c, prompt_sistema)
                    if texto_completo: break

            if not texto_completo and lista_mistral:
                st.info("🌀 Acionando Motor 3: Mistral AI...")
                for c in lista_mistral:
                    texto_completo = chamar_mistral(c, prompt_sistema)
                    if texto_completo: break

            if not texto_completo and lista_cohere:
                st.info("🔮 Acionando Motor 4: Cohere...")
                for c in lista_cohere:
                    texto_completo = chamar_cohere(c, prompt_sistema)
                    if texto_completo: break

            if not texto_completo and lista_hf:
                st.info("🛡️ Acionando Motor 5: Hugging Face...")
                for c in lista_hf:
