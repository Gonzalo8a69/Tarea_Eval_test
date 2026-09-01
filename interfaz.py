# interfaz.py
import streamlit as st

def inyectar_estilos_css():
    estilo = """
    <style>
        :root {
            --color-primary-light: #0da68c;
            --color-primary: #004d40;
            --color-secondary-light: #10bfaa;
            --color-secondary: #00695c;
            --color-secondary-dark: #004d43;
            --color-accent-light: #b34d00;
            --color-accent: #4d2100;
            --color-warning: #e8ba30;
            --color-background: #ffffff;
            --color-surface: #fafafa;
            --color-text-primary: #181b1a;
            --color-text-secondary: #616b69;
            --color-text-disabled: #a1aaa9;
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        .stApp { background-color: var(--color-surface); }

        .card-resultado {
            background-color: var(--color-background);
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
            border-left: 6px solid var(--color-primary-light);
            margin-bottom: 20px;
            transition: transform 0.2s ease;
        }
        
        .card-resultado:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.12);
        }

        .card-titulo {
            color: var(--color-text-secondary);
            font-size: 0.95rem;
            text-transform: uppercase;
            font-weight: 600;
            margin-bottom: 5px;
        }

        .card-valor {
            color: var(--color-primary);
            font-size: 2.2rem;
            font-weight: 800;
            line-height: 1.2;
            margin: 0;
        }
        
        .card-unidad { font-size: 0.4em; color: var(--color-text-disabled); vertical-align: text-bottom; }
        
        .semaforo-container {
            border-radius: 8px; padding: 15px 20px; display: flex; align-items: center; 
            justify-content: space-between; box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
            color: white; margin-top: 15px; margin-bottom: 20px;
        }
    </style>
    """
    st.markdown(estilo, unsafe_allow_html=True)

def mostrar_header_seccion(titulo: str, descripcion: str):
    html = f"""
    <div style="margin-bottom: 25px; padding-bottom: 10px; border-bottom: 2px solid var(--color-secondary-light);">
        <h2 style="color: var(--color-primary); margin-bottom: 5px; font-weight: 800;">{titulo}</h2>
        <p style="color: var(--color-text-secondary); margin: 0; font-size: 1.1rem;">{descripcion}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def mostrar_tarjeta_resultado(titulo: str, valor: float, unidad: str, borde_color: str = "var(--color-primary-light)"):
    html = f"""
    <div class="card-resultado" style="border-left-color: {borde_color};">
        <div class="card-titulo">{titulo}</div>
        <div class="card-valor">{valor:,.2f} <span class="card-unidad">{unidad}</span></div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def mostrar_semaforo_ipr(potencial: float):
    if potencial < 50: color, estado, icono = "var(--color-primary-light)", "Operación Conservadora", "🛡️"
    elif 50 <= potencial <= 80: color, estado, icono = "var(--color-warning)", "Operación Óptima", "⚡"
    else: color, estado, icono = "var(--color-accent-light)", "Riesgo Inminente", "⚠️"
        
    html = f"""
    <div class="semaforo-container" style="background-color: {color};">
        <div>
            <div style="font-size: 0.9em; text-transform: uppercase;">Diagnóstico IPR</div>
            <div style="font-size: 1.2em; font-weight: bold;">{icono} {estado}</div>
        </div>
        <div style="font-size: 2.5em; font-weight: 800;">{potencial:.1f}%</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
