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
# 1) ESTILIZAÇÃO MODO ESCURO / CYBERPUNK (PILAR 1)
# ==============================================================================
st.set_page_config(page_title="Império Cibernético v7.0", page_icon="⚡", layout="centered")

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

st.title("⚡ IMPÉRIO CIBERNÉTICO V7.0")
st.write("Central Soberana: Inteligência Evolutiva, Landing Pages Automáticas e Automação Residencial.")

ARQUIVO_BANCO = "banco_de_relatorios.csv"

# Preservação de estados na memória do navegador
if "gemini_lista" not in st.session_state: st.session_state.gemini_lista = ""
if "groq_lista" not in st.session_state: st.session_state.groq_lista = ""

# ==============================================================================
# PAINEL LATERAL DE CREDENCIAIS
# ==============================================================================
st.sidebar.header("🔑 Banco de Energia (Chaves)")
input_gemini = st.sidebar.text_area("Lista de Gemini API Keys", value=st.session_state.gemini_lista)
input_groq = st.sidebar.text_area("Lista de Groq API Keys", value=st.session_state.groq_lista)

st.session_state.gemini_lista = input_gemini
st.session_state.groq_lista = input_groq

lista_gemini = [k.strip() for k in input_gemini.split(",") if k.strip()]
lista_groq = [k.strip() for k in input_groq.split(",") if k.strip()]

# ==============================================================================
# NAVEGAÇÃO ENTRE MÓDULOS (Abas do Aplicativo)
# ==============================================================================
aba_gerador, aba_vendas, aba_fisica = st.tabs(["🧠 Laboratório Generativo", "🏪 Máquina de Vendas (Landing Page)", "🔌 Engenharia Maker Física"])

# ------------------------------------------------------------------------------
# ABA 1: LABORATÓRIO GENERATIVO (Loop Infinito Evolutivo)
# ------------------------------------------------------------------------------
with aba_gerador:
    st.subheader("⚙️ Loop Generativo Quântico")
    modo_infinito = st.toggle("🔄 ATIVAR OPERAÇÃO INTELIGENTE GENERATIVA INFINITA")

    if st.button("🚀 INICIAR OPERAÇÃO AUTÔNOMA", use_container_width=True) or modo_infinito:
        if not lista_gemini and not lista_groq:
            st.error("❌ Erro: Insira pelo menos uma chave de IA válida na barra lateral.")
        else:
            execucoes = 0
            idx_gemini = 0
            idx_groq = 0
            
            while True:
                execucoes += 1
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

                prompt_sistema = f"Tempo: {time.time()}. Histórico: [{historico_total}]. Projete um NOVO dispositivo focado em ENERGIA AUTOSSUSTENTÁVEL ou CIBERNÉTICA. Na PRIMEIRA LINHA responda apenas: 'NOME: [Nome da Invenção]'."

                if lista_gemini:
                    with st.spinner(f"🧠 [Ciclo {execucoes}] Processando via Google..."):
                        try:
                            client = genai.Client(api_key=lista_gemini[idx_gemini % len(lista_gemini)])
                            texto_completo = client.models.generate_content(model='gemini-2.5-flash', contents=prompt_sistema).text
                        except:
                            idx_gemini += 1
                
                if not texto_completo and lista_groq:
                    with st.spinner(f"⚠️ Redundância: Processando via Groq..."):
                        try:
                            client_groq = Groq(api_key=lista_groq[idx_groq % len(lista_groq)])
                            texto_completo = client_groq.chat.completions.create(messages=[{"role": "user", "content": prompt_sistema}], model="llama-3.1-8b-instant").choices.message.content
                        except:
                            idx_groq += 1

                if texto_completo:
                    if "NOME:" in texto_completo:
                        for linha in texto_completo.split("\n"):
                            if linha.startswith("NOME:"):
                                nome_produto = linha.replace("NOME:", "").strip()
                                break
                    
                    # Salva na planilha de dados
                    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    nova_linha = pd.DataFrame([{"Data/Hora": data_atual, "Invenção": nome_produto, "Projeto de Engenharia": texto_completo}])
                    if os.path.exists(ARQUIVO_BANCO):
                        try: df_final = pd.concat([pd.read_csv(ARQUIVO_BANCO), nova_linha], ignore_index=True)
                        except: df_final = nova_linha
                    else: df_final = nova_linha
                    df_final.to_csv(ARQUIVO_BANCO, index=False)
                    
                    st.success(f"🔥 Invenção '{nome_produto}' integrada com sucesso!")
                    st.write(texto_completo)
                else:
                    st.error("Todas as chaves esgotadas.")
                    break

                if not modo_infinito: break
                time.sleep(15)
                st.rerun()

# ------------------------------------------------------------------------------
# ABA 2: MÁQUINA DE VENDAS (FÁBRICA DE LANDING PAGES - PILAR 2)
# ------------------------------------------------------------------------------
with aba_vendas:
    st.subheader("🏪 Estrutura Comercial Automática")
    if os.path.exists(ARQUIVO_BANCO):
        df_v = pd.read_csv(ARQUIVO_BANCO)
        if not df_v.empty:
            ultima_inv = df_v.iloc[-1]
            nome_inv = str(ultima_inv.get("Invenção", "AetherFlux Generator"))
            detalhes_inv = str(ultima_inv.get("Projeto de Engenharia", ""))
            
            st.write(f"Gerando Página de Alta Conversão para: **{nome_inv}**")
            
            # Código visual simulado da Landing Page pronto para exibição
            st.markdown(f"""
            <div style="background-color: #1a1c29; padding: 25px; border-radius: 10px; border: 2px solid #00ff66; text-align: center;">
                <h1 style="color: #00ff66 !important;">{nome_inv.upper()}</h1>
                <p style="color: #ffffff; font-size: 18px;">A Revolução Definitiva em Energia Livre e Autossustentável</p>
                <div style="background-color: #0d0e15; padding: 15px; border-radius: 5px; color: #8a2be2; margin: 15px 0; font-weight: bold;">
                    ⚡ GARANTA SUA INDEPENDÊNCIA ENERGÉTICA AGORA!
                </div>
                <button style="width: 100%; padding: 12px; background-color: #00ff66; border: none; font-weight: bold; border-radius: 5px; color: #0d0e15;">
                    ADQUIRIR PROJETO TÉCNICO COMPLETO (PDF)
                </button>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Execute uma operação laboratorial primeiro para coletar os produtos de venda.")
    else:
        st.info("Aguardando geração de dados na planilha.")

# ------------------------------------------------------------------------------
# ABA 3: ENGENHARIA MAKER FÍSICA (PLANO DA CASA AUTOMÁTICA - PILAR 3)
# ------------------------------------------------------------------------------
with aba_fisica:
    st.subheader("🔌 Central de Comando Residencial Remoto (Simulador)")
    st.write("Mapeamento lógico para integrar o seu celular a interruptores físicos reais (Sonoff/Arduino).")
    
    col1, col2 = st.columns(2)
    with col1:
        lampada = st.toggle("💡 Lâmpada do Laboratório Quântico")
        if lampada: st.success("🟢 Comando Enviado: Lâmpada LIGADA remotamente via Nuvem!")
        else: st.info("🔴 Status: Lâmpada DESLIGADA")
        
    with col2:
        rele_motor = st.toggle("⚡ Alimentação Principal do Gerador")
        if rele_motor: st.success("🟢 Relé de Alta Potência: ATIVADO!")
        else: st.info("🔴 Status: Relé em Repouso")

    st.markdown("---")
    st.write("🛒 **Lista de Componentes Recomendados para Iniciar Prática Física:**")
    st.markdown("*   **[Módulo Interruptor Inteligente Sonoff MINI](https://google.com)** - Para embutir na parede e controlar luzes.")
    st.markdown("*   **[Tomada Inteligente Wi-Fi Tuya](https://google.com)** - Para controlar qualquer aparelho de tomada de forma remota.")
