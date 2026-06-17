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
st.set_page_config(page_title="Império Cibernético v6.0", page_icon="⚡", layout="centered")

st.title("⚡ Máquina Viva v6.0: Energia Generativa Infinita")
st.write("Sistema auto-sustentável com revezamento de chaves e salvamento automático de credenciais.")

# Arquivo local de banco de dados
ARQUIVO_BANCO = "banco_de_relatorios.csv"

# ==============================================================================
# SISTEMA DE MEMÓRIA DE CHAVES DO NAVEGADOR (Para não precisar digitar sempre)
# ==============================================================================
if "gemini_lista" not in st.session_state: st.session_state.gemini_lista = ""
if "groq_lista" not in st.session_state: st.session_state.groq_lista = ""
if "heygen_s" not in st.session_state: st.session_state.heygen_s = ""
if "eleven_s" not in st.session_state: st.session_state.eleven_s = ""

# ==============================================================================
# PAINEL DE CREDENCIAIS AVANÇADO (MESA DE REVEZAMENTO)
# ==============================================================================
st.sidebar.header("🔑 Banco de Energia (Chaves de API)")
st.sidebar.write("Adicione várias chaves separadas por vírgula para o revezamento infinito.")

input_gemini = st.sidebar.text_area("Lista de Gemini API Keys", value=st.session_state.gemini_lista, help="Cole suas chaves separadas por vírgula")
input_groq = st.sidebar.text_area("Lista de Groq API Keys", value=st.session_state.groq_lista)
input_heygen = st.sidebar.text_input("HeyGen API Key", value=st.session_state.heygen_s, type="password")
input_eleven = st.sidebar.text_input("ElevenLabs API Key", value=st.session_state.eleven_s, type="password")

# Salva o que foi digitado na memória da sessão atual
st.session_state.gemini_lista = input_gemini
st.session_state.groq_lista = input_groq
st.session_state.heygen_s = input_heygen
st.session_state.eleven_s = input_eleven

# Transforma o texto das caixas em listas reais de chaves limpas
lista_gemini = [k.strip() for k in input_gemini.split(",") if k.strip()]
lista_groq = [k.strip() for k in input_groq.split(",") if k.strip()]

# Exibe o status do banco de energia
st.sidebar.markdown("---")
st.sidebar.subheader("🔋 Status dos Motores")
st.sidebar.write(f"• Motores Gemini Ativos: {len(lista_gemini)}")
st.sidebar.write(f"• Motores Groq Ativos: {len(lista_groq)}")

# ==============================================================================
# FUNÇÕES ESTRUTURAIS (PDF E SALVAMENTO)
# ==============================================================================
def criar_pdf_comercial(titulo, conteudo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, f"PATENTE CONCEITUAL: {titulo}", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 10, txt=conteudo.encode('utf-8', 'ignore').decode('utf-8'))
    return pdf.output()

def salvar_na_planilha(produto, detalhes):
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    nova_linha = pd.DataFrame([{"Data/Hora": data_atual, "Invenção": produto, "Projeto de Engenharia": detalhes}])
    if os.path.exists(ARQUIVO_BANCO):
        try:
            df_ex = pd.read_csv(ARQUIVO_BANCO)
            if "Produto Identificado" in df_ex.columns: df_ex = df_ex.rename(columns={"Produto Identificado": "Invenção"})
            if "Relatório Completo de Engenharia" in df_ex.columns: df_ex = df_ex.rename(columns={"Relatório Completo de Engenharia": "Projeto de Engenharia"})
            df_final = pd.concat([df_ex, nova_linha], ignore_index=True)
        except: df_final = nova_linha
    else:
        df_final = nova_linha
    df_final.to_csv(ARQUIVO_BANCO, index=False)
    return df_final

# ==============================================================================
# MOTOR REVOLUCIONÁRIO DE REVEZAMENTO AUTOMÁTICO INDEPENDENTE
# ==============================================================================
st.subheader("⚙️ Configuração do Loop Generativo")
modo_infinito = st.toggle("🔄 ATIVAR OPERAÇÃO INTELIGENTE GENERATIVA INFINITA")

if st.button("🚀 INICIAR OPERAÇÃO AUTÔNOMA", use_container_width=True) or modo_infinito:
    if not lista_gemini and not lista_groq:
        st.error("❌ ERRO CRÍTICO: Insira pelo menos uma chave de IA válida no menu lateral.")
    else:
        execucoes = 0
        idx_gemini = 0
        idx_groq = 0
        
        while True:
            execucoes += 1
            texto_completo = ""
            nome_produto = "Dispositivo Desconhecido"
            
            # Captura a memória histórica de dados
            historico_total = "Nenhuma invenção criada ainda."
            if os.path.exists(ARQUIVO_BANCO):
                try:
                    df_h = pd.read_csv(ARQUIVO_BANCO)
                    if not df_h.empty:
                        col = "Invenção" if "Invenção" in df_h.columns else "Produto Identificado"
                        historico_total = ", ".join(df_h[col].astype(str).tolist())
                except: pass

            prompt_sistema = f"""
            Tempo cibernético: {time.time()}
            Histórico de tecnologia criada: [{historico_total}]
            Projete um NOVO dispositivo ou motor focado em ENERGIA AUTOSSUSTENTÁVEL, CIBERNÉTICA ou CAPTAÇÃO LIVRE.
            Adicione melhorias sem retroceder. Na PRIMEIRA LINHA responda apenas: 'NOME: [Nome da Invenção]'.
            """

            # TENTATIVA 1: REVEZAMENTO GOOGLE GEMINI
            if lista_gemini:
                chave_atual_gemini = lista_gemini[idx_gemini % len(lista_gemini)]
                with st.spinner(f"🧠 [Ciclo {execucoes}] Usando Chave Gemini #{idx_gemini % len(lista_gemini) + 1}..."):
                    try:
                        client = genai.Client(api_key=chave_atual_gemini)
                        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt_sistema)
                        texto_completo = response.text
                    except Exception as e:
                        st.warning(f"Chave Gemini #{idx_gemini % len(lista_gemini) + 1} esgotada. Rotacionando...")
                        idx_gemini += 1 # Pula para a próxima chave de IA automaticamente se der erro 429
            
            # TENTATIVA 2: REDUNDÂNCIA REVEZAMENTO GROQ
            if not texto_completo and lista_groq:
                chave_atual_groq = lista_groq[idx_groq % len(lista_groq)]
                with st.spinner(f"⚠️ Revezamento Groq: Usando Chave #{idx_groq % len(lista_groq) + 1}..."):
                    try:
                        client_groq = Groq(api_key=chave_atual_groq)
                        chat_completion = client_groq.chat.completions.create(
                            messages=[{"role": "user", "content": prompt_sistema}],
                            model="llama-3.1-8b-instant",
                        )
                        texto_completo = chat_completion.choices.message.content
                    except:
                        st.warning(f"Chave Groq #{idx_groq % len(lista_groq) + 1} esgotada. Rotacionando...")
                        idx_groq += 1

            if texto_completo:
                if "NOME:" in texto_completo:
                    for linha in texto_completo.split("\n"):
                        if linha.startswith("NOME:"):
                            nome_produto = linha.replace("NOME:", "").strip()
                            break
                
                salvar_na_planilha(nome_produto, texto_completo)
                st.success(f"🔥 Invenção '{nome_produto}' integrada à árvore tecnológica!")
                st.write(texto_completo)
            else:
                st.error("❌ Todas as chaves adicionadas no menu de revezamento estão esgotadas por hoje. Adicione mais chaves.")
                break

            if not modo_infinito: break
            time.sleep(15)
            st.rerun()

# ==============================================================================
# PAINEL DE EXPORTAÇÃO COMERCIAL E BANCO DE DADOS
# ==============================================================================
st.markdown("---")
st.subheader("📋 Banco de Dados de Patentes Cumulativas")
if os.path.exists(ARQUIVO_BANCO):
    try:
        df_visualizacao = pd.read_csv(ARQUIVO_BANCO)
        if "Produto Identificado" in df_visualizacao.columns: df_visualizacao = df_visualizacao.rename(columns={"Produto Identificado": "Invenção"})
        if "Relatório Completo de Engenharia" in df_visualizacao.columns: df_visualizacao = df_visualizacao.rename(columns={"Relatório Completo de Engenharia": "Projeto de Engenharia"})
        
        st.metric(label="Patentes Salvas na Memória", value=len(df_visualizacao))
        st.dataframe(df_visualizacao)
        
        if not df_visualizacao.empty:
            ultima_inv = df_visualizacao.iloc[-1]
            pdf_bytes = criar_pdf_comercial(str(ultima_inv["Invenção"]), str(ultima_inv["Projeto de Engenharia"]))
            st.download_button(label="📄 BAIXAR RELATÓRIO DA ÚLTIMA INVENÇÃO EM PDF", data=pdf_bytes, file_name="patente.pdf", mime="application/pdf", use_container_width=True)
        
        csv_data = df_visualizacao.to_csv(index=False).encode('utf-8')
        st.download_button(label="📥 BAIXAR PLANILHA COMPLETA (CSV)", data=csv_data, file_name="historico_ia_autonoma.csv", mime="text/csv", use_container_width=True)
    except: pass
else:
    st.info("A planilha está vazia. Inicie a operação para colher os primeiros relatórios!")
