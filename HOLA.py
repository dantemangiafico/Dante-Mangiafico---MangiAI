import streamlit as st
from groq import Groq
from datetime import datetime
import base64
import uuid
import html
import time

# ==================== CONFIGURACIÓN ====================
st.set_page_config(
    page_title="MangiAI",
    page_icon="🤖",
    layout="centered"
)

# ==================== FUNCIONES AUXILIARES ====================
def cargar_logo_base64(path):
    """Carga una imagen y la convierte a base64"""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ==================== LOGOS ====================
logo_fijo_base64 = cargar_logo_base64("logomangi.png")
logo_definitivo_base64 = cargar_logo_base64("logodefinitivo2.png")

# ==================== ESTILOS CSS ====================
st.markdown(
    f"""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Exo+2:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

    <style>
    /* -------- FUENTE GLOBAL -------- */
    html, body, [class*="st-"], div, span, p, h1, h2, h3, h4, h5, h6,
    button, input, textarea {{
        font-family: 'Exo 2', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }}

    h1 {{ font-weight: 900; margin: 0; }}

    /* -------- LOGO FIJO SUPERIOR DERECHO -------- */
    .logo-fixed {{
        position: fixed;
        top: 16px;
        right: 16px;
        width: 150px;
        z-index: 999;
        opacity: 0.95;
        pointer-events: none;
        filter: drop-shadow(0 6px 18px rgba(0,0,0,0.35));
        animation: breathing 3s ease-in-out infinite;
    }}

    @keyframes breathing {{
        0%, 100% {{ transform: scale(1); opacity: 0.95; }}
        50% {{ transform: scale(1.05); opacity: 1; }}
    }}

    /* -------- ANIMACIONES -------- */
    @keyframes flotar {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-12px); }}
    }}

    @keyframes brillo {{
        0%, 100% {{ filter: drop-shadow(0 0 8px rgba(34, 197, 94, 0.3)); }}
        50% {{ filter: drop-shadow(0 0 20px rgba(34, 197, 94, 0.6)); }}
    }}

    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(40px) scale(0.95); }}
        to {{ opacity: 1; transform: translateY(0) scale(1); }}
    }}

    @keyframes slideInFromBottom {{
        from {{ opacity: 0; transform: translateY(100px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    @keyframes zoomIn {{
        from {{ opacity: 0; transform: scale(0.8); }}
        to {{ opacity: 1; transform: scale(1); }}
    }}

    @keyframes particula1 {{
        0% {{ transform: translate(0, 0) scale(0); opacity: 0; }}
        50% {{ opacity: 0.6; }}
        100% {{ transform: translate(-30px, -40px) scale(1); opacity: 0; }}
    }}

    @keyframes particula2 {{
        0% {{ transform: translate(0, 0) scale(0); opacity: 0; }}
        50% {{ opacity: 0.6; }}
        100% {{ transform: translate(30px, -45px) scale(1); opacity: 0; }}
    }}

    /* -------- PANTALLA DE BIENVENIDA -------- */
    .welcome-screen {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 72vh;
        text-align: center;
        animation: fadeInUp 1s cubic-bezier(0.34, 1.56, 0.64, 1);
        padding: 20px;
    }}

    .welcome-screen img {{
        width: 130px;
        height: 130px;
        margin-bottom: 28px;
        animation: flotar 3s ease-in-out infinite, brillo 3s ease-in-out infinite, zoomIn 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
    }}

    .welcome-screen h1 {{
        font-size: 3rem;
        font-weight: 900;
        letter-spacing: -0.02em;
        line-height: 1.15;
        margin-bottom: 14px;
        animation: fadeInUp 1s cubic-bezier(0.34, 1.56, 0.64, 1) 0.2s backwards;
    }}

    .welcome-subtitle {{
        font-size: 1.1rem;
        opacity: 0.75;
        margin-bottom: 40px;
        max-width: 500px;
        animation: fadeInUp 1s cubic-bezier(0.34, 1.56, 0.64, 1) 0.4s backwards;
    }}

    /* -------- BOTÓN DE INICIO -------- */
    div[data-testid="stButton"] button {{
        background: linear-gradient(135deg, rgb(34, 197, 94) 0%, rgb(16, 185, 129) 100%) !important;
        color: white !important;
        padding: 16px 48px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 12px !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(34, 197, 94, 0.25) !important;
        width: auto !important;
        animation: zoomIn 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) 0.6s backwards !important;
    }}

    div[data-testid="stButton"] button:hover {{
        transform: translateY(-2px) scale(1.05) !important;
        box-shadow: 0 8px 20px rgba(34, 197, 94, 0.35) !important;
    }}

    /* -------- HEADER DEL CHAT -------- */
    .header-logo {{
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 12px;
        margin-top: 24px;
        margin-bottom: 34px;
        text-align: center;
        animation: slideInFromBottom 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
    }}

    .header-logo img {{
        width: 100px;
        height: 100px;
        animation: flotar 3s ease-in-out infinite, brillo 3s ease-in-out infinite, zoomIn 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
    }}

    .header-logo h1 {{
        font-size: 2.5rem;
        font-weight: 900;
        letter-spacing: -0.02em;
        line-height: 1.15;
        animation: fadeInUp 0.7s cubic-bezier(0.34, 1.56, 0.64, 1) 0.1s backwards;
    }}

    .header-subtitle {{
        font-size: 1rem;
        opacity: 0.75;
        margin-top: -4px;
        animation: fadeInUp 0.7s cubic-bezier(0.34, 1.56, 0.64, 1) 0.2s backwards;
    }}

    /* -------- EMPTY STATE -------- */
    .empty-state {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 40vh;
        text-align: center;
        opacity: 0.95;
        animation: fadeInUp 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) 0.3s backwards;
    }}

    .empty-title {{
        font-size: 2.15rem;
        font-weight: 800;
        animation: zoomIn 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) 0.4s backwards;
    }}

    .empty-subtitle {{
        font-size: 1.05rem;
        opacity: 0.75;
        animation: fadeInUp 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) 0.5s backwards;
    }}

    /* -------- BOTONES DE ESTILO UNIFORMES -------- */
    .stSidebar div[data-testid="stButton"] button {{
        height: 48px !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        white-space: nowrap !important;
        padding: 0 16px !important;
    }}

    /* -------- SCROLLBAR PERSONALIZADO -------- */
    .main, [data-testid="stAppViewContainer"], section[data-testid="stMainBlockContainer"] {{
        overflow-y: auto !important;
    }}

    .main::-webkit-scrollbar, 
    [data-testid="stAppViewContainer"]::-webkit-scrollbar,
    section[data-testid="stMainBlockContainer"]::-webkit-scrollbar {{
        width: 8px !important;
    }}

    .main::-webkit-scrollbar-track,
    [data-testid="stAppViewContainer"]::-webkit-scrollbar-track,
    section[data-testid="stMainBlockContainer"]::-webkit-scrollbar-track {{
        background: transparent !important;
    }}

    .main::-webkit-scrollbar-thumb,
    [data-testid="stAppViewContainer"]::-webkit-scrollbar-thumb,
    section[data-testid="stMainBlockContainer"]::-webkit-scrollbar-thumb {{
        background: rgba(34, 197, 94, 0.3) !important;
        border-radius: 10px !important;
    }}

    .main::-webkit-scrollbar-thumb:hover,
    [data-testid="stAppViewContainer"]::-webkit-scrollbar-thumb:hover,
    section[data-testid="stMainBlockContainer"]::-webkit-scrollbar-thumb:hover {{
        background: rgba(34, 197, 94, 0.5) !important;
    }}

    .main, [data-testid="stAppViewContainer"], section[data-testid="stMainBlockContainer"] {{
        scrollbar-width: thin !important;
        scrollbar-color: rgba(34, 197, 94, 0.3) transparent !important;
    }}

    /* -------- PARTÍCULAS FLOTANTES EN INPUT -------- */
    .stChatInput {{
        position: relative !important;
    }}

    .stChatInput::before,
    .stChatInput::after {{
        content: '' !important;
        position: absolute !important;
        width: 6px !important;
        height: 6px !important;
        background: rgb(34, 197, 94) !important;
        border-radius: 50% !important;
        pointer-events: none !important;
        z-index: 1 !important;
    }}

    .stChatInput::before {{
        bottom: 20px !important;
        left: 10% !important;
        animation: particula1 3s ease-in-out infinite !important;
    }}

    .stChatInput::after {{
        bottom: 20px !important;
        right: 10% !important;
        animation: particula2 3s ease-in-out infinite 0.5s !important;
    }}

    /* -------- ANIMACIONES DE MENSAJES DEL CHAT -------- */
    @keyframes messageSlideIn {{
        from {{
            opacity: 0;
            transform: translateX(-30px);
        }}
        to {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}

    @keyframes messageSlideInRight {{
        from {{
            opacity: 0;
            transform: translateX(30px);
        }}
        to {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}

    div[data-testid="stChatMessage"] {{
        animation: messageSlideInRight 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    }}

    div[data-testid="stChatMessage"] p,
    div[data-testid="stChatMessage"] > div {{
        animation: fadeInUp 0.5s ease-out 0.1s backwards;
    }}

    /* -------- PANTALLA DE LOGIN -------- */
    .login-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 80vh;
        padding: 20px;
        animation: fadeInUp 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
    }}

    .login-box {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border: 2px solid rgba(34, 197, 94, 0.2);
        border-radius: 24px;
        padding: 48px 40px;
        width: 100%;
        max-width: 420px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        animation: zoomIn 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) 0.2s backwards;
    }}

    .login-logo {{
        width: 100px;
        height: 100px;
        margin: 0 auto 24px;
        display: block;
        animation: flotar 3s ease-in-out infinite, brillo 3s ease-in-out infinite;
    }}

    .login-title {{
        font-size: 2rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 8px;
        background: linear-gradient(135deg, #22c55e 0%, #10b981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    .login-subtitle {{
        font-size: 0.95rem;
        text-align: center;
        opacity: 0.7;
        margin-bottom: 32px;
    }}

    .login-divider {{
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(34, 197, 94, 0.3), transparent);
        margin: 24px 0;
    }}

    .login-footer {{
        text-align: center;
        margin-top: 24px;
        font-size: 0.85rem;
        opacity: 0.6;
    }}
    </style>

    <img src="data:image/png;base64,{logo_fijo_base64}" class="logo-fixed">
    """,
    unsafe_allow_html=True
)

# ==================== CONFIGURACIÓN DE MODELOS Y ESTILOS ====================
MODELOS = [
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile",
    "deepseek-r1-distill-llama-70b"
]

ESTILOS = {
    "⚡ Directo": "Respondé de forma breve, clara y sin rodeos.",
    "📖 Explicativo": "Respondé paso a paso, con contexto y ejemplos claros.",
    "🎯 Estratégico": "Respondé analizando opciones, pros y contras, y recomendando.",
    "🧑‍💼 Formal": "Respondé con tono profesional, estructurado y neutral.",
    "💻 Código": (
        "Respondé como un programador senior. "
        "Priorizá código limpio y optimizado. "
        "Usá bloques de código correctamente. "
        "No expliques salvo que el usuario lo pida."
    )
}

AVATARES = {
    "⚡ Directo": ("⚡", "Directo"),
    "📖 Explicativo": ("📖", "Explicativo"),
    "🎯 Estratégico": ("🎯", "Estratégico"),
    "🧑‍💼 Formal": ("🧑‍💼", "Formal"),
    "💻 Código": ("💻", "Código")
}

# ==================== FUNCIONES ====================
def construir_system_prompt():
    """Construye el prompt del sistema basado en el estilo seleccionado"""
    estilo = st.session_state.get("estilo_respuesta", "⚡ Directo")
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
    return (
        f"MangiAI, una IA moderna y profesional creada por Dante Mangiafico. "
        f"{ESTILOS[estilo]} {timestamp}"
    )

def configurar_sidebar():
    """Configura el sidebar con modelos, estilos y herramientas"""
    st.sidebar.title("⚙️ Configuración")
    modelo = st.sidebar.selectbox("Modelo:", MODELOS)

    st.sidebar.markdown("### 💬 Estilo de respuesta")

    if "estilo_respuesta" not in st.session_state:
        st.session_state.estilo_respuesta = "⚡ Directo"

    for estilo in ESTILOS:
        if st.sidebar.button(estilo, use_container_width=True):
            st.session_state.estilo_respuesta = estilo

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎨 Herramientas")
    
    if st.sidebar.button("🧠 Prompt Genius", use_container_width=True, key="gen_img", type="secondary"):
        st.session_state.mostrar_generador = True
        st.rerun()

    if st.sidebar.button("🧹 Limpiar conversación", use_container_width=True):
        st.session_state.mensajes = []
        st.session_state.mostrar_bienvenida = True
        st.rerun()

    # Usuario y cerrar sesión
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"### 👤 {st.session_state.nombre_usuario}")
    if st.sidebar.button("🚪 Cerrar Sesión", use_container_width=True, key="logout"):
        st.session_state.usuario_logueado = False
        st.session_state.nombre_usuario = ""
        st.session_state.mensajes = []
        st.session_state.mostrar_bienvenida = True
        st.rerun()

    return modelo

def inicializar_estado():
    """Inicializa las variables de sesión"""
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []
    if "mostrar_bienvenida" not in st.session_state:
        st.session_state.mostrar_bienvenida = True
    if "mostrar_generador" not in st.session_state:
        st.session_state.mostrar_generador = False
    if "usuario_logueado" not in st.session_state:
        st.session_state.usuario_logueado = False
    if "nombre_usuario" not in st.session_state:
        st.session_state.nombre_usuario = ""

def actualizar_historial(rol, contenido, avatar, estilo=None):
    """Agrega un mensaje al historial"""
    st.session_state.mensajes.append({
        "id": str(uuid.uuid4()),
        "role": rol,
        "content": contenido,
        "avatar": avatar,
        "estilo": estilo
    })

def mostrar_historial():
    """Muestra el historial de mensajes"""
    for m in st.session_state.mensajes:
        if m["role"] == "assistant":
            emoji, nombre = AVATARES.get(m["estilo"], ("🤖", "MangiAI"))
            texto = html.escape(m["content"])
            st.markdown(f"""
                <div style="animation: messageSlideIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);">
                    <strong>{emoji} {nombre}</strong>
                    <br><br>
                    {texto}
                </div>
            """, unsafe_allow_html=True)
        else:
            with st.chat_message("user", avatar=m["avatar"]):
                st.markdown(m["content"])

def generar_respuesta(cliente, modelo):
    """Genera una respuesta usando Groq"""
    mensajes = [{"role": "system", "content": construir_system_prompt()}] + [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.mensajes
    ]

    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=mensajes
    )

    return respuesta.choices[0].message.content

def mejorar_prompt(prompt_basico, cliente, modelo):
    """Mejora un prompt básico convirtiéndolo en uno detallado para generación de imágenes"""
    system_prompt = """Sos un experto en crear prompts para generación de imágenes con IA. 
Tu trabajo es tomar descripciones simples y convertirlas en prompts detallados, profesionales y efectivos.

Incluí detalles sobre:
- Estilo visual (fotorrealista, artístico, cartoon, etc.)
- Iluminación y atmósfera
- Colores y paleta
- Composición y ángulo
- Calidad (8k, alta definición, etc.)
- Texturas y detalles específicos

Respondé SOLO con el prompt mejorado, sin explicaciones adicionales."""

    try:
        respuesta = cliente.chat.completions.create(
            model=modelo,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Mejorá este prompt para generar una imagen: {prompt_basico}"}
            ]
        )
        return respuesta.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error al mejorar prompt: {str(e)}")
        return prompt_basico

# ==================== APLICACIÓN PRINCIPAL ====================
inicializar_estado()

# ==================== PANTALLA DE LOGIN ====================
if not st.session_state.usuario_logueado:
    # Ocultar sidebar durante login
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f'''
        <div class="login-container">
            <div class="login-box">
                <img src="data:image/png;base64,{logo_definitivo_base64}" class="login-logo">
                <div class="login-title">MangiAI</div>
                <div class="login-subtitle">Accede a tu asistente inteligente</div>
                <div class="login-divider"></div>
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
    with st.form("login_form"):
        usuario = st.text_input("👤 Usuario", placeholder="Ingresa tu usuario")
        password = st.text_input("🔒 Contraseña", type="password", placeholder="Ingresa tu contraseña")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button("🚀 Iniciar Sesión", use_container_width=True, type="primary")
        
        if submitted:
            if usuario == "admin" and password == "1234":
                st.session_state.usuario_logueado = True
                st.session_state.nombre_usuario = usuario
                st.success("✅ ¡Bienvenido!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Usuario o contraseña incorrectos")
    
    st.markdown('<div class="login-footer">MangiAI © 2025 - Creado por Dante Mangiafico</div>', unsafe_allow_html=True)
    st.stop()

# ==================== APP PROTEGIDA ====================
cliente = Groq(api_key=st.secrets["CLAVE_API"])
modelo = configurar_sidebar()

# ==================== PROMPT GENIUS ====================
if st.session_state.get("mostrar_generador", False):
    st.markdown("---")
    st.markdown("## 🧠 Prompt Genius")
    
    if "prompt_mejorado" not in st.session_state:
        st.session_state.prompt_mejorado = ""
    
    prompt_imagen = st.text_area(
        "Describe tu idea:",
        placeholder="Ej: Un gato astronauta en el espacio...",
        height=100,
        key="prompt_img"
    )
    
    col1, col2 = st.columns([2, 2])
    
    with col1:
        if st.button("🧠 Potenciar con IA", use_container_width=True, key="btn_enhance", type="primary"):
            if prompt_imagen:
                with st.spinner("🧠 Potenciando tu idea..."):
                    prompt_mejorado = mejorar_prompt(prompt_imagen, cliente, modelo)
                    st.session_state.prompt_mejorado = prompt_mejorado
                    st.rerun()
            else:
                st.warning("Escribí algo primero")
    
    with col2:
        if st.button("❌ Cerrar", use_container_width=True, key="btn_close"):
            st.session_state.mostrar_generador = False
            st.session_state.prompt_mejorado = ""
            st.rerun()
    
    if st.session_state.prompt_mejorado:
        st.markdown("### 💎 Prompt Potenciado:")
        st.info(st.session_state.prompt_mejorado)
        
        if st.button("📋 Copiar Prompt", use_container_width=False):
            st.success("¡Copiá el texto de arriba!")
    
    st.markdown("---")

# ==================== PANTALLA DE BIENVENIDA ====================
elif st.session_state.mostrar_bienvenida:
    st.markdown(
        f"""
        <div class="welcome-screen">
            <img src="data:image/png;base64,{logo_definitivo_base64}">
            <h1>¡Bienvenido a MangiAI!</h1>
            <div class="welcome-subtitle">
                Tu asistente inteligente, elevado al siguiente nivel. Siempre.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Comenzar", use_container_width=True):
            st.session_state.mostrar_bienvenida = False
            st.rerun()

# ==================== PANTALLA DE CHAT ====================
else:
    st.markdown(
        f"""
        <div class="header-logo">
            <img src="data:image/png;base64,{logo_definitivo_base64}">
            <h1>¡Bienvenido a MangiAI!</h1>
            <div class="header-subtitle">
                Tu asistente inteligente, elevado al siguiente nivel. Siempre.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state.mensajes:
        st.markdown("""
            <div class="empty-state">
                <div class="empty-title">¿En qué te ayudo hoy?</div>
                <div class="empty-subtitle">Elegí un estilo o escribí tu consulta</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        mostrar_historial()

    mensaje_usuario = st.chat_input("Escribí tu mensaje...")

    if mensaje_usuario:
        actualizar_historial("user", mensaje_usuario, "🤔")

        with st.spinner("Analizando..."):
            respuesta = generar_respuesta(cliente, modelo)

        estilo_actual = st.session_state.estilo_respuesta
        avatar = AVATARES[estilo_actual][0]

        actualizar_historial("assistant", respuesta, avatar, estilo=estilo_actual)

        st.rerun()
