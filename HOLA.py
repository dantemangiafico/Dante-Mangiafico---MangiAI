import streamlit as st
from groq import Groq
from datetime import datetime
import base64

# -------------------- CONFIG PÁGINA --------------------
st.set_page_config(
    page_title="MangiAI",
    page_icon="🤖",
    layout="centered"
)

# -------------------- LOGO FIXED PREMIUM --------------------
def cargar_logo_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = cargar_logo_base64("logomangi.png")

st.markdown(
    f"""
    <style>
    .logo-fixed {{
        position: fixed;
        top: 16px;
        right: 16px;
        width: 130px;
        opacity: 0.95;
        z-index: 999;
        pointer-events: none;
        filter: drop-shadow(0 6px 18px rgba(0,0,0,0.35));
    }}

    /* Mobile */
    @media (max-width: 768px) {{
        .logo-fixed {{
            width: 95px;
            top: 12px;
            right: 12px;
        }}
    }}
    </style>

    <img src="data:image/png;base64,{logo_base64}" class="logo-fixed">
    """,
    unsafe_allow_html=True
)

# -------------------- HEADER --------------------
st.title("🤖 ¡Bienvenido a MangiAI!")
st.caption("Tu asistente, a otro nivel. Siempre.")

# -------------------- MODELOS --------------------
MODELOS = [
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile",
    "deepseek-r1-distill-llama-70b"
]

# -------------------- CONTEXTO ACTUAL --------------------
def obtener_contexto_actual():
    ahora = datetime.now()
    return (
        f"Fecha actual: {ahora.strftime('%d/%m/%Y')}. "
        f"Hora actual: {ahora.strftime('%H:%M')}. "
        "Respondé teniendo en cuenta que esta información es actual."
    )

SYSTEM_PROMPT_BASE = (
    "Sos MangiAI, una IA moderna, clara y profesional. "
    "Recordás todo el contexto de la conversación. "
    "Respondés de forma ordenada y útil. "
    "Si el usuario pide código, explicás paso a paso. "
    "Si pide ideas, sos creativo pero realista."
)

# -------------------- SIDEBAR --------------------
def configurar_pagina():
    st.sidebar.title("⚙️ Configuración")
    modelo = st.sidebar.selectbox("Elige un modelo:", MODELOS)

    if st.sidebar.button("🧹 Limpiar conversación"):
        st.session_state.mensajes = []
        st.rerun()

    return modelo

# -------------------- GROQ CLIENT --------------------
def crear_cliente_groq():
    return Groq(api_key=st.secrets["CLAVE_API"])

# -------------------- ESTADO --------------------
def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({
        "role": rol,
        "content": contenido,
        "avatar": avatar
    })

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])

# -------------------- RESPUESTA IA --------------------
def generar_respuesta(cliente, modelo):
    system_prompt = {
        "role": "system",
        "content": SYSTEM_PROMPT_BASE + " " + obtener_contexto_actual()
    }

    mensajes = [system_prompt] + [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.mensajes
    ]

    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=mensajes
    )

    return respuesta.choices[0].message.content

# -------------------- APP --------------------
inicializar_estado()
cliente = crear_cliente_groq()
modelo = configurar_pagina()

mostrar_historial()

mensaje_usuario = st.chat_input("Escribe tu mensaje...")

if mensaje_usuario:
    actualizar_historial("user", mensaje_usuario, "🤔")

    with st.spinner("MangiAI está pensando..."):
        respuesta = generar_respuesta(cliente, modelo)

    # 👇 AVATAR CORRECTO (NO LOGO)
    actualizar_historial("assistant", respuesta, "🤖")
    st.rerun()

