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
st.set_page_config(page_title="Cibernética Autônoma v5.3", page_icon="⚡", layout="centered")

st.title("⚡ Império Cibernético Autônomo v5.3")
st.write("Geração infinita de Energia Autossustentável e Cibernética com exportação comercial em PDF.")

# Arquivo local de banco de dados
ARQUIVO_BANCO = "banco_de_relatorios.csv"

# ==============================================================================
# PAINEL DE CREDENCIAIS COMPLETO
# ==============================================================================
st.sidebar.header("🔑 Chaves de Ativação")
gemini_key = st.sidebar.text_input("1) Gemini API Key (Principal Grátis)", type="password")
groq_key = st.sidebar.text_input("2) Groq API Key (Reserva Grátis)", type="password")
heygen_key = st.sidebar.text_input("3) HeyGen API Key (Teste Grátis)", type="password")
eleven_key = st.sidebar.text_input("4) ElevenLabs API Key (Plano Grátis)", type="password")

st.sidebar.markdown("---")
st.sidebar.header("📱 Notificações Opcionais")
telegram_token = st.sidebar.text_input("Telegram Bot Token", type="password")
telegram_chat_id = st.sidebar.text_input("Telegram Chat ID", type="password")

# ==============================================================================
# FUNÇÃO PARA GERAR PDF PROFISSIONAL COMERCIAL
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

# ==============================================================================
# FUNÇÃO PARA ENVIAR ALERTA NO SEU CELULAR
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
        try:
            df_existente = pd.read_csv(ARQUIVO_BANCO)
            if "Produto Identificado" in df_existente.columns:
                df_existente = df_existente.rename(columns={"Produto Identificado": "Invenção"})
            if "Relatório Completo de Engenharia" in df_existente.columns:
                df_existente = df_existente.rename(columns={"Relatório Completo de Engenharia": "Projeto de Engenharia"})
            df_final = pd.concat([df_existente, nova_linha], ignore_index=True)
        except:
            df_final = nova_linha
    else:
        df_final = nova_linha
    df_final.to_csv(ARQUIVO_BANCO, index=False)
    return df_final

# ==============================================================================
# CONTROLES DO LOOP GENERATIVO FOCO CIBERNÉTICA E ENERGIA
# ==============================================================================
st.subheader("⚙️ Configuração da Mente Generativa")
modo_infinito = st.toggle("🔄 ATIVAR OPERAÇÃO INTELIGENTE INFINITA")

if st.button("🚀 INICIAR OPERAÇÃO AUTÔNOMA", use_container_width=True) or modo_infinito:
    if not gemini_key and not groq_key:
        st.error("❌ ERRO CRÍTICO: Insira pelo menos uma chave de IA (Gemini ou Groq) para ativar.")
    else:
        execucoes = 0
        while True:
            execucoes += 1
            texto_completo = ""
            nome_produto = "Dispositivo Desconhecido"
            
            historico_total = "Nenhuma invenção criada ainda."
            if os.path.exists(ARQUIVO_BANCO):
                try:
                    df_historico = pd.read_csv(ARQUIVO_BANCO)
                    if not df_historico.empty:
                        coluna_busca = "Invenção" if "Invenção" in df_historico.columns else "Produto Identificado"
                        historico_total = ", ".join(df_historico[coluna_busca].astype(str).tolist())
                except: pass

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

            # TENTATIVA 1: RODA NO GEMINI
            try:
                if gemini_key:
                    with st.spinner(f"🧠 [Ciclo {execucoes}] Cérebro Google processando alta engenharia..."):
                        client = genai.Client(api_key=gemini_key)
                        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt_sistema)
                        texto_completo = response.text
                else:
                    raise Exception("Acessando redundância da Groq")
            except:
                # TENTATIVA 2: SE O GEMINI FALHAR, ACIONA O CLIENTE DIRETO E OFICIAL DA GROQ (INFALÍVEL)
                if groq_key:
                    with st.spinner(f"⚠️ Redundância: Cérebro Groq Oficial processando evolução..."):
                        try:
                            client_groq = Groq(api_key=groq_key)
                            chat_completion = client_groq.chat.completions.create(
                                messages=[{"role": "user", "content": prompt_sistema}],
                                model="llama3-8b-8192",
                            )
                            texto_completo = chat_completion.choices[0].message.content
                        except Exception as erro_interno_groq:
                            st.error(f"Falha na API da Groq: {erro_interno_groq}")
                            break
                else:
                    st.error("Sem chaves disponíveis para execução. Insira a sua Groq API Key ativa.")
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
                
                if telegram_token and telegram_chat_id:
                    enviar_aviso_celular(telegram_token, telegram_chat_id, f"⚡ NOVA PATENTE GERADA:\n{nome_produto}")

            if not modo_infinito:
                break
                
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
        if "Produto Identificado" in df_visualizacao.columns:
            df_visualizacao = df_visualizacao.rename(columns={"Produto Identificado": "Invenção"})
        if "Relatório Completo de Engenharia" in df_visualizacao.columns:
            df_visualizacao = df_visualizacao.rename(columns={"Relatório Completo de Engenharia": "Projeto de Engenharia"})
        
        st.metric(label="Patentes Salvas na Memória", value=len(df_visualizacao))
        st.dataframe(df_visualizacao)
        
        if not df_visualizacao.empty:
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
    except:
