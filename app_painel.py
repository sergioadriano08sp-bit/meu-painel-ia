import streamlit as st
import os
import requests
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# Configuração da Página do Aplicativo (Visual do Celular)
st.set_page_config(page_title="Cibernética Autônoma", page_icon="🤖", layout="centered")

st.title("🤖 Painel do Supervisor Soberano (Versão Gratuita)")
st.write("Sua equipe de gênios rodando sem custos usando a IA da Groq.")

# ==============================================================================
# PAINEL DE CREDENCIAIS (ENTRADA SEGURA)
# ==============================================================================
st.sidebar.header("🔑 Chaves de Ativação")
groq_key = st.sidebar.text_input("Groq API Key (Gratuita)", type="password", help="Sua chave gratuita da Groq")
heygen_key = st.sidebar.text_input("HeyGen API Key (Teste Grátis)", type="password", help="Sua chave de teste do HeyGen")
eleven_key = st.sidebar.text_input("ElevenLabs API Key (Plano Grátis)", type="password", help="Sua chave grátis da ElevenLabs")

# ==============================================================================
# CONFIGURAÇÃO DO MOTOR DE IA GRATUITO (GROQ)
# ==============================================================================
if st.button("🚀 INICIAR OPERAÇÃO AUTÔNOMA", use_container_width=True):
    if not groq_key:
        st.error("❌ ERRO CRÍTICO: Você precisa colocar a sua Groq API Key para ativar o cérebro das IAs.")
    else:
        # Configura o motor gratuito apontando para a Groq utilizando o modelo Llama 3
        llm_gratuito = ChatOpenAI(
            openai_api_base="https://groq.com",
            openai_api_key=groq_key,
            model_name="llama3-70b-8192"
        )
        
        with st.spinner("🧠 Os cientistas estão debatendo e minerando o mercado mundial..."):
            # Criação Automática dos Agentes com o cérebro gratuito (llm=llm_gratuito)
            analista = Agent(
                role='Analista de Tendências',
                goal='Minerar produtos virais globais.',
                backstory='Especialista em encontrar o que vende em massa antes de todo mundo.',
                verbose=True,
                llm=llm_gratuito
            )
            engenheiro = Agent(
                role='Engenheiro de Hiper-Melhoria',
                goal='Criar um projeto 1000x melhor e mais barato baseado no produto viral.',
                backstory='Gênio da engenharia reversa. Elimina falhas de concorrentes.',
                verbose=True,
                llm=llm_gratuito
            )
            arquiteto = Agent(
                role='Arquiteto de Automação',
                goal='Criar roteiro de vendas para os robôs hiper-realistas.',
                backstory='Especialista em automação financeira e avatares digitais.',
                verbose=True,
                llm=llm_gratuito
            )

            # Definição das Tarefas Sucessivas
            t1 = Task(description='Varra as tendências e isole o produto físico campeão.', expected_output='Relatório do produto viral.', agent=analista)
            t2 = Task(description='Desenhe a versão definitiva corrigindo falhas.', expected_output='Projeto conceitual otimizado.', agent=engenheiro)
            t3 = Task(description='Escreva o roteiro de vendas persuasivo para a IA de vídeo.', expected_output='Roteiro de marketing final.', agent=arquiteto)

            # Ativação do Enxame
            enxame = Crew(agents=[analista, engenheiro, arquiteto], tasks=[t1, t2, t3], process=Process.sequential)
            relatorio_final = enxame.kickoff()
            
        st.success("✅ Relatório de Engenharia e Vendas Concluído!")
        st.subheader("📋 Relatório dos Gênios:")
        st.write(str(relatorio_final))

        # DISPARO DOS ROBÔS MULTIMÍDIA (Usando os créditos gratuitos deles)
        if heygen_key or eleven_key:
            with st.spinner("🎥 Acionando Robôs de Mídia..."):
                # Chamada HeyGen
                if heygen_key:
                    try:
                        headers = {"X-Api-Key": heygen_key, "Content-Type": "application/json"}
                        payload = {
                            "video_setting": {"width": 1080, "height": 1920},
                            "dimension": "vertical",
                            "character": {"character_id": "avatar_masculino_executivo_01", "type": "avatar"},
                            "input_text": str(relatorio_final)[:300]
                        }
                        res_vid = requests.post("https://heygen.com", json=payload, headers=headers).json()
                        video_id = res_vid.get("data", {}).get("video_id", "Vídeo enviado para processamento!")
                        st.info(f"🎬 Vídeo Publicitário Enviado! ID: {video_id}")
                    except Exception as e:
                        st.warning(f"Nota do HeyGen: {e}")

                # Chamada ElevenLabs
                if eleven_key:
                    try:
                        headers = {"xi-api-key": eleven_key, "Content-Type": "application/json"}
                        payload = {"text": str(relatorio_final)[:300], "model_id": "eleven_multilingual_v2"}
                        res_aud = requests.post("https://elevenlabs.io", json=payload, headers=headers)
                        if res_aud.status_code == 200:
                            st.info("🗣️ Áudio Gratuito Gerado na ElevenLabs!")
                    except Exception as e:
                        st.warning(f"Nota do ElevenLabs: {e}")
                
        st.balloons()
