import streamlit as st
import os
import requests
import pandas as pd
import time
from datetime import datetime
from google import genai

# Configuração da Página do Aplicativo (Visual do Celular)
st.set_page_config(page_title="Cibernética Autônoma", page_icon="🤖", layout="centered")

st.title("🤖 Máquina Autônoma Viva v2.0")
st.write("Ecossistema generativo infinito com salvamento automático em banco de dados.")

# Arquivo local que servirá como nossa planilha de banco de dados
ARQUIVO_BANCO = "banco_de_relatorios.csv"

# ==============================================================================
# PAINEL DE CREDENCIAIS (ENTRADA SEGURA)
# ==============================================================================
st.sidebar.header("🔑 Chaves de Ativação")
gemini_key = st.sidebar.text_input("Gemini API Key (Gratuita do Google)", type="password")
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
        # Se a planilha já existe, lê e adiciona a nova linha no final
        df_existente = pd.read_csv(ARQUIVO_BANCO)
        df_final = pd.concat([df_existente, nova_linha], ignore_index=True)
    else:
        # Se não existe, cria uma nova
        df_final = nova_linha
        
    df_final.to_csv(ARQUIVO_BANCO, index=False)
    return df_final

# ==============================================================================
# CONTROLES DO LOOP INFINITO AUTO-MULTIPLICÁVEL
# ==============================================================================
st.subheader("⚙️ Configuração do Loop Generativo")
modo_infinito = st.toggle("🔄 ATIVAR MODO INFINITO (Execução Sem Fim)")

if modo_infinito:
    st.warning("⚠️ O sistema está em modo Auto-Multiplicável. Ele gerará novos produtos e salvará na planilha sem parar até que você desligue o botão acima.")

# Botão de gatilho manual ou verificação do switch infinito
if st.button("🚀 INICIAR OPERAÇÃO AUTÔNOMA", use_container_width=True) or modo_infinito:
    if not gemini_key:
        st.error("❌ ERRO CRÍTICO: Você precisa colocar a sua Gemini API Key para ativar o cérebro das IAs.")
    else:
        # Se o modo infinito estiver ligado, ele roda em loop. Se não, roda apenas 1 vez.
        execucoes = 0
        while True:
            execucoes += 1
            with st.spinner(f"🧠 [Ciclo {execucoes}] Cientistas virtuais debatendo na rede..."):
                try:
                    client = genai.Client(api_key=gemini_key)
                    
                    # Prompt mestre focado em gerar produtos aleatórios sempre inovadores
                    prompt_sistema = f"""
                    Ciclo atual do sistema: {time.time()}
                    Você é uma equipe de três cientistas gênios trabalhando juntos.
                    Determine um produto de consumo comum atual que esteja viralizando no mercado mas que tenha falhas.
                    O Engenheiro deve criar uma versão 1000x melhor e mais barata de engenharia com 5 tópicos brutais.
                    O Arquiteto deve fazer um roteiro de vendas curto de até 200 letras.
                    Na PRIMEIRA LINHA do seu texto, responda APENAS o nome do produto precedido por 'NOME:'.
                    Nas linhas de baixo, entregue o debate e o projeto detalhado.
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt_sistema,
                    )
                    
                    texto_completo = response.text
                    
                    # Separa o nome do produto para organizar a planilha
                    nome_produto = "Produto Desconhecido"
                    if "NOME:" in texto_completo:
                        linhas = texto_completo.split("\n")
                        for l in linhas:
                            if l.startswith("NOME:"):
                                nome_produto = l.replace("NOME:", "").strip()
                                break
                    
                    # Salva automaticamente na planilha interna
                    df_atualizado = salvar_na_planilha(nome_produto, texto_completo)
                    
                    st.success(f"✅ Ciclo {execucoes} Concluído! '{nome_produto}' guardado na planilha.")
                    st.write(texto_completo)
                    
                    # Disparo opcional dos robôs multimídia (HeyGen/ElevenLabs)
                    if heygen_key:
                        requests.post("https://heygen.com", json={"input_text": texto_completo[:200]}, headers={"X-Api-Key": heygen_key})
                    
                except Exception as err:
                    st.error(f"Falha no ciclo: {err}")
            
            # Se o modo infinito não estiver ativo, sai do loop imediatamente após a primeira execução
            if not modo_infinito:
                break
                
            # Tempo de descanso obrigatório de 10 segundos entre os ciclos para não travar a API gratuita
            time.sleep(10)
            st.rerun()

# ==============================================================================
# PAINEL DA PLANILHA (ÁREA DE LEITURA E DOWNLOAD)
# ==============================================================================
st.markdown("---")
st.subheader("📋 Banco de Dados de Invenções Salvas")

if os.path.exists(ARQUIVO_BANCO):
    df_visualizacao = pd.read_csv(ARQUIVO_BANCO)
    
    # Mostra a quantidade de produtos na memória
    st.metric(label="Total de Invenções na Planilha", value=len(df_visualizacao))
    
    # Exibe a tabela na tela do celular/computador
    st.dataframe(df_visualizacao)
    
    # Botão mágico que permite baixar a planilha em formato CSV/Excel direto pro celular
    csv_data = df_visualizacao.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 BAIXAR PLANILHA COMPLETA",
        data=csv_data,
        file_name="historico_ia_autonoma.csv",
        mime="text/csv",
        use_container_width=True
    )
else:
    st.info("A planilha está vazia. Inicie a operação para colher os primeiros relatórios!")
