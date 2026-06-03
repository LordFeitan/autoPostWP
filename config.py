import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    # URL base de WordPress, limpiamos la barra inclinada final si existe
    WP_URL = os.getenv("WP_URL", "").rstrip("/")
    WP_USER = os.getenv("WP_USER", "")
    WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD", "")

    @classmethod
    def validate(cls):
        """Valida que las credenciales no estén vacías."""
        errors = []
        if not cls.GEMINI_API_KEY:
            errors.append("GEMINI_API_KEY no configurado en el archivo .env")
        if not cls.WP_URL:
            errors.append("WP_URL no configurado en el archivo .env")
        if not cls.WP_USER:
            errors.append("WP_USER no configurado en el archivo .env")
        if not cls.WP_APP_PASSWORD:
            errors.append("WP_APP_PASSWORD no configurado en el archivo .env")
        return errors
