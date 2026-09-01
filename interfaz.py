# interfaz.py
import streamlit as st

def inyectar_estilos_css():
    """Inyecta CSS avanzado para efectos hover, sombras y botones modernos."""
    estilo = """
    <style>
        :root {
            --color-primary-light: #0da68c;
            --color-primary: #004d40;
            --color-secondary-light: #10bfaa;
            --color-secondary: #00695c;
            --color-accent-light: #b34d00;
            --color-warning: #e8ba30;
            --color-background: #ffffff;
            --color-surface: #fafafa;
            --color-text-primary: #181b1a;
            --color-text-secondary: #616b69;
        }

        /* Fondo y tipografía general */
        .stApp {
            background-color: var(--color-surface);
            color: var(--color-text-primary);
        }

        /* 1. Modernización de Botones Nativos de Streamlit */
        .stButton > button {
            background: linear-gradient(135deg, var(--color-primary-light) 0%, var(--color-primary) 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            box-shadow: 0 4px 6px rgba(0, 77, 64, 0.2);
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0, 77, 64, 0.3);
            border-color: transparent;
            color: white;
        }

        .stButton > button:active {
            transform: translateY(1px);
        }

        /* 2. Tarjetas de Resultados con Hover Effects */
        .card-premium {
            background-color: var(--color-background);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
            border-left: 6px solid var(--color-primary-light);
            margin-bottom: 20px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .card-premium:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        }
        
        .card-titulo {
            color: var(--color-text-secondary);
            font-size: 0.9rem;
            text-transform: uppercase;
            font-weight: 700;
        }
        
        .card-valor {
            color: var(--color-primary);
            font-size: 2.5rem;
            font-weight: 800;
            line-height: 1.1;
        }
    </style>
    """
    st.markdown(estilo, unsafe_allow_html=True)

def mostrar_tarjeta(titulo: str, valor: float, unidad: str, color_borde: str = "var(--color-primary-light)"):
    """Renderiza una tarjeta HTML/CSS interactiva para mostrar métricas clave."""
    html = f"""
    <div class="card-premium" style="border-left-color: {color_borde};">
        <div class="card-titulo">{titulo}</div>
        <div class="card-valor">{valor:,.2f} <span style="font-size: 0.4em; color: var(--color-text-secondary);">{unidad}</span></div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
