import streamlit as st
import anthropic
import base64
import os
from dotenv import load_dotenv

# Configuración de la página
st.set_page_config(
    page_title="Resume Reviewer",
    page_icon="📄",
    layout="centered"
)

def load_environment():
    """Cargar variables de entorno"""
    with st.spinner('Cargando configuración...'):
        load_dotenv()
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            st.error('❌ No se encontró la clave API de Anthropic. Por favor, configure ANTHROPIC_API_KEY en el archivo .env')
            st.stop()
    return api_key

def analyze_resume(pdf_data, client):
    """Analizar el CV usando Claude"""
    try:
        with st.spinner('🤖 Analizando tu CV con Claude...'):
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "document",
                                "source": {
                                    "type": "base64",
                                    "media_type": "application/pdf",
                                    "data": pdf_data
                                }
                            },
                            {
                                "type": "text",
                                "text": "Analyze the resume and provide actionable feedback in case of any issues. If the resume is good, just say 'The resume is good.'"
                            }
                        ]
                    }
                ],
            )
            return message.content[0].text
    except Exception as e:
        st.error(f"❌ Error al analizar el CV: {str(e)}")
        return None

def main():
    st.title("📄 Resume Reviewer")
    st.write("Sube tu CV en formato PDF y recibe retroalimentación personalizada usando IA")
    
    # Cargar configuración
    api_key = load_environment()
    
    # Inicializar cliente de Anthropic
    try:
        client = anthropic.Anthropic(api_key=api_key)
    except Exception as e:
        st.error(f"❌ Error al conectar con Anthropic: {str(e)}")
        st.stop()
    
    # File uploader
    uploaded_file = st.file_uploader("Elige tu CV", type=['pdf'])
    
    if uploaded_file is not None:
        # Mostrar información del archivo
        st.success(f"✅ Archivo subido: {uploaded_file.name}")
        
        # Crear columnas para mostrar detalles
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"📁 Tamaño: {uploaded_file.size/1024:.1f} KB")
        with col2:
            st.info("📄 Tipo: PDF")
        
        # Botón para analizar
        if st.button("🔍 Analizar CV"):
            try:
                # Codificar PDF
                with st.spinner('📥 Procesando el PDF...'):
                    pdf_data = base64.standard_b64encode(uploaded_file.read()).decode("utf-8")
                
                # Analizar con Claude
                analysis = analyze_resume(pdf_data, client)
                
                if analysis:
                    st.markdown("### 📊 Análisis del CV")
                    st.markdown(analysis)
                    
                    # Añadir botón para descargar el análisis
                    st.download_button(
                        label="📥 Descargar Análisis",
                        data=analysis,
                        file_name="analisis_cv.txt",
                        mime="text/plain"
                    )
            
            except Exception as e:
                st.error(f"❌ Error durante el análisis: {str(e)}")

if __name__ == "__main__":
    main() 