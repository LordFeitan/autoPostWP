import requests
from requests.auth import HTTPBasicAuth
from config import Config

class WPService:
    @staticmethod
    def publish_draft_post(title: str, content: str) -> dict:
        """
        Publica un artículo como borrador ('draft') en WordPress utilizando la REST API.
        Retorna un diccionario con detalles del post creado o eleva una excepción con el error.
        """
        # Endpoint de la API REST para posts
        endpoint = f"{Config.WP_URL}/wp-json/wp/v2/posts"
        
        # Datos a enviar
        payload = {
            "title": title,
            "content": content,
            "status": "draft"
        }
        
        # Autenticación Básica con contraseñas de aplicación de WordPress
        auth = HTTPBasicAuth(Config.WP_USER, Config.WP_APP_PASSWORD)
        
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        try:
            response = requests.post(
                endpoint,
                json=payload,
                auth=auth,
                headers=headers,
                timeout=15  # Timeout razonable
            )
            
            # Lanzará HTTPError si el código de estado no es exitoso (por ejemplo, 401, 400, 500, etc.)
            response.raise_for_status()
            
            post_data = response.json()
            post_id = post_data.get("id")
            public_link = post_data.get("link", "")
            
            # Construimos la URL de edición de WordPress para la comodidad del usuario
            edit_link = f"{Config.WP_URL}/wp-admin/post.php?post={post_id}&action=edit"
            
            return {
                "success": True,
                "id": post_id,
                "title": post_data.get("title", {}).get("rendered", title),
                "link": public_link,
                "edit_link": edit_link,
                "status": post_data.get("status")
            }
            
        except requests.exceptions.HTTPError as http_err:
            # Intentar obtener el detalle del error de WordPress
            try:
                error_json = response.json()
                error_msg = error_json.get("message", str(http_err))
                error_code = error_json.get("code", "unknown_error")
                raise Exception(f"Error de WordPress ({error_code}): {error_msg}")
            except Exception:
                raise Exception(f"Error HTTP de WordPress: {response.status_code} - {response.text}")
                
        except requests.exceptions.ConnectionError:
            raise Exception(f"No se pudo establecer conexión con el servidor de WordPress en: {Config.WP_URL}. Verifica que el dominio sea correcto y el servidor esté activo.")
            
        except requests.exceptions.Timeout:
            raise Exception("La solicitud a WordPress superó el tiempo de espera límite.")
            
        except Exception as e:
            raise Exception(f"Ocurrió un error inesperado al conectar con WordPress: {str(e)}")
