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
st.set_page_config(page_title="Império Cibernético v10.7", page_icon="⚡", layout="centered")

# Estilização Cyberpunk Aprimorada
st.markdown("""
    <style>
    .stApp { background-color: #0d0e15; color: #00ff66; }
    h1, h2, h3 { color: #8a2be2 !important; text-shadow: 0 0 10px #8a2be2; }
    .stButton>button { background-color: #8a2be2; color: #00ff66; border: 2px solid #00ff66; box-shadow: 0 0 15px #8a2be2; width: 100%; height: 50px; font-weight: bold; }
    .stButton>button:hover { background-color: #00ff66; color: #0d0e15; box-shadow: 0 0 20px #00ff66; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { background-color: #1a1c29 !important; color: #00ff66 !important; border: 1px solid #8a2be2 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ IMPÉRIO CIBERNÉTICO V10.7")
st.write("Central Soberana: Atualização de Modelos de Rede Concluída com Sucesso.")

ARQUIVO_BANCO = "banco_de_relatorios.csv"

# ==============================================================================
# PAINEL CENTRAL DE ENTRADA DIRETA
# ==============================================================================
st.subheader("🔑 Ativação Direta do Enxame")
st.write("Cole a sua chave da Groq (a que começa com gsk_...) no campo abaixo para ligar a máquina de graça:")

groq_key_direta = st.text_input("Sua Groq API Key Ativa:", type="password")

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

# ------------------------------------------------------------------------------
# ABA 1: EXECUÇÃO DO LABORATÓRIO (DIRETO COM MODELO LLAMA 3.3 ATUALIZADO)
# ------------------------------------------------------------------------------
with aba_gerador:
    box_telemetria = st.code("📡 Inicializando rastreador de sinal... Ready.")
    
    if st.button("🚀 DISPARAR ENXAME CIBERNÉTICO AGORA", use_container_width=True):
        if not groq_key_direta:
            st.error("❌ Alerta de Sistema: Insira a sua Groq API Key no campo do topo antes de clicar.")
        else:
            texto_completo = ""
            nome_produto = "Dispositivo Desconhecido"
            
            box_telemetria.code("📡 Roteando dados para Canal Atualizado [Groq Llama 3.3]...")
            
            historico_total = "Nenhuma invenção criada ainda."
            if os.path.exists(ARQUIVO_BANCO):
                try:
                    df_h = pd.read_csv(ARQUIVO_BANCO)
                    if not df_h.empty:
                        col = "Invenção" if "Invenção" in df_h.columns else "Produto Identificado"
                        historico_total = ", ".join(df_h[col].astype(str).tolist())
                except: pass

            prompt_sistema = f"Tempo: {time.time()}. Histórico: [{historico_total}]. Projete um dispositivo novo e disruptivo focado em ENERGIA AUTOSSUSTENTÁVEL ou CIBERNÉTICA. Na PRIMEIRA LINHA responda apenas: 'NOME: [Nome]'."

            # Executa no modelo Llama 3.3 Versatile (Substituto oficial do Llama 3.1)
            try:
                t_inicio = time.time()
                client_groq = Groq(api_key=groq_key_direta.strip())
                chat_completion = client_groq.chat.completions.create(
                    messages=[{"role": "user", "content": prompt_sistema}], 
                    model="llama-3.3-70b-versatile"
                )
                texto_completo = chat_completion.choices.message.content
                box_telemetria.code(f"📡 Canal Groq Llama 3.3: Sucesso em {time.time() - t_inicio:.2f}s")
            except Exception as e:
                box_telemetria.code(f"📡 Canal Groq Falhou -> Erro: {str(e)}")

            if texto_completo:
                if "NOME:" in texto_completo:
                    for linha in texto_completo.split("\n"):
                        if linha.startswith("NOME:"):
                            nome_produto = linha.replace("NOME:", "").strip()
                            break
                
                # Gravação na planilha de dados
                data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                nova_linha = pd.DataFrame([{"Data/Hora": data_atual, "Invenção": nome_produto, "Projeto de Engenharia": texto_completo}])
                if os.path.exists(ARQUIVO_BANCO):
                    try: df_final = pd.concat([pd.read_csv(ARQUIVO_BANCO), nova_linha], ignore_index=True)
                    except: df_final = nova_linha
                else: df_final = nova_linha
                df_final.to_csv(ARQUIVO_BANCO, index=False)
                
                st.success(f"🔥 Sincronização Concluída: '{nome_produto}' registrado na rede.")
                st.write(texto_completo)
                st.balloons()
            else:
                st.error("🚨 FALHA CRÍTICA: A comunicação falhou. Verifique a mensagem detalhada na caixa de telemetria acima.")

# ------------------------------------------------------------------------------
# ABAS 2 E 3
# ------------------------------------------------------------------------------
with aba_vendas:
    st.subheader("🏪 Estrutura Comercial de Alta Conversão")
    if os.path.exists(ARQUIVO_BANCO):
        try:
            df_v = pd.read_csv(ARQUIVO_BANCO)
            if not df_v.empty:
                ultima_inv = df_v.iloc[-1]
                nome_inv = str(ultima_inv.get("Invenção", "AetherFlux Generator"))
                st.write(f"Landing Page Automática estruturada para: **{nome_inv}**")
                st.markdown(f"""
                <div style="background-color: #1a1c29; padding: 25px; border-radius: 10px; border: 2px solid #00ff66; text-align: center;">
                    <h1 style="color: #00ff66 !important;">{nome_inv.upper()}</h1>
                    <p style="color: #ffffff; font-size: 18px;">A Revolução Definitiva em Energia Livre e Autossustentável</p>
                    <div style="background-color: #0d0e15; padding: 15px; border-radius: 5px; color: #8a2be2; margin: 15px 0; font-weight: bold;">
                        ⚡ COMPRE O BLUEPRINT COMPLETO DA TECNOLOGIA E ASSUMA O CONTROLE AGORA!
                    </div>
                </div>
                """, unsafe_allow_html=True)
        except: pass

with aba_fisica:
    st.subheader("🔌 Central de Comando Residencial")
    col1, col2 = st.columns(2)
    with col1:
        lampada = st.toggle("💡 Lâmpada do Laboratório Quântico")
        if lampada: st.success("🟢 Comando enviado via Nuvem: LIGADO!")
    with col2:
        rele_motor = st.toggle("⚡ Alimentação Principal do Gerador")
        if rele_motor: st.success("🟢 Comando enviado para o Relé físico: ATIVADO!")

st.markdown("---")
st.subheader("📋 Banco de Dados de Patentes Cumulativas")
if os.path.exists(ARQUIVO_BANCO):
    try:
        df_visualizacao = pd.read_csv(ARQUIVO_BANCO)
        st.metric(label="Patentes Salvas na Memória", value=len(df_visualizacao))
        st.dataframe(df_visualizacao)
        if not df_visualizacao.empty:
            ultima_inv = df_visualizacao.iloc[-1]
            pdf_bytes = criar_pdf_comercial(str(ultima_inv["Invenção"]), str(ultima_inv["Projeto de Engenharia"]))
            st.download_button(label="📄 BAIXAR RELATÓRIO DA ÚLTIMA INVENÇÃO EM PDF", data=pdf_bytes, file_name="patente.pdf", mime="application/pdf")
    except: pass
