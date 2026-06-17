import streamlit as st
import os
import requests
import pandas as pd
import time
from datetime import datetime
from google import genai
from fpdf import FPDF

# Configuração da Página do Aplicativo (Visual do Celular)
st.set_page_config(page_title="Cibernética Autônoma v5.0", page_icon="⚡", layout="centered")

st.title("⚡ Império Cibernético Autônomo v5.0")
st.write("Geração infinita de Energia Autossustentável e Cibernética com exportação comercial em PDF.")

# Arquivo local de banco de dados
ARQUIVO_BANCO = "banco_de_relatorios.csv"

# ==============================================================================
# PAINEL DE CREDENCIAIS (ENTRADA SEGURA)
# ==============================================================================
st.sidebar.header("🔑 Chaves de Ativação")
gemini_key = st.sidebar.text_input("Gemini API Key (Principal Grátis)", type="password")
telegram_token = st.sidebar.text_input("Telegram Bot Token (Opcional)", type="password", help="Para avisos no celular")
telegram_chat_id = st.sidebar.text_input("Telegram Chat ID (Opcional)", type="password")

# ==============================================================================
# FUNÇÃO PARA GERAR PDF PROFISSIONAL COMERCIAL (PILAR 1)
# ==============================================================================
def criar_pdf_comercial(titulo, conteudo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    # Título do Documento
    pdf.cell(0, 10, f"PATENTE CONCEITUAL: {titulo}", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 12)
    # Conteúdo com quebra automática de linha para não cortar o texto
    pdf.multi_cell(0, 10, txt=conteudo.encode('utf-8', 'ignore').decode('utf-8'))
    return pdf.output()

# ==============================================================================
# FUNÇÃO PARA ENVIAR ALERTA NO SEU CELULAR (PILAR 2)
# ==============================================================================
def enviar_aviso_celular(token, chat_id, mensagem):
    if token and chat_id:
        url = f"https://telegram.org{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": mensagem}
        try: requests.post(url, json=payload)
        except: pass

# ==============================================================================
# FUNÇÃO PARA SALVAR AUTOMATICAMENTE NA PLANILHA
# ==============================================================================
def salvar_na_planilha(produto, detalhes):
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    nova_linha = pd.DataFrame([{
        "Data/Hora": data_atual,
        "Invenção": produto,
        "Projeto de Engenharia": detalhes
    }])
    if os.path.exists(ARQUIVO_BANCO):
        df_existente = pd.read_csv(ARQUIVO_BANCO)
        df_final = pd.concat([df_existente, nova_linha], ignore_index=True)
    else:
        df_final = nova_linha
    df_final.to_csv(ARQUIVO_BANCO, index=False)
    return df_final

# ==============================================================================
# CONTROLES DO LOOP GENERATIVO FOCO CIBERNÉTICA E ENERGIA (PILAR 3)
# ==============================================================================
st.subheader("⚙️ Configuração da Mente Generativa")
modo_infinito = st.toggle("🔄 ATIVAR OPERAÇÃO INTELIGENTE INFINITA")

if st.button("🚀 INICIAR OPERAÇÃO AUTÔNOMA", use_container_width=True) or modo_infinito:
    if not gemini_key:
        st.error("❌ ERRO CRÍTICO: Insira a sua Gemini API Key para ativar as máquinas.")
    else:
        execucoes = 0
        while True:
            execucoes += 1
            texto_completo = ""
            nome_produto = "Dispositivo Desconhecido"
            
            # MEMÓRIA HISTÓRICA CUMULATIVA
            historico_total = "Nenhuma invenção criada ainda."
            if os.path.exists(ARQUIVO_BANCO):
                try:
                    df_historico = pd.read_csv(ARQUIVO_BANCO)
                    if not df_historico.empty:
                        historico_total = ", ".join(df_historico["Invenção"].astype(str).tolist())
                except: pass

            # DIRETRIZ MESTRE ULTRA-CIENTÍFICA (PILAR 3)
            prompt_sistema = f"""
            Instante do tempo: {time.time()}
            Histórico de tecnologia já criada: [{historico_total}]
            
            Você é uma inteligência artificial líder em engenharia reversa, cibernética e física quântica.
            Sua missão é projetar um NOVO dispositivo ou motor focado estritamente em ENERGIA AUTOSSUSTENTÁVEL, CIBERNÉTICA ou CAPTAÇÃO LIVRE.
            Você deve analisar o histórico de tecnologia para acumular sabedoria e propor um avanço evolutivo direto, adicionando melhorias sem nunca retroceder.
            
            Estruture o relatório em:
            1. Nome do Dispositivo.
            2. Debate científico da equipe de gênios.
            3. 5 Melhorias brutais de física e mecânica aplicadas.
            4. Roteiro curto de vendas comerciais (Até 200 letras).
            
            Na PRIMEIRA LINHA da resposta, escreva APENAS: 'NOME: [Nome da Invenção]'.
            """

            with st.spinner(f"🧠 [Ciclo {execucoes}] Cientistas processando alta engenharia quântica..."):
                try:
                    client = genai.Client(api_key=gemini_key)
                    response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt_sistema)
                    texto_completo = response.text
                except Exception as err:
                    st.error(f"Erro na rede: {err}")
                    break

            if texto_completo:
                if "NOME:" in texto_completo:
                    for linha in texto_completo.split("\n"):
                        if linha.startswith("NOME:"):
                            nome_produto = linha.replace("NOME:", "").strip()
                            break
                
                salvar_na_planilha(nome_produto, texto_completo)
                st.success(f"🔥 Invenção '{nome_produto}' integrada com sucesso!")
                st.write(texto_completo)
                
                # Dispara Alerta para o seu celular (Pilar 2)
                if telegram_token and telegram_chat_id:
                    enviar_aviso_celular(telegram_token, telegram_chat_id, f"⚡ ALERTA DE ALTA PATENTE CRUCIAL:\nNova invenção gerada: {nome_produto}\nVerifique seu painel visual!")

            if not modo_infinito:
                break
                
            time.sleep(15)
            st.rerun()

# ==============================================================================
# PAINEL DE EXPORTAÇÃO COMERCIAL E BANCO DE DADOS (PILAR 1)
# ==============================================================================
st.markdown("---")
st.subheader("📋 Banco de Dados de Patentes Cumulativas")
if os.path.exists(ARQUIVO_BANCO):
    df_visualizacao = pd.read_csv(ARQUIVO_BANCO)
    st.metric(label="Patentes Salvas na Memória", value=len(df_visualizacao))
    st.dataframe(df_visualizacao)
    
    # PEGA A ÚLTIMA INVENÇÃO PARA EXPORTAR EM PDF PROFISSIONAL (PILAR 1)
    ultima_inv = df_visualizacao.iloc[-1]
    nome_pdf = str(ultima_inv["Invenção"])
    conteudo_pdf = str(ultima_inv["Projeto de Engenharia"])
    
    pdf_bytes = criar_pdf_comercial(nome_pdf, conteudo_pdf)
    st.download_button(
        label="📄 BAIXAR RELATÓRIO DA ÚLTIMA INVENÇÃO EM PDF COMERCIAL",
        data=pdf_bytes,
        file_name=f"patente_{nome_pdf.lower().replace(' ', '_')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
    
    csv_data = df_visualizacao.to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 BAIXAR PLANILHA COMPLETA (CSV)", data=csv_data, file_name="historico_ia_autonoma.csv", mime="text/csv", use_container_width=True)
