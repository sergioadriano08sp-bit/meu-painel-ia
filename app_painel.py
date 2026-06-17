import streamlit as st
import os
import requests
import pandas as pd
import time
from datetime import datetime
from google import genai
from langchain_groq import ChatGroq

# Configuração da Página do Aplicativo (Visual do Celular)
st.set_page_config(page_title="Cibernética Autônoma v4.0", page_icon="🤖", layout="centered")

st.title("🤖 Máquina Viva v4.0: Memória Evolutiva & Curadoria")
st.write("Ecossistema cibernético auto-construtivo que acumula sabedoria e destaca as melhores patentes.")

# Arquivo local que serve como banco de dados
ARQUIVO_BANCO = "banco_de_relatorios.csv"

# ==============================================================================
# PAINEL DE CREDENCIAIS (ENTRADA SEGURA)
# ==============================================================================
st.sidebar.header("🔑 Chaves de Ativação")
gemini_key = st.sidebar.text_input("1) Gemini API Key (Principal Grátis)", type="password")
groq_key = st.sidebar.text_input("2) Groq API Key (Reserva Grátis)", type="password")
heygen_key = st.sidebar.text_input("HeyGen API Key (Teste Grátis)", type="password")
eleven_key = st.sidebar.text_input("ElevenLabs API Key (Plano Grátis)", type="password")

# ==============================================================================
# FUNÇÃO PARA SALVAR AUTOMATICAMENTE NA PLANILHA
# ==============================================================================
def salvar_na_planilha(produto, detalhes):
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    nova_linha = pd.DataFrame([{
        "Data/Hora": data_atual,
        "Produto Identificado": produto,
        "Relatório Completo de Engenharia": detalhes
    }])
    if os.path.exists(ARQUIVO_BANCO):
        df_existente = pd.read_csv(ARQUIVO_BANCO)
        df_final = pd.concat([df_existente, nova_linha], ignore_index=True)
    else:
        df_final = nova_linha
    df_final.to_csv(ARQUIVO_BANCO, index=False)
    return df_final

# ==============================================================================
# INTERFACE DA CRIAÇÃO DO PAINEL DE DESTAQUE
# ==============================================================================
if os.path.exists(ARQUIVO_BANCO):
    df_verificacao = pd.read_csv(ARQUIVO_BANCO)
    if not df_verificacao.empty and (gemini_key or groq_key):
        st.markdown("### 🏆 Invenção em Destaque (Alta Patente)")
        
        # O Cérebro avalia a planilha atualizada para escolher o melhor
        chave_ativa = gemini_key if gemini_key else groq_key
        prompt_curadoria = f"Aqui está a lista de invenções geradas: {df_verificacao['Produto Identificado'].tolist()}. Escolha estritamente uma única que tenha o maior impacto de engenharia e justifique resumidamente em duas linhas o porquê."
        
        try:
            if gemini_key:
                client_c = genai.Client(api_key=gemini_key)
                destaque_res = client_c.models.generate_content(model='gemini-2.5-flash', contents=prompt_curadoria).text
            else:
                llm_res = ChatGroq(groq_api_key=groq_key, model_name="llama3-8b-8192")
                destaque_res = llm_res.invoke(prompt_curadoria).content
                
            st.info(destaque_res)
        except:
            st.info("Avaliando o histórico de dados...")

# ==============================================================================
# CONTROLES DO LOOP INFINITO AUTO-CONSTRUTIVO
# ==============================================================================
st.markdown("---")
st.subheader("⚙️ Configuração do Loop Generativo")
modo_infinito = st.toggle("🔄 ATIVAR OPERAÇÃO INTELIGENTE GENERATIVA INFINITA")

if st.button("🚀 INICIAR OPERAÇÃO AUTÔNOMA", use_container_width=True) or modo_infinito:
    if not gemini_key and not groq_key:
        st.error("❌ ERRO CRÍTICO: Insira pelo menos uma Chave de IA (Gemini ou Groq) para iniciar.")
    else:
        execucoes = 0
        while True:
            execucoes += 1
            texto_completo = ""
            nome_produto = "Produto Desconhecido"
            
            # SISTEMA DE MEMÓRIA COMPLETO (Recupera todas as criações anteriores)
            historico_total = "Nenhuma invenção no banco de dados ainda."
            if os.path.exists(ARQUIVO_BANCO):
                try:
                    df_historico = pd.read_csv(ARQUIVO_BANCO)
                    if not df_historico.empty:
                        historico_total = ", ".join(df_historico["Produto Identificado"].astype(str).tolist())
                except:
                    pass

            # Prompt de auto-evolução dependente construtiva
            prompt_sistema = f"""
            Instante do tempo cibernético: {time.time()}
            Histórico completo de patentes geradas nesta máquina: [{historico_total}]
            
            Você é uma inteligência artificial genial e auto-construtiva. 
            Instrução Mestre: Projete uma nova invenção de consumo. Você nunca deve replicar ou reduzir o nível do histórico fornecido. Analise o que já foi inventado e use como base para criar algo ainda mais inteligente, adicionando melhorias cumulativas e de alta engenharia, sem nunca retroceder.
            
            Entregue o debate científico contendo:
            1. O novo produto evolutivo de foco.
            2. 5 melhorias conceituais brutais e acumulativas.
            3. Roteiro persuasivo final para automação de vídeo com menos de 200 letras.
            
            Na PRIMEIRA LINHA da sua resposta, escreva APENAS o nome do produto usando o rótulo 'NOME: [Nome aqui]'.
            """

            # EXECUÇÃO DO ENXAME DE DOIS CÉREBROS (Google e Groq)
            try:
                if gemini_key:
                    with st.spinner(f"🧠 [Ciclo {execucoes}] Cérebro Google processando evolução..."):
                        client = genai.Client(api_key=gemini_key)
                        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt_sistema)
                        texto_completo = response.text
                else:
                    raise Exception("Pulando para Groq")
            except Exception as e:
                if groq_key:
                    with st.spinner(f"⚠️ Redundância: Cérebro Groq processando evolução..."):
                        llm_resva = ChatGroq(groq_api_key=groq_key, model_name="llama3-8b-8192")
                        texto_completo = llm_resva.invoke(prompt_sistema).content
                else:
                    st.error("Todas as opções de cota foram esgotadas. Insira a chave da Groq.")
                    break

            # TRATAMENTO DE REGISTRO E FEEDBACK
            if texto_completo:
                if "NOME:" in texto_completo:
                    for linha in texto_completo.split("\n"):
                        if linha.startswith("NOME:"):
                            nome_produto = linha.replace("NOME:", "").strip()
                            break
                
                salvar_na_planilha(nome_produto, texto_completo)
                st.success(f"🔥 Ciclo {execucoes} Concluído: '{nome_produto}' integrado à sabedoria de rede.")
                st.write(texto_completo)
                
                # Desparos multimídia automáticos
                if heygen_key:
                    try: requests.post("https://heygen.com", json={"input_text": texto_completo[:200]}, headers={"X-Api-Key": heygen_key})
                    except: pass

            if not modo_infinito:
                break
                
            time.sleep(15) # Tempo de resfriamento da rede
            st.rerun()

# ==============================================================================
# EXIBIÇÃO DA PLANILHA DO BANCO DE DADOS
# ==============================================================================
st.markdown("---")
st.subheader("📋 Banco de Dados de Invenções Cumulativas")
if os.path.exists(ARQUIVO_BANCO):
    df_visualizacao = pd.read_csv(ARQUIVO_BANCO)
    st.metric(label="Invenções Guardadas na Memória", value=len(df_visualizacao))
    st.dataframe(df_visualizacao)
    csv_data = df_visualizacao.to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 BAIXAR PLANILHA COMPLETA", data=csv_data, file_name="historico_ia_autonoma.csv", mime="text/csv", use_container_width=True)
