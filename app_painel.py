import streamlit as st
import os
import requests
from google import genai

# Configuração da Página do Aplicativo (Visual do Celular)
st.set_page_config(page_title="Cibernética Autônoma", page_icon="🤖", layout="centered")

st.title("🤖 Painel do Supervisor Soberano")
st.write("Sua equipe de gênios rodando sem custos usando a IA oficial do Google.")

# ==============================================================================
# PAINEL DE CREDENCIAIS (ENTRADA SEGURA)
# ==============================================================================
st.sidebar.header("🔑 Chaves de Ativação")
gemini_key = st.sidebar.text_input("Gemini API Key (Gratuita do Google)", type="password")
heygen_key = st.sidebar.text_input("HeyGen API Key (Teste Grátis)", type="password")
eleven_key = st.sidebar.text_input("ElevenLabs API Key (Plano Grátis)", type="password")

# ==============================================================================
# CONFIGURAÇÃO E EXECUÇÃO DO SISTEMA
# ==============================================================================
if st.button("🚀 INICIAR OPERAÇÃO AUTÔNOMA", use_container_width=True):
    if not gemini_key:
        st.error("❌ ERRO CRÍTICO: Você precisa colocar a sua Gemini API Key para ativar o cérebro das IAs.")
    else:
        with st.spinner("🧠 Os cientistas virtuais estão debatendo e minerando o mercado mundial..."):
            try:
                # Inicializa o cliente oficial do Google Gemini
                client = genai.Client(api_key=gemini_key)
                
                # Comando unificado que simula o debate do enxame de agentes especialistas
                prompt_sistema = """
                Você é uma equipe de três cientistas gênios trabalhando juntos:
                1. Analista de Tendências: Minera produtos virais globais e identifica o que vende em massa.
                2. Engenheiro de Hiper-Melhoria: Cria um projeto 1000x melhor e mais barato baseado no produto viral, corrigindo falhas.
                3. Arquiteto de Automação: Cria o roteiro de vendas curto e persuasivo para robôs hiper-realistas usarem.
                
                Debatam entre si e entreguem o relatório final contendo: O produto viral escolhido, as 5 melhorias brutais de engenharia e o roteiro final de marketing com menos de 300 letras.
                """
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt_sistema,
                )
                
                relatorio_final = response.text
                
                st.success("✅ Relatório de Engenharia e Vendas Concluído!")
                st.subheader("📋 Relatório dos Gênios:")
                st.write(relatorio_final)
                
                # DISPARO DOS ROBÔS MULTIMÍDIA
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
                
            except Exception as error_geral:
                st.error(f"Falha na execução do cérebro Google: {error_geral}")
