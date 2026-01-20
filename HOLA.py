import streamlit as st
from groq import Groq
from datetime import datetime
import base64
import html

# -------------------- CONFIG PÁGINA --------------------
st.set_page_config(
    page_title="MangiAI",
    page_icon="🤖",
    layout="centered"
)

# -------------------- LOGO --------------------
def cargar_logo_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = cargar_logo_base64("logomangi.png")

st.markdown(
    f"""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Exo+2:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

    <style>
    /* -------- FONT GLOBAL (SAFE) -------- */
    html, body, button, input, textarea {{
        font-family: 'Exo 2', -apple-system, BlinkMacSystemFont,
                     'Segoe UI', sans-serif !important;
    }}

    /* -------- FIX MATERIAL ICONS -------- */
    .material-icons,
    .material-symbols-outlined,
    .material-symbols-rounded,
    .material-symbols-sharp {{
        font-family: 'Material Icons', 'Material Symbols Outlined',
                     'Material Symbols Rounded', 'Material Symbols Sharp' !important;
    }}

    /* -------- LOGO -------- */
    .logo-fixed {{
        position: fixed;
        top: 14px;
        right: 14px;
        width: 130px;
        z-index: 999;
        pointer-events: none;
        filter: drop-shadow(0 6px 18px rgba(0,0,0,0.35));
    }}

    @media (max-width: 768px) {{
        .logo-fixed {{ width: 95px; }}
    }}

    /* -------- CHAT -------- */
    .chat-wrapper {{
        position: relative;
        padding: 18px;
        border-radius: 14px;
        margin-bottom: 14px;
        background: rgba(255,255,255,0.03);
    }}

    .chat-message {{
        line-height: 1.7;
        font-size: 1.02rem;
        white-space: pre-wrap;
        word-break: break-word;
    }}
    </style>

    <img src="data:image/png;base64,{logo_base64}" class="logo-fixed">
    """,
    unsafe_allow_html=True
)

# -------------------- HEADER --------------------
st.title("🤖 ¡Bienvenido a MangiAI!")
st.caption("Tu asistente inteligente, elevado al siguiente nivel.")

# -------------------- MODELOS --------------------
MODELOS = [
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile",
    "deepseek-r1-distill-llama-70b"
]

# -------------------- ESTILOS --------------------
ESTILOS = {
    "⚡ Directo": "Respondé de forma breve, clara y sin rodeos.",
    "📖 Explicativo": "Respondé paso a paso, con contexto y ejemplos.",
    "🎯 Estratégico": "Respondé analizando opciones y recomendando.",
    "🧑‍💼 Formal": "Respondé con tono profesional.",
    "💻 Código": "Respondé como programador senior. Código limpio."
}

AVATARES = {k: (k.split()[0], k.split()[1]) for k in ESTILOS}

# -------------------- CONTEXTO --------------------
def construir_system_prompt():
    estilo = st.session_state.get("estilo_respuesta", "⚡ Directo")
    ahora = datetime.now().strftime("%d/%m/%Y %H:%M")
    return f"Sos MangiAI, una IA premium creada por Dante Mangiafico. {ESTILOS[estilo]} Fecha: {ahora}"

# -------------------- SIDEBAR --------------------
st.sidebar.title("⚙️ Configuración")
modelo = st.sidebar.selectbox("Modelo", MODELOS)

st.session_state.setdefault("estilo_respuesta", "⚡ Directo")

for estilo in ESTILOS:
    if st.sidebar.button(estilo, use_container_width=True):
        st.session_state.estilo_respuesta = estilo

if st.sidebar.button("🧹 Limpiar conversación"):
    st.session_state.mensajes = []
    st.rerun()

# -------------------- GROQ --------------------
cliente = Groq(api_key=st.secrets["CLAVE_API"])
st.session_state.setdefault("mensajes", [])

# -------------------- HISTORIAL --------------------
for m in st.session_state.mensajes:
    if m["role"] == "assistant":
        texto = html.escape(m["content"])
        st.markdown(
            f"<div class='chat-wrapper'><div class='chat-message'>{texto}</div></div>",
            unsafe_allow_html=True
        )
    else:
        with st.chat_message("user", avatar="🤔"):
            st.markdown(m["content"])

# -------------------- INPUT --------------------
mensaje = st.chat_input("Escribí tu mensaje...")

if mensaje:
    st.session_state.mensajes.append({"role": "user", "content": mensaje})

    with st.spinner("Analizando..."):
        respuesta = cliente.chat.completions.create(
            model=modelo,
            messages=[{"role": "system", "content": construir_system_prompt()}]
            + st.session_state.mensajes
        ).choices[0].message.content

    st.session_state.mensajes.append({
        "role": "assistant",
        "content": respuesta,
        "estilo": st.session_state.estilo_respuesta
    })

    st.rerun()
