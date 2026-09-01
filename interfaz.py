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
        }
        .tarjeta-kpi {
            background-color: var(--color-surface);
            border-left: 5px solid var(--color-primary-light);
            padding: 15px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 15px;
        }
        .tarjeta-kpi h4 { color: var(--color-primary); margin-top: 0; }
    </style>
    """
    st.markdown(estilo, unsafe_allow_html=True)

def mostrar_logo_corporativo():
    html = """
    <div style='text-align: center; padding: 10px 0; border-bottom: 2px solid var(--color-primary); margin-bottom: 20px;'>
        <h2 style='color: var(--color-primary); font-weight: bold; margin: 0;'>CONSORCIO BESTENERGY REDO</h2>
        <p style='color: var(--color-text-secondary); font-style: italic; margin: 0;'>División de Analítica e Ingeniería</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def mostrar_semaforo_ipr(potencial: float):
    if potencial < 50:
        color, texto = "#0da68c", "Operación Conservadora"
    elif 50 <= potencial <= 80:
        color, texto = "#e8ba30", "Operación Óptima"
    else:
        color, texto = "#b34d00", "Riesgo Inminente"
    st.markdown(f"<div style='background-color:{color}; color:#fff; padding:12px; border-radius:6px; text-align:center; font-weight:bold;'>Índice de Potencial: {potencial:.1f}% - {texto}</div>", unsafe_allow_html=True)

def mostrar_indicador_balance(delta_p: float):
    if delta_p > 100:
        color, estado = "var(--color-primary-light)", "🟢 SOBREBALANCE"
    elif abs(delta_p) <= 100:
        color, estado = "var(--color-warning)", "🟡 BALANCE APROXIMADO"
    else:
        color, estado = "var(--color-accent-light)", "🔴 BAJO BALANCE"
    st.markdown(f"<div style='background-color:{color}; color:#fff; padding:12px; border-radius:6px; text-align:center; font-weight:bold; margin-top:10px;'>{estado} (\u0394P: {delta_p:.1f} psi)</div>", unsafe_allow_html=True)

def mostrar_tarjetas_poes(poes: float, rec: float):
    html = f"""
    <div style='display:flex; gap:15px; margin-top:15px;'>
        <div style='flex:1; background:var(--color-surface); border-left:5px solid var(--color-primary); padding:15px; border-radius:8px;'>
            <h4 style='color:var(--color-primary); margin:0;'>POES Estimado</h4><h2 style='margin:0;'>{poes:.2f} <span style='font-size:0.5em;'>MMSTB</span></h2>
        </div>
        <div style='flex:1; background:var(--color-surface); border-left:5px solid var(--color-secondary); padding:15px; border-radius:8px;'>
            <h4 style='color:var(--color-secondary); margin:0;'>Volumen Recuperable</h4><h2 style='margin:0;'>{rec:.2f} <span style='font-size:0.5em;'>MMSTB</span></h2>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)