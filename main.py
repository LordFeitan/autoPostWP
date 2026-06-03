from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional
import os

from config import Config
from services.gemini_service import GeminiService
from services.wp_service import WPService

app = FastAPI(
    title="Generador de Contenidos SEO para WordPress",
    description="Aplicación local para generar artículos optimizados con Gemini 1.5 y publicarlos en WordPress.",
    version="1.0.0"
)

# Modelo para la solicitud de generación
class ArticleRequest(BaseModel):
    theme: str = Field(..., min_length=3, max_length=200, description="Tema o título semilla del artículo")
    keywords: Optional[str] = Field(None, max_length=500, description="Palabras clave o enfoque SEO")

# Modelo para la respuesta
class ArticleResponse(BaseModel):
    success: bool
    message: str
    post_id: Optional[int] = None
    title: Optional[str] = None
    link: Optional[str] = None
    edit_link: Optional[str] = None
    status: Optional[str] = None
    content: Optional[str] = None

class ArticleGenerateResponse(BaseModel):
    success: bool
    title: str
    content: str  # Contenido HTML generado por Gemini

class PublishRequest(BaseModel):
    title: str
    content: str

@app.get("/api/config-status")
def get_config_status():
    """Retorna si las variables de entorno están correctamente configuradas."""
    errors = Config.validate()
    return {
        "configured": len(errors) == 0,
        "errors": errors,
        "wp_url": Config.WP_URL
    }

@app.post("/api/generate-publish", response_model=ArticleResponse)
async def generate_and_publish(request: ArticleRequest):
    """
    Endpoint principal: genera el artículo con Gemini y lo publica como borrador en WordPress.
    """
    # 1. Validar configuración
    config_errors = Config.validate()
    if config_errors:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error de configuración del servidor: {', '.join(config_errors)}"
        )

    # 2. Generar el artículo mediante la API de Gemini
    try:
        html_content = GeminiService.generate_seo_article(
            theme=request.theme,
            keywords=request.keywords
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error al generar artículo con Gemini: {str(e)}"
        )

    # 3. Publicar el artículo en WordPress
    try:
        wp_result = WPService.publish_draft_post(
            title=request.theme,
            content=html_content
        )
        return ArticleResponse(
            success=True,
            message="El artículo se generó y guardó como borrador en WordPress con éxito.",
            post_id=wp_result["id"],
            title=wp_result["title"],
            link=wp_result["link"],
            edit_link=wp_result["edit_link"],
            status=wp_result["status"],
            content=html_content
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error al publicar borrador en WordPress: {str(e)}"
        )

@app.post("/api/generate-only", response_model=ArticleGenerateResponse)
async def generate_only(request: ArticleRequest):
    """
    Endpoint para generar el artículo con Gemini pero NO publicarlo en WordPress.
    """
    if not Config.GEMINI_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error: GEMINI_API_KEY no configurada en el archivo .env"
        )

    try:
        html_content = GeminiService.generate_seo_article(
            theme=request.theme,
            keywords=request.keywords
        )
        return ArticleGenerateResponse(
            success=True,
            title=request.theme,
            content=html_content
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error al generar artículo con Gemini: {str(e)}"
        )

@app.post("/api/publish-only", response_model=ArticleResponse)
async def publish_only(request: PublishRequest):
    """
    Endpoint para publicar un artículo ya generado directamente en WordPress.
    """
    config_errors = Config.validate()
    wp_errors = [err for err in config_errors if "WP_" in err]
    if wp_errors:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error de configuración de WordPress: {', '.join(wp_errors)}"
        )

    try:
        wp_result = WPService.publish_draft_post(
            title=request.title,
            content=request.content
        )
        return ArticleResponse(
            success=True,
            message="El artículo se guardó como borrador en WordPress con éxito.",
            post_id=wp_result["id"],
            title=wp_result["title"],
            link=wp_result["link"],
            edit_link=wp_result["edit_link"],
            status=wp_result["status"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error al publicar borrador en WordPress: {str(e)}"
        )

# Aseguramos que la carpeta static exista
os.makedirs("static", exist_ok=True)

# Servir archivos estáticos para la interfaz de usuario
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# Redirección en caso de que falte index.html para evitar 404
@app.exception_handler(404)
async def custom_404_handler(request, __):
    return FileResponse("static/index.html")
