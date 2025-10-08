from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os

# --- Configuración del cliente ---
client = genai.Client(api_key="openAi_KEY")

# --- Prompt (corregido) ---
prompt = (
    "Create an image to visually integrate an applied mathematics project onto it. "
    "The project should appear as an explanatory diagram or mathematical scheme — "
    "including formulas, lines, vectors, annotations, and graphs — showing how mathematics "
    "applies to the situation depicted in the base image. "
    "Make sure the diagram blends naturally with the scene, appearing as a semi-transparent "
    "or digital whiteboard-style overlay. Keep the look educational, clean, professional, "
    "and easy to read."
) 

# --- Cargar imagen base ---
image_path = "/home/raing/Documents/Abladorios/app/resources/campo.png"
image_path = "/home/raing/Documents/Abladorios/app/resources/proyecto.png"
image_path = "/home/raing/Documents/Abladorios/app/resources/musica.png"
image = Image.open(image_path)

# --- Llamada al modelo de generación ---
response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[prompt, image],
)

# --- Procesar y guardar resultado ---
for part in response.candidates[0].content.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        generated_image = Image.open(BytesIO(part.inline_data.data))
        
        # Guardar en la carpeta raíz del proyecto
        root_path = "/home/raing/Documents/Abladorios/generated_imusica.png"
        generated_image.save(root_path)
        print(f"✅ Imagen generada y guardada en: {root_path}")
