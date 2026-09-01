# app.py
import streamlit as st
from interfaz import inyectar_estilos_css, mostrar_tarjeta
# Importar calculos.py, modelos.py, etc.

st.set_page_config(page_title="App SPE - Oil & Gas", layout="wide")

def main():
    # Inyectar CSS global al inicio para transformar la UI inmediatamente
    inyectar_estilos_css()
    
    st.sidebar.title("Navegación")
    modulo = st.sidebar.radio("Módulos:", ["Home", "Ejercicios"])
    
    if modulo == "Ejercicios":
        tab_prod, tab_perf, tab_res = st.tabs(["Producción", "Perforación", "Reservorios"])
        
        with tab_prod:
            st.markdown("### Cálculo IPR Compuesta")
            
            # El botón nativo ahora tendrá el diseño moderno del CSS inyectado
            if st.button("Ejecutar Simulación IPR", key="btn_ipr"):
                # Ejemplo de uso de la tarjeta interactiva
                mostrar_tarjeta("Caudal Máximo Teórico", 1500.50, "STB/d")

if __name__ == "__main__":
    main()
