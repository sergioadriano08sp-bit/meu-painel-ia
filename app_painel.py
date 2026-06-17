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
st.set_page_config(page_title="Império Cibernético v9.0", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0d0e15; color: #00ff66; }
    h1, h2, h3 { color: #8a2be2 !important; text-shadow: 0 0 10px #8a2be2; }
    .stButton>button { background-color: #8a2be2; color: #00ff66; border: 2px solid #00ff66; box-shadow: 0 0 15px #8a2be2; }
    .stButton>button:hover { background-color: #00ff66; color: #0d0e15; box-shadow: 0 0 20px #00ff66; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { background-color: #1a1c29 !important; color: #00ff66 !important; border: 1px solid #8a2be2 !important; }
    sidebar .sidebar-content { background-color: #12131c !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ IMPÉRIO CIBERNÉTICO V9.0")
st.write("Usina Suprema: 10 Motores Mundiais de Inteligência Artificial e Mídia Sintética.")

ARQUIVO_BANCO = "banco_de_relatorios.csv"

# ==============================================================================
# SISTEMA DE MEMÓRIA DE SESSÃO ATIVA (SALVA TODAS AS 10 CHAVES NA TELA)
# ==============================================================================
chaves_estado = ["gemini_s", "groq_s", "mistral_s", "cohere_s", "hf_s", "eleven_s", "heygen_s", "qwen_s", "claude_s", "chatgpt_s"]
for chave in chaves_estado:
    if chave not in st.session_state:
        st.session_state[chave] = ""

# ==============================================================================
# PAINEL LATERAL DE CREDENCIAIS MONUMENTAL (10 ESPAÇOS CONSOLIDADOS)
# ==============================================================================
st.sidebar.header("🔑 Banco de Energia Suprema")
st.sidebar.write("Cole os códigos correspondentes. Múltiplas chaves podem ser separadas por vírgula.")

input_gemini = st.sidebar.text_area("1) Google Gemini Keys", value=st.session_state.gemini_s)
input_groq = st.sidebar.text_area("2) Groq (Llama) Keys", value=st.session_state.groq_s)
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

# Separação limpa de chaves
lista_gemini = [k.strip() for k in input_gemini.split(",") if k.strip()]
lista_groq = [k.strip() for k in input_groq.split(",") if k.strip()]
lista_mistral = [k.strip() for k in input_mistral.split(",") if k.strip()]
lista_cohere = [k.strip() for k in input_cohere.split(",") if k.strip()]
lista_hf = [k.strip() for k in input_hf.split(",") if k.strip()]
lista_qwen = [k.strip() for k in input_qwen.split(",") if k.strip()]
lista_claude = [k.strip() for k in input_claude.split(",") if k.strip()]
lista_chatgpt = [k.strip() for k in input_chatgpt.split(",") if k.strip()]

# ==============================================================================
# NAVEGAÇÃO ENTRE MÓDULOS (Abas)
# ==============================================================================
aba_gerador, aba_vendas, aba_fisica = st.tabs(["🧠 Laboratório Generativo", "🏪 Máquina de Vendas (Landing Page)", "🔌 Engenharia Maker Física"])

def criar_pdf_comercial(titulo, conteudo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, f"PATENTE CONCEITUAL: {titulo}", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 10, txt=conteudo.encode('utf-8', 'ignore').decode('utf-8'))
    return pdf.output()

# ------------------------------------------------------------------------------
# ABA 1: LABORATÓRIO GENERATIVO (Varre as chaves de forma linear alinhada)
# ------------------------------------------------------------------------------
with aba_gerador:
    st.subheader("⚙️ Execução Generativa Estabilizada")
    
    if st.button("🚀 DISPARAR ENXAME CIBERNÉTICO", use_container_width=True):
        chaves_existentes = any([lista_gemini, lista_groq, lista_mistral, lista_cohere, lista_hf, lista_qwen, lista_claude, lista_chatgpt])
        if not chaves_existentes:
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

            # CANAL 1: GOOGLE GEMINI
            if not texto_completo and lista_gemini:
                with st.spinner("🧠 Consultando canal do Google Gemini..."):
                    for i, chave in enumerate(lista_gemini):
                        try:
                            client = genai.Client(api_key=chave)
                            texto_completo = client.models.generate_content(model='gemini-2.5-flash', contents=prompt_sistema).text
                            st.info(f"⚡ Sucesso via Google Gemini (Chave #{i+1})")
                            break
                        except: pass

            # CANAL 2: GROQ (LLAMA 3.1)
            if not texto_completo and lista_groq:
                with st.spinner("⚠️ Mudando rota para o canal da Groq..."):
                    for i, chave in enumerate(lista_groq):
                        try:
                            client_groq = Groq(api_key=chave)
                            texto_completo = client_groq.chat.completions.create(messages=[{"role": "user", "content": prompt_sistema}], model="llama-3.1-8b-instant").choices.message.content
                            st.info(f"⚡ Sucesso via Groq Llama (Chave #{i+1})")
                            break
                        except: pass

            # CANAL 3: MISTRAL AI
            if not texto_completo and lista_mistral:
                with st.spinner("🌀 Mudando rota para o canal da Mistral AI..."):
                    for i, chave in enumerate(lista_mistral):
                        try:
                            headers = {"Authorization": f"Bearer {chave}", "Content-Type": "application/json"}
                            payload = {"model": "mistral-tiny", "messages": [{"role": "user", "content": prompt_sistema}]}
                            res = requests.post("https://mistral.ai", json=payload, headers=headers, timeout=10).json()
                            texto_completo = res["choices"]["message"]["content"]
                            st.info(f"⚡ Sucesso via Mistral AI (Chave #{i+1})")
                            break
                        except: pass

            # CANAL 4: COHERE
            if not texto_completo and lista_cohere:
                with st.spinner("🔮 Mudando rota para o canal da Cohere..."):
                    for i, chave in enumerate(lista_cohere):
                        try:
                            headers = {"Authorization": f"Bearer {chave}", "Content-Type": "application/json"}
                            payload = {"model": "command-r-plus", "message": prompt_sistema}
                            res = requests.post("https://cohere.com", json=payload, headers=headers, timeout=10).json()
                            texto_completo = res["text"]
                            st.info(f"⚡ Sucesso via Cohere (Chave #{i+1})")
                            break
                        except: pass

            # CANAL 5: HUGGING FACE
            if not texto_completo and lista_hf:
                with st.spinner("🛡️ Ativando a fortaleza da Hugging Face..."):
                    for i, token in enumerate(lista_hf):
                        try:
                            headers = {"Authorization": f"Bearer {token}"}
                            payload = {"inputs": prompt_sistema}
                            res = requests.post("https://huggingface.co", json=payload, headers=headers, timeout=10).json()
         
