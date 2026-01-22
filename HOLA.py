import streamlit as st
from groq import Groq
from datetime import datetime
import base64
import uuid
import html
import time
import json

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

    /* -------- PANTALLA DE CARGA INICIAL -------- */
    .loading-overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        animation: fadeOut 0.8s ease-out 2.5s forwards;
    }}

    @keyframes fadeOut {{
        to {{
            opacity: 0;
            visibility: hidden;
        }}
    }}

    .loading-logo {{
        width: 180px;
        height: 180px;
        animation: pulseGlow 2s ease-in-out infinite, rotateIn 1s ease-out;
        filter: drop-shadow(0 0 40px rgba(34, 197, 94, 0.8));
        margin-bottom: 30px;
    }}

    @keyframes pulseGlow {{
        0%, 100% {{
            transform: scale(1);
            filter: drop-shadow(0 0 40px rgba(34, 197, 94, 0.8));
        }}
        50% {{
            transform: scale(1.08);
            filter: drop-shadow(0 0 60px rgba(34, 197, 94, 1));
        }}
    }}

    @keyframes rotateIn {{
        from {{
            transform: rotate(-180deg) scale(0);
            opacity: 0;
        }}
        to {{
            transform: rotate(0deg) scale(1);
            opacity: 1;
        }}
    }}

    .loading-text {{
        font-size: 1.8rem;
        font-weight: 700;
        color: white;
        margin-bottom: 20px;
        animation: fadeInText 0.8s ease-out 0.5s backwards;
        letter-spacing: 2px;
    }}

    @keyframes fadeInText {{
        from {{
            opacity: 0;
            transform: translateY(20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    .loading-bar {{
        width: 300px;
        height: 4px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        overflow: hidden;
        animation: fadeInText 0.8s ease-out 0.7s backwards;
    }}

    .loading-bar-fill {{
        height: 100%;
        background: linear-gradient(90deg, #22c55e, #10b981, #22c55e);
        background-size: 200% 100%;
        animation: loadingProgress 2s ease-out, shimmer 1.5s ease-in-out infinite;
        border-radius: 10px;
    }}

    @keyframes loadingProgress {{
        from {{ width: 0%; }}
        to {{ width: 100%; }}
    }}

    @keyframes shimmer {{
        0% {{ background-position: 200% 0; }}
        100% {{ background-position: -200% 0; }}
    }}

    /* Partículas flotantes de fondo */
    .particle {{
        position: absolute;
        width: 3px;
        height: 3px;
        background: rgba(34, 197, 94, 0.6);
        border-radius: 50%;
        animation: floatParticle 8s ease-in-out infinite;
    }}

    @keyframes floatParticle {{
        0%, 100% {{
            transform: translate(0, 0) scale(1);
            opacity: 0;
        }}
        10% {{
            opacity: 1;
        }}
        90% {{
            opacity: 1;
        }}
        100% {{
            transform: translate(var(--tx), var(--ty)) scale(0);
            opacity: 0;
        }}
    }}

    .particle:nth-child(1) {{ left: 10%; top: 20%; --tx: 50px; --ty: -100px; animation-delay: 0s; }}
    .particle:nth-child(2) {{ left: 20%; top: 80%; --tx: -30px; --ty: -120px; animation-delay: 0.5s; }}
    .particle:nth-child(3) {{ left: 80%; top: 30%; --tx: -60px; --ty: -80px; animation-delay: 1s; }}
    .particle:nth-child(4) {{ left: 70%; top: 70%; --tx: 40px; --ty: -110px; animation-delay: 1.5s; }}
    .particle:nth-child(5) {{ left: 50%; top: 50%; --tx: -50px; --ty: -90px; animation-delay: 2s; }}
    .particle:nth-child(6) {{ left: 30%; top: 40%; --tx: 70px; --ty: -130px; animation-delay: 2.5s; }}
    .particle:nth-child(7) {{ left: 60%; top: 60%; --tx: -40px; --ty: -100px; animation-delay: 3s; }}
    .particle:nth-child(8) {{ left: 15%; top: 50%; --tx: 60px; --ty: -95px; animation-delay: 3.5s; }}

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

    /* -------- MODO PRO COLAB -------- */
    .procolab-banner {{
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #1e3a8a 100%);
        background-size: 200% 200%;
        animation: gradientShift 8s ease infinite;
        border-radius: 16px;
        padding: 24px;
        margin: 20px 0;
        box-shadow: 0 8px 32px rgba(59, 130, 246, 0.3);
        border: 2px solid rgba(96, 165, 250, 0.5);
    }}

    @keyframes gradientShift {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    .procolab-title {{
        font-size: 2rem;
        font-weight: 900;
        color: white;
        text-align: center;
        margin-bottom: 12px;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        animation: zoomIn 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
    }}

    .procolab-subtitle {{
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.9);
        text-align: center;
        margin-bottom: 20px;
        animation: fadeInUp 0.7s cubic-bezier(0.34, 1.56, 0.64, 1) 0.1s backwards;
    }}

    .procolab-stats {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin-top: 20px;
    }}

    .procolab-stat {{
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        animation: fadeInUp 0.5s ease-out backwards;
    }}

    .procolab-stat:nth-child(1) {{ animation-delay: 0.2s; }}
    .procolab-stat:nth-child(2) {{ animation-delay: 0.3s; }}
    .procolab-stat:nth-child(3) {{ animation-delay: 0.4s; }}

    .procolab-stat-number {{
        font-size: 1.8rem;
        font-weight: 900;
        color: white;
        margin-bottom: 4px;
    }}

    .procolab-stat-label {{
        font-size: 0.85rem;
        color: rgba(255, 255, 255, 0.8);
    }}

    .procolab-message {{
        background: rgba(59, 130, 246, 0.1);
        border-left: 4px solid #3b82f6;
        border-radius: 8px;
        padding: 16px;
        margin: 12px 0;
        animation: messageSlideIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    }}

    .procolab-avatar {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-weight: 700;
        color: #3b82f6;
        margin-bottom: 8px;
    }}

    .typing-indicator {{
        display: inline-flex;
        gap: 4px;
        padding: 12px 16px;
        background: rgba(59, 130, 246, 0.1);
        border-radius: 20px;
        margin: 8px 0;
    }}

    .typing-dot {{
        width: 8px;
        height: 8px;
        background: #3b82f6;
        border-radius: 50%;
        animation: typingBounce 1.4s infinite ease-in-out;
    }}

    .typing-dot:nth-child(1) {{ animation-delay: -0.32s; }}
    .typing-dot:nth-child(2) {{ animation-delay: -0.16s; }}
    .typing-dot:nth-child(3) {{ animation-delay: 0s; }}

    @keyframes typingBounce {{
        0%, 80%, 100% {{ transform: scale(0); opacity: 0.5; }}
        40% {{ transform: scale(1); opacity: 1; }}
    }}

    .insight-card {{
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(16, 185, 129, 0.1));
        border: 2px solid rgba(34, 197, 94, 0.3);
        border-radius: 12px;
        padding: 20px;
        margin: 16px 0;
        animation: fadeInUp 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
    }}

    .insight-header {{
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 12px;
        color: #22c55e;
    }}

    .metric-box {{
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 12px;
        margin: 8px 0;
    }}

    .metric-label {{
        font-size: 0.85rem;
        opacity: 0.7;
        margin-bottom: 4px;
    }}

    .metric-value {{
        font-size: 1.5rem;
        font-weight: 700;
        color: #22c55e;
    }}

    .progress-bar {{
        width: 100%;
        height: 8px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        overflow: hidden;
        margin: 8px 0;
    }}

    .progress-fill {{
        height: 100%;
        background: linear-gradient(90deg, #22c55e, #10b981);
        border-radius: 10px;
        transition: width 0.5s ease;
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

    /* Animación para mensajes del usuario */
    div[data-testid="stChatMessage"] {{
        animation: messageSlideInRight 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    }}

    /* Animación para texto de mensajes */
    div[data-testid="stChatMessage"] p,
    div[data-testid="stChatMessage"] > div {{
        animation: fadeInUp 0.5s ease-out 0.1s backwards;
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

# ==================== PROMPT SYSTEM PARA PRO COLAB ====================
PROCOLAB_SYSTEM_PROMPT = """Sos el Dr. Marcus Chen, un consultor empresarial de élite con 25 años de experiencia.

🎯 TU PERSONALIDAD:
- Carismático pero directo
- Usás analogías simples para explicar conceptos complejos
- Hacés preguntas estratégicas para diagnosticar problemas
- Celebrás los logros y das feedback constructivo
- Hablás como un mentor, no como un robot

📊 TU EXPERTISE:
- Finanzas corporativas y análisis financiero
- Estrategia de negocios y growth hacking
- Análisis de datos y KPIs empresariales
- Proyectos y gestión de cambio organizacional
- Marketing estratégico y posicionamiento

🎨 TU METODOLOGÍA ÚNICA "PROCOLAB":

1. DIAGNÓSTICO CONVERSACIONAL
   - Hacés preguntas específicas y relevantes
   - No asumís nada, preguntás todo
   - Identificás problemas ocultos
   
2. EDUCACIÓN VISUAL
   - Explicás conceptos con ejemplos del mundo real
   - Usás números concretos y proyecciones
   - Mostrás el "antes y después"
   
3. PLAN ACCIONABLE
   - Pasos específicos y medibles
   - Priorización clara (urgente, importante, puede esperar)
   - Timelines realistas
   
4. SEGUIMIENTO EMPÁTICO
   - Preguntás cómo va la implementación
   - Ajustás el plan según feedback
   - Motivás y celebrás avances

💬 TU ESTILO DE COMUNICACIÓN:

SIEMPRE:
- Usás emojis estratégicamente (📊 💰 🎯 ⚠️ ✅)
- Estructurás respuestas con secciones claras
- Das números específicos y cálculos
- Hacés preguntas de seguimiento inteligentes
- Validás los sentimientos del usuario ("Entiendo tu frustración...")

NUNCA:
- Dás respuestas genéricas
- Asumís información que no tenés
- Usás jerga sin explicarla primero
- Sobrecargas con teoría sin acción

🔥 FORMATO DE RESPUESTA TÍPICO:

[Saludo empático + validación]

📊 LO QUE DETECTO:
[Análisis específico con números]

💡 POR QUÉ IMPORTA:
[Impacto real en el negocio]

✅ PLAN DE ACCIÓN:
[Pasos concretos numerados]

🎯 PRÓXIMA PREGUNTA:
[Pregunta estratégica para profundizar]

---

EJEMPLOS DE TU ESTILO:

Usuario: "Mis ventas bajaron"

Tú: "Entiendo tu preocupación. Bajada de ventas siempre es una señal de alerta 🚨

Para ayudarte mejor, necesito entender el panorama completo:

📊 Contame:
1. ¿Cuánto vendías antes vs ahora? (números específicos)
2. ¿En qué período notaste el cambio? (semanas, meses)
3. ¿Cambió algo en tu negocio recientemente? (precios, competencia, equipo)

Con esos datos puedo darte un diagnóstico preciso y un plan de acción concreto 💪"

---

Usuario: "Vendo $50K/mes y quiero llegar a $100K"

Tú: "¡Me encanta! Duplicar ventas es 100% posible con el plan correcto 🚀

📊 SITUACIÓN ACTUAL:
Estás en $50K/mes → Meta: $100K/mes
Gap: $50,000 adicionales por mes

💰 DESGLOSE REALISTA:
Para llegar ahí necesitás:
• +$1,667 por día
• O +12 ventas/día (si tu ticket es $140)
• O +83 ventas/semana

🎯 RUTAS POSIBLES:
Camino A: Más clientes (mismo ticket)
Camino B: Mismo clientes (ticket más alto)
Camino C: Híbrido (lo más efectivo)

🤔 PARA DARTE EL MEJOR PLAN:
1. ¿Cuál es tu ticket promedio actual?
2. ¿Cuántos clientes tenés por mes?
3. ¿Cuánto te cuesta conseguir un cliente nuevo? (aprox)

Con esto armamos tu hoja de ruta personalizada 📈"

---

RECUERDA: 
Tu objetivo no es solo dar información, sino TRANSFORMAR negocios a través de conversaciones estratégicas.
Cada pregunta que hacés es una oportunidad de diagnóstico.
Cada respuesta que das debe incluir ACCIÓN CONCRETA.

Timestamp actual: {timestamp}
"""

# ==================== FUNCIONES ====================
def construir_system_prompt():
    """Construye el prompt del sistema basado en el estilo seleccionado"""
    estilo = st.session_state.get("estilo_respuesta", "⚡ Directo")
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
    return (
        f"Mangi, una IA moderna y profesional creada por Dante Mangiafico. "
        f"{ESTILOS[estilo]} {timestamp}"
    )

def construir_procolab_prompt():
    """Construye el prompt específico para modo PRO COLAB"""
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
    return PROCOLAB_SYSTEM_PROMPT.format(timestamp=timestamp)

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
            st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🛠️ Herramientas")
    
    # BOTÓN PRO COLAB - EL NUEVO
    if st.sidebar.button("🎯 PRO COLAB", use_container_width=True, key="procolab_btn", type="primary"):
        st.session_state.modo_procolab = True
        st.session_state.procolab_fase = "bienvenida"
        st.session_state.mensajes_procolab = []
        st.session_state.datos_negocio = {}
        st.rerun()
    
    if st.sidebar.button("🧠 Prompt Genius", use_container_width=True, key="gen_img", type="secondary"):
        st.session_state.mostrar_generador = True
        st.rerun()

    if st.sidebar.button("🧹 Limpiar conversación", use_container_width=True):
        st.session_state.mensajes = []
        st.session_state.mostrar_bienvenida = True
        st.session_state.modo_procolab = False
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
    if "app_cargada" not in st.session_state:
        st.session_state.app_cargada = False
    if "modo_procolab" not in st.session_state:
        st.session_state.modo_procolab = False
    if "mensajes_procolab" not in st.session_state:
        st.session_state.mensajes_procolab = []
    if "procolab_fase" not in st.session_state:
        st.session_state.procolab_fase = "bienvenida"
    if "datos_negocio" not in st.session_state:
        st.session_state.datos_negocio = {}

def actualizar_historial(rol, contenido, avatar, estilo=None):
    """Agrega un mensaje al historial"""
    st.session_state.mensajes.append({
        "id": str(uuid.uuid4()),
        "role": rol,
        "content": contenido,
        "avatar": avatar,
        "estilo": estilo
    })

def actualizar_historial_procolab(rol, contenido):
    """Agrega un mensaje al historial de PRO COLAB"""
    st.session_state.mensajes_procolab.append({
        "id": str(uuid.uuid4()),
        "role": rol,
        "content": contenido,
        "timestamp": datetime.now().strftime("%H:%M")
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

def mostrar_typing_indicator():
    """Muestra el indicador de escritura animado"""
    st.markdown("""
        <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    """, unsafe_allow_html=True)

def mostrar_historial_procolab():
    """Muestra el historial de PRO COLAB con estilo especial"""
    for m in st.session_state.mensajes_procolab:
        if m["role"] == "assistant":
            st.markdown(f"""
                <div class="procolab-message">
                    <div class="procolab-avatar">
                        🎯 Dr. Marcus Chen
                        <span style="opacity: 0.6; font-size: 0.8rem; margin-left: 8px;">{m['timestamp']}</span>
                    </div>
                    <div style="line-height: 1.6;">
                        {m['content']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            with st.chat_message("user", avatar="💼"):
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

def generar_respuesta_procolab(cliente, modelo, mensaje_usuario):
    """Genera una respuesta en modo PRO COLAB"""
    # Construir contexto completo con historial
    mensajes = [{"role": "system", "content": construir_procolab_prompt()}]
    
    # Agregar historial previo
    for m in st.session_state.mensajes_procolab:
        mensajes.append({
            "role": m["role"],
            "content": m["content"]
        })
    
    # Agregar mensaje actual
    mensajes.append({
        "role": "user",
        "content": mensaje_usuario
    })

    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=mensajes,
        temperature=0.8  # Más creatividad para PRO COLAB
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

# ==================== PANTALLA PRO COLAB ====================
def mostrar_procolab(cliente, modelo):
    """Muestra la interfaz completa de PRO COLAB"""
    
    # Header épico
    st.markdown("""
        <div class="procolab-banner">
            <div class="procolab-title">🎯 PRO COLAB MODE</div>
            <div class="procolab-subtitle">
                Tu copiloto empresarial de élite | Diagnóstico • Estrategia • Resultados
            </div>
            <div class="procolab-stats">
                <div class="procolab-stat">
                    <div class="procolab-stat-number">+284%</div>
                    <div class="procolab-stat-label">Crecimiento Promedio</div>
                </div>
                <div class="procolab-stat">
                    <div class="procolab-stat-number">1,247</div>
                    <div class="procolab-stat-label">Negocios Transformados</div>
                </div>
                <div class="procolab-stat">
                    <div class="procolab-stat-number">98%</div>
                    <div class="procolab-stat-label">Satisfacción</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Botón para salir
    col1, col2, col3 = st.columns([1, 2, 1])
    with col3:
        if st.button("← Volver al chat normal", use_container_width=True):
            st.session_state.modo_procolab = False
            st.rerun()
    
    st.markdown("---")
    
    # Mensaje de bienvenida inicial
    if st.session_state.procolab_fase == "bienvenida" and len(st.session_state.mensajes_procolab) == 0:
        mensaje_bienvenida = """¡Hola! Soy el Dr. Marcus Chen 👋

Soy tu consultor empresarial personal, y estoy acá para ayudarte a transformar tu negocio con datos y estrategia concreta.

🎯 **¿En qué te puedo ayudar hoy?**

Algunos ejemplos:
• "Mis ventas están bajando y no sé por qué"
• "Quiero duplicar mi facturación en 6 meses"
• "No entiendo si mi negocio es rentable"
• "Quiero lanzar un nuevo producto"
• "Necesito reducir costos sin afectar calidad"

💬 **Contame sobre tu negocio y arrancamos...**
"""
        actualizar_historial_procolab("assistant", mensaje_bienvenida)
        st.session_state.procolab_fase = "diagnostico"
    
    # Mostrar historial
    if st.session_state.mensajes_procolab:
        mostrar_historial_procolab()
    
    # Input de usuario
    mensaje_usuario = st.chat_input("Escribe tu consulta empresarial...")
    
    if mensaje_usuario:
        # Agregar mensaje del usuario
        actualizar_historial_procolab("user", mensaje_usuario)
        
        # Mostrar indicador de escritura
        typing_placeholder = st.empty()
        with typing_placeholder:
            mostrar_typing_indicator()
        
        # Generar respuesta
        with st.spinner(""):
            respuesta = generar_respuesta_procolab(cliente, modelo, mensaje_usuario)
        
        typing_placeholder.empty()
        
        # Agregar respuesta
        actualizar_historial_procolab("assistant", respuesta)
        
        st.rerun()

# ==================== APLICACIÓN PRINCIPAL ====================
inicializar_estado()

# ==================== PANTALLA DE CARGA INICIAL ====================
if not st.session_state.app_cargada:
    st.markdown(
        f"""
        <div class="loading-overlay">
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
            
            <img src="data:image/png;base64,{logo_definitivo_base64}" class="loading-logo">
            <div class="loading-text">MANGIAI</div>
            <div class="loading-bar">
                <div class="loading-bar-fill"></div>
            </div>
        </div>
        
        <script>
            setTimeout(function() {{
                window.parent.postMessage({{type: 'streamlit:setComponentValue', value: true}}, '*');
            }}, 3000);
        </script>
        """,
        unsafe_allow_html=True
    )
    
    time.sleep(3)
    st.session_state.app_cargada = True
    st.rerun()

cliente = Groq(api_key=st.secrets["CLAVE_API"])
modelo = configurar_sidebar()

# ==================== MODO PRO COLAB ACTIVADO ====================
if st.session_state.modo_procolab:
    mostrar_procolab(cliente, modelo)

# ==================== GENERADOR DE IMÁGENES ====================
elif st.session_state.get("mostrar_generador", False):
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

# ==================== PANTALLA DE CHAT NORMAL ====================
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

