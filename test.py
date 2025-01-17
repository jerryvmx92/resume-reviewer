import anthropic
import base64
import os
from dotenv import load_dotenv

# Cargar variables de entorno
print("🔄 Cargando variables de entorno...")
load_dotenv()
api_key = os.getenv('ANTHROPIC_API_KEY')
print("✅ Variables de entorno cargadas")

# Load and encode the PDF
print("\n📥 Leyendo PDF local...")
pdf_path = "./pdfs/Copy of The Pragmatic Engineer's Resume Template - TheTechResume.com (1).pdf"
try:
    # Verificar si el archivo existe
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"No se encontró el archivo en: {pdf_path}")
        
    # Leer y codificar el PDF
    with open(pdf_path, "rb") as pdf_file:
        pdf_data = base64.standard_b64encode(pdf_file.read()).decode("utf-8")
    print("✅ PDF leído y codificado correctamente")
except Exception as e:
    print(f"❌ Error al leer el PDF: {str(e)}")
    raise

# Send to Claude
print("\n🤖 Conectando con Claude...")
try:
    client = anthropic.Anthropic(
        api_key=api_key
    )
    print("✅ Conexión establecida con Claude")
    
    print("\n📝 Enviando documento para análisis...")
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
                        "text": "Analyze the resume and provide actionable feedback in case of any issues. If the resume is good, just say 'The resume is good.'."
                    }
                ]
            }
        ],
    )
    print("\n✅ Respuesta recibida de Claude:")
    print("=" * 50)
    print(message.content)
    print("=" * 50)
except Exception as e:
    print(f"\n❌ Error al procesar con Claude: {str(e)}")
    raise