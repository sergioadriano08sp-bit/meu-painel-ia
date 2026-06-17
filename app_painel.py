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
# ESTILIZAÇÃO MODO ESCURO / CYBERPUNK (PILAR 1)
# ==============================================================================
st.set_page_config(page_title="Império Cibernético v8.0", page_icon="⚡", layout="centered")

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

st.title("⚡ IMPÉRIO CIBERNÉTICO V8.0")
st.write("Usina de Dados Suprema: Revezamento de 5 Motores Globais de Inteligência Artificial.")

ARQUIVO_BANCO = "banco_de_relatorios.csv"

# Preservação de estados na memória de sessão do navegador
if "gemini_lista" not in st.session_state: st.session_state.gemini_lista = ""
if "groq_lista" not in st.session_state: st.session_state.groq_lista = ""
if "mistral_lista" not in st.session_state: st.session_state.mistral_lista = ""
if "cohere_lista" not in st.session_state: st.session_state.cohere_lista = ""
if "hf_lista" not in st.session_state: st.session_state.hf_lista = ""

# ==============================================================================
# PAINEL LATERAL DE CREDENCIAIS AVANÇADO (EXPANSÃO DE MOTORES)
# ==============================================================================
st.sidebar.header("🔑 Banco de Energia de 5 Motores")
st.sidebar.write("Separe múltiplas chaves por vírgula para ativar o ciclo perpétuo.")

input_gemini = st.sidebar.text_area("1) Google Gemini Keys", value=st.session_state.gemini_lista)
input_groq = st.sidebar.text_area("2) Groq (Llama 3) Keys", value=st.session_state.groq_lista)
input_mistral = st.sidebar.text_area("3) Mistral AI Keys", value=st.session_state.mistral_lista)
input_cohere = st.sidebar.text_area("4) Cohere Keys", value=st.session_state.cohere_lista)
input_hf = st.sidebar.text_area("5) Hugging Face Tokens", value=st.session_state.hf_lista)

st.session_state.gemini_lista = input_gemini
st.session_state.groq_lista = input_groq
st.session_state.mistral_lista = input_mistral
st.session_state.cohere_lista = input_cohere
st.session_state.hf_lista = input_hf

# Processamento dinâmico de strings em listas limpas
lista_gemini = [k.strip() for k in input_gemini.split(",") if k.strip()]
lista_groq = [k.strip() for k in input_groq.split(",") if k.strip()]
lista_mistral = [k.strip() for k in input_mistral.split(",") if k.strip()]
lista_cohere = [k.strip() for k in input_cohere.split(",") if k.strip()]
lista_hf = [k.strip() for k in input_hf.split(",") if k.strip()]

st.sidebar.markdown("---")
st.sidebar.subheader("🔋 Carga dos Revezamentos")
st.sidebar.write(f"• Gemini: {len(lista_gemini)} | Groq: {len(lista_groq)}")
st.sidebar.write(f"• Mistral: {len(lista_mistral)} | Cohere: {len(lista_cohere)}")
st.sidebar.write(f"• HuggingFace: {len(lista_hf)}")

# ==============================================================================
# NAVEGAÇÃO ENTRE MÓDULOS (Abas)
# ==============================================================================
aba_gerador, aba_vendas, aba_fisica = st.tabs(["🧠 Laboratório Generativo", "🏪 Máquina de Vendas (Landing Page)", "🔌 Engenharia Maker Física"])

# FUNÇÃO AUXILIAR PARA PDF
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
# ABA 1: LABORATÓRIO GENERATIVO FOCO 5 CÉREBROS MUNDIAIS
# ------------------------------------------------------------------------------
with aba_gerador:
    st.subheader("⚙️ Loop Generativo Quântico Avançado")
    modo_infinito = st.toggle("🔄 ATIVAR OPERAÇÃO INTELIGENTE GENERATIVA INFINITA")

    if st.button("🚀 INICIAR OPERAÇÃO AUTÔNOMA", use_container_width=True) or modo_infinito:
        if not any([lista_gemini, lista_groq, lista_mistral, lista_cohere, lista_hf]):
            st.error("❌ Erro Crítico: Abasteça o banco de energia com pelo menos uma chave de API na barra lateral.")
        else:
            execucoes = 0
            idx_gemini, idx_groq, idx_mistral, idx_cohere, idx_hf = 0, 0, 0, 0, 0
            
            while True:
                execucoes += 1
                texto_completo = ""
                nome_produto = "Dispositivo Desconhecido"
                
                # Leitura de Memória Histórica de Dados
                historico_total = "Nenhuma invenção criada ainda."
                if os.path.exists(ARQUIVO_BANCO):
                    try:
                        df_h = pd.read_csv(ARQUIVO_BANCO)
                        if not df_h.empty:
                            col = "Invenção" if "Invenção" in df_h.columns else "Produto Identificado"
                            historico_total = ", ".join(df_h[col].astype(str).tolist())
                    except: pass

                prompt_sistema = f"Instante: {time.time()}. Histórico de patentes: [{historico_total}]. Projete um dispositivo novo e disruptivo focado em ENERGIA AUTOSSUSTENTÁVEL ou CIBERNÉTICA. Nunca replique dados anteriores. Na PRIMEIRA LINHA responda estritamente: 'NOME: [Nome da Invenção]'."

                # MOTOR 1: GOOGLE GEMINI
                if not texto_completo and lista_gemini:
                    with st.spinner(f"🧠 [Ciclo {execucoes}] Acionando Motor 1 (Google)..."):
                        try:
                            client = genai.Client(api_key=lista_gemini[idx_gemini % len(lista_gemini)])
                            texto_completo = client.models.generate_content(model='gemini-2.5-flash', contents=prompt_sistema).text
                        except: idx_gemini += 1

                # MOTOR 2: GROQ (LLAMA 3)
                if not texto_completo and lista_groq:
                    with st.spinner(f"⚠️ [Ciclo {execucoes}] Acionando Motor 2 (Groq)..."):
                        try:
                            client_groq = Groq(api_key=lista_groq[idx_groq % len(lista_groq)])
                            texto_completo = client_groq.chat.completions.create(messages=[{"role": "user", "content": prompt_sistema}], model="llama-3.1-8b-instant").choices.message.content
                        except: idx_groq += 1

                # MOTOR 3: MISTRAL AI (INTEGRAÇÃO DIRETA VIA API HTTP)
                if not texto_completo and lista_mistral:
                    with st.spinner(f"🌀 [Ciclo {execucoes}] Acionando Motor 3 (Mistral AI)..."):
                        try:
                            headers = {"Authorization": f"Bearer {lista_mistral[idx_mistral % len(lista_mistral)]}", "Content-Type": "application/json"}
                            payload = {"model": "mistral-tiny", "messages": [{"role": "user", "content": prompt_sistema}]}
                            res = requests.post("https://mistral.ai", json=payload, headers=headers).json()
                            texto_completo = res["choices"][0]["message"]["content"]
                        except: idx_mistral += 1

                # MOTOR 4: COHERE (INTEGRAÇÃO DIRETA VIA API HTTP)
                if not texto_completo and lista_cohere:
                    with st.spinner(f"🔮 [Ciclo {execucoes}] Acionando Motor 4 (Cohere)..."):
                        try:
                            headers = {"Authorization": f"Bearer {lista_cohere[idx_cohere % len(lista_cohere)]}", "Content-Type": "application/json"}
                            payload = {"model": "command-r-plus", "message": prompt_sistema}
                            res = requests.post("https://cohere.com", json=payload, headers=headers).json()
                            texto_completo = res["text"]
                        except: idx_cohere += 1

                # MOTOR 5: HUGGING FACE (SISTEMA DE FORTALEZA DE CÓDIGO ABERTO)
                if not texto_completo and lista_hf:
                    with st.spinner(f"🛡️ [Ciclo {execucoes}] Acionando Motor 5 (Hugging Face)..."):
                        try:
                            headers = {"Authorization": f"Bearer {lista_hf[idx_hf % len(lista_hf)]}"}
                            payload = {"inputs": prompt_sistema}
                            # Usa o modelo de alta performance Llama-3 da Meta hospedado de graça na Hugging Face
                            res = requests.post("https://huggingface.co", json=payload, headers=headers).json()
                            texto_completo = res[0]["generated_text"]
                        except: idx_hf += 1

                # CONSOLIDAR RESULTADO E SALVAR NA PLANILHA
                if texto_completo:
                    if "NOME:" in texto_completo:
                        for linha in texto_completo.split("\n"):
                            if linha.startswith("NOME:"):
                                nome_produto = linha.replace("NOME:", "").strip()
                                break
                    
                    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
