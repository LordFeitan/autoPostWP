import os
from google import genai
from google.genai import types
from config import Config

class GeminiService:
    @staticmethod
    def generate_seo_article(theme: str, keywords: str = None) -> str:
        """
        Genera un artículo optimizado para SEO basado en un tema y palabras clave opcionales.
        Devuelve el contenido en formato HTML limpio y listo para WordPress.
        """
        # Inicializa el cliente usando la clave de API configurada
        client = genai.Client(api_key=Config.GEMINI_API_KEY)
        
        system_instruction = (
            "Eres un redactor experto en SEO y blogs profesionales. Tu tarea es generar un artículo de blog estructurado, informativo, de alta calidad y 100% verídico.\n"
            "REQUISITOS IMPORTANTES:\n"
            "1. Utiliza la herramienta de búsqueda integrada de Google para corroborar toda la información, fechas, datos, estadísticas y hechos. NO inventes ningún dato. Si no encuentras información verídica sobre un hecho o dato, no lo menciones.\n"
            "2. Devuelve EXCLUSIVAMENTE código HTML limpio para el cuerpo del post.\n"
            "3. NO uses bloques de código markdown (evita por completo encerrar la respuesta en ```html o ``` al inicio y final). Devuelve solo el texto HTML crudo.\n"
            "4. No incluyas las etiquetas <html>, <head>, <body> o <h1>. El título se gestiona por separado en WordPress.\n"
            "5. Usa únicamente las siguientes etiquetas HTML permitidas: <h2>, <h3>, <p>, <strong>, <ul>, <ol>, <li>, <blockquote>, <em>, <a>.\n"
            "6. El artículo debe estar redactado en español de forma fluida, atractiva y optimizado para SEO."
        )
        
        prompt = f"Tema o Título del Artículo: {theme}\n"
        if keywords:
            prompt += f"Enfoque SEO / Keywords a incluir: {keywords}\n"
        
        prompt += "\nGenera el cuerpo del artículo estructurado con etiquetas HTML. Comienza directamente con una introducción en un párrafo <p> o un subtítulo H2, sin títulos H1."

        # Realizar la llamada a la API con Google Search Grounding habilitado
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        
        content = response.text
        if not content:
            raise ValueError("La API de Gemini devolvió una respuesta vacía.")
            
        # Post-procesamiento de seguridad para limpiar posibles bloques markdown ```html del modelo
        content = content.strip()
        if content.startswith("```html"):
            content = content[7:]
        elif content.startswith("```"):
            content = content[3:]
            
        if content.endswith("```"):
            content = content[:-3]
            
        return content.strip()
