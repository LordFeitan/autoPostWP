# Tecnober SEO Creator 🚀

**Tecnober SEO Creator** es una aplicación local construida con **FastAPI** y **Tailwind CSS** que permite generar artículos de blog estructurados y optimizados para SEO utilizando la inteligencia artificial de **Google Gemini 1.5 Flash**, para luego guardarlos automáticamente o previsualizarlos antes de publicarlos como borradores en **WordPress**.

---

## 🌟 Características Principales

- ✍️ **Redacción SEO Profesional:** Estructura artículos completos basados en un tema raíz y palabras clave opcionales, siguiendo buenas prácticas SEO.
- 🛠️ **Flujos de Trabajo Flexibles:**
  - **Solo Generar Entrada:** Genera el artículo, muestra una previsualización en tiempo real y permite copiar el contenido sin subirlo a la web. Ideal si tu sitio de WordPress tiene restricciones de red temporales o si prefieres subirlo de forma manual.
  - **Generar y Publicar:** Genera la entrada y la publica directamente en tu sitio como un borrador en un solo paso.
- 🖥️ **Vista Previa en Vivo:**
  - **Pestaña de Previsualización:** Renderiza el HTML generado para ver cómo lucirá el artículo final.
  - **Pestaña de Código HTML:** Muestra el código HTML crudo estructurado por la IA para copiarlo directamente al portapapeles.
- 📋 **Acciones Rápidas de Copiado:** Copia con un solo botón el título generado o todo el código HTML de la entrada.
- 🔒 **Publicación Diferida:** Publica un post generado previamente en cualquier momento haciendo clic en "Publicar en WordPress".
- 🛡️ **Seguridad Bypassing:** Configurado con cabeceras `User-Agent` de navegador para evitar bloqueos por parte de cortafuegos o plugins de seguridad como *Wordfence*, *Sucuri* o *Cloudflare*.
- 🎨 **Interfaz Premium y Fluida:** Diseño web oscuro moderno con estética *glassmorphism*, degradados brillantes y efectos interactivos.

---

## 📁 Estructura del Proyecto

```bash
apiTecnoberPosts/
│
├── services/
│   ├── gemini_service.py  # Conexión con Google Gemini AI y parámetros de prompt
│   └── wp_service.py      # Conexión, autenticación y publicación en WordPress REST API
│
├── static/
│   └── index.html         # Frontend cliente (HTML, CSS personalizado y JS interactivo)
│
├── .env                   # Variables de entorno locales (Claves de API y credenciales)
├── .env.example           # Plantilla de ejemplo para configurar el archivo .env
├── config.py              # Clase de configuración y validador de credenciales
├── main.py                # Servidor FastAPI, esquemas Pydantic y endpoints
└── requirements.txt       # Librerías de Python requeridas para el proyecto
```

---

## ⚙️ Requisitos Previos

1. **Python 3.10 o superior** instalado en tu sistema.
2. **Clave de API de Google Gemini** (obtenida desde Google AI Studio).
3. **Acceso de Administrador o Editor en WordPress** con el sistema de **Contraseñas de Aplicación** activo (disponible en *Usuarios > Perfil* en tu panel de WordPress).

---

## 🚀 Instalación y Configuración

### 1. Preparar el Entorno Virtual

Abre tu terminal en la carpeta raíz del proyecto y ejecuta:

*   **Para crear el entorno virtual:**
    ```bash
    python -m venv .venv
    ```

*   **Para activar el entorno virtual:**
    *   En **PowerShell**:
        ```powershell
        .venv\Scripts\Activate.ps1
        ```
    *   En **Símbolo del Sistema (CMD)**:
        ```cmd
        .venv\Scripts\activate.bat
        ```

### 2. Instalar Dependencias

Con el entorno virtual activo, instala las librerías necesarias:
```bash
pip install -r requirements.txt
```

### 3. Configurar Variables de Entorno

Copia el archivo de ejemplo `.env.example` y renombralo a `.env`:
```bash
cp .env.example .env
```

Abre el archivo `.env` e ingresa tus credenciales:
```env
GEMINI_API_KEY=tu_clave_de_api_de_gemini
WP_URL=https://tu-sitio-wordpress.com
WP_USER=tu_usuario_de_wordpress_o_correo
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx
```
> ⚠️ **Nota:** La contraseña de WordPress debe ser una **Contraseña de Aplicación** generada desde tu panel de WordPress, no tu clave personal de acceso directo.

---

## 💻 Ejecución de la Aplicación

Para iniciar el servidor de desarrollo local, ejecuta en tu terminal:

```bash
uvicorn main:app --reload
```

Una vez que se inicie, podrás acceder en tu navegador a:
- 🌐 **Interfaz Web:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- 📝 **Documentación Interactiva de la API:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🛠️ Tecnologías Utilizadas

- **FastAPI:** Framework backend moderno y rápido para Python.
- **Google GenAI SDK:** Para la integración directa con Gemini 1.5 Flash.
- **WordPress REST API:** Para la publicación automatizada de contenidos como borrador.
- **Tailwind CSS:** Para construir una UI altamente responsive y estilizada.
- **JavaScript (Vanilla):** Para la manipulación asíncrona del DOM y peticiones AJAX.
