# app.py
import streamlit as st
import pandas as pd

from interfaz import (
    inyectar_estilos_css, 
    mostrar_header_seccion, 
    mostrar_tarjeta_resultado, 
    mostrar_semaforo_ipr
)
from modelos import ModeloProduccionIPR, ModeloPerforacion, ModeloReservorioPOES
from validaciones import validar_produccion_ipr, validar_perforacion_hidrostatica, validar_reservorios_poes
from calculos import calcular_ipr_completo, calcular_presion_hidrostatica, calcular_volumetria_poes
from datos import generar_datos_curva_ipr, preparar_datos_poes_grafico

st.set_page_config(
    page_title="App SPE - Análisis de Ingeniería", 
    page_icon="🛢️", 
    layout="wide"
)

def renderizar_home():
    mostrar_header_seccion("Bootcamp Data Analytics for Oil & Gas", "Plataforma Avanzada de Cálculos de Ingeniería")
    st.markdown("""
    <div class='card-resultado' style='border-left-color: var(--color-secondary);'>
        <div class='card-titulo'>Identidad del Proyecto</div>
        <p style='color: var(--color-text-primary); font-size: 1.1em; margin-top: 10px;'>
            <b>Organización:</b> CONSORCIO BESTENERGY REDO<br>
            <b>Desarrollador:</b> José Gonzalo Ochoa Paz<br>
            <b>Propósito:</b> Integración de modelos matemáticos avanzados para Producción (IPR), Perforación e Ingeniería de Reservorios con control de ejecución por botones.
        </p>
    </div>
    """, unsafe_allow_html=True)

def renderizar_ejercicios():
    st.title("Módulo Técnico: Ejercicios")
    
    # Navegación por pestañas (Tabs) según requerimiento de la rúbrica
    tab_prod, tab_perf, tab_res = st.tabs(["Producción", "Perforación", "Reservorios"])
    
    # ==========================================
    # 1. TAB PRODUCCIÓN (IPR)
    # ==========================================
    with tab_prod:
        mostrar_header_seccion("Cálculo IPR Compuesta", "Modelo de reservorio subsaturado con control de ejecución.")
        col_in_prod, col_out_prod = st.columns([1, 2])
        
        with col_in_prod:
            pr = st.number_input("Presión de Reservorio (Pr) [psi]", min_value=1.0, value=3000.0, step=100.0, key="pr_prod")
            pb = st.number_input("Presión de Burbuja (Pb) [psi]", min_value=0.0, value=2500.0, step=100.0, key="pb_prod")
            j = st.number_input("Índice de Productividad (J) [STB/d/psi]", min_value=0.01, value=0.5, step=0.1, key="j_prod")
            pwf = st.number_input("Presión de Fondo (Pwf) [psi]", min_value=0.0, value=2000.0, step=100.0, key="pwf_prod")
            qo_obj = st.number_input("Caudal Objetivo (Opcional) [STB/d]", min_value=0.0, value=0.0, key="qo_prod")
            
            # Botón de cálculo respaldado por Session State
            btn_calcular_ipr = st.button("Calcular IPR y Diagnóstico", type="primary", use_container_width=True, key="btn_ipr")
            
            if btn_calcular_ipr:
                st.session_state["ejecutar_ipr"] = True

        with col_out_prod:
            if st.session_state.get("ejecutar_ipr", False):
                valido, msj = validar_produccion_ipr(pr, pb, j, pwf)
                if not valido:
                    st.error(msj)
                else:
                    mod_ipr = ModeloProduccionIPR(pr, pb, j, pwf, qo_obj if qo_obj > 0 else None)
                    res_ipr = calcular_ipr_completo(mod_ipr)
                    
                    mostrar_tarjeta_resultado("Caudal Estimado (qo)", res_ipr['qo'], "STB/d")
                    mostrar_semaforo_ipr(res_ipr["potencial"])
                    
                    df_curva = generar_datos_curva_ipr(mod_ipr)
                    st.line_chart(df_curva.set_index("Caudal_Qo_STBd")["Presion_Fondo_Pwf_psi"])
            else:
                st.info("👈 Ingrese los parámetros en el panel izquierdo y haga clic en **Calcular IPR y Diagnóstico**.")

    # ==========================================
    # 2. TAB PERFORACIÓN
    # ==========================================
    with tab_perf:
        mostrar_header_seccion("Presión Hidrostática", "Evaluación de la columna de lodo y gradientes.")
        col_in_perf, col_out_perf = st.columns([1, 2])
        
        with col_in_perf:
            mw = st.number_input("Peso lodo (MW) [ppg]", min_value=0.1, value=10.0, step=0.1, key="mw_perf")
            md = st.number_input("Profundidad Medida (MD) [ft]", min_value=1.0, value=10000.0, step=100.0, key="md_perf")
            tvd = st.number_input("Prof. Vertical (TVD) [ft]", min_value=1.0, value=9500.0, step=100.0, key="tvd_perf")
            pform = st.number_input("Presión Formación [psi]", min_value=0.0, value=4800.0, step=100.0, key="pform_perf")
            
            btn_calcular_perf = st.button("Calcular Presión Hidrostática", type="primary", use_container_width=True, key="btn_perf")
            
            if btn_calcular_perf:
                st.session_state["ejecutar_perf"] = True

        with col_out_perf:
            if st.session_state.get("ejecutar_perf", False):
                valido, msj = validar_perforacion_hidrostatica(mw, md, tvd, pform)
                if not valido: 
                    st.error(msj)
                else:
                    res_perf = calcular_presion_hidrostatica(ModeloPerforacion(mw, md, tvd, pform))
                    m1, m2 = st.columns(2)
                    with m1:
                        mostrar_tarjeta_resultado("P. Hidrostática", res_perf['presion_hidrostatica_psi'], "psi")
                    with m2:
                        mostrar_tarjeta_resultado("Diferencial (\u0394P)", res_perf['diferencial_presion_psi'], "psi", "var(--color-warning)")
                    st.info(f"**Gradiente Calculado:** {res_perf['gradiente_psi_ft']:.3f} psi/ft")
            else:
                st.info("👈 Configure los datos del pozo y haga clic en **Calcular Presión Hidrostática**.")

    # ==========================================
    # 3. TAB RESERVORIOS
    # ==========================================
    with tab_res:
        mostrar_header_seccion("Estimación Volumétrica", "Cálculo analítico del POES y volumen recuperable.")
        col_in_res, col_out_res = st.columns([1, 2])
        
        with col_in_res:
            a = st.number_input("Área [acres]", min_value=0.1, value=500.0, key="a_res")
            h = st.number_input("Espesor bruto [ft]", min_value=0.1, value=50.0, key="h_res")
            ntg = st.number_input("NTG [fracción]", min_value=0.0, max_value=1.0, value=0.8, step=0.05, key="ntg_res")
            poro = st.number_input("Porosidad [fracción]", min_value=0.0, max_value=1.0, value=0.2, step=0.05, key="poro_res")
            swi = st.number_input("Swi [fracción]", min_value=0.0, max_value=1.0, value=0.25, step=0.05, key="swi_res")
            boi = st.number_input("Boi [rb/STB]", min_value=0.1, value=1.2, step=0.1, key="boi_res")
            fr = st.number_input("Factor Recobro", min_value=0.0, max_value=1.0, value=0.3, step=0.05, key="fr_res")
            
            btn_calcular_res = st.button("Estimar POES", type="primary", use_container_width=True, key="btn_res")
            
            if btn_calcular_res:
                st.session_state["ejecutar_res"] = True

        with col_out_res:
            if st.session_state.get("ejecutar_res", False):
                valido, msj = validar_reservorios_poes(a, h, ntg, poro, swi, boi, fr)
                if not valido: 
                    st.error(msj)
                else:
                    res = calcular_volumetria_poes(ModeloReservorioPOES(a, h, ntg, poro, swi, boi, fr))
                    c1, c2 = st.columns(2)
                    with c1:
                        mostrar_tarjeta_resultado("POES", res['poes_mmstb'], "MMSTB", "var(--color-primary)")
                    with c2:
                        mostrar_tarjeta_resultado("Recuperable", res['recuperable_mmstb'], "MMSTB", "var(--color-secondary)")
                    
                    df_poes = preparar_datos_poes_grafico(res['poes_stb'], res['recuperable_stb'])
                    st.bar_chart(df_poes.set_index("Categoría"))
            else:
                st.info("👈 Ingrese las propiedades volumétricas y haga clic en **Estimar POES**.")

def main():
    inyectar_estilos_css()
    st.sidebar.title("Navegación")
    
    # Ruteo estricto lateral entre Home y Ejercicios
    if st.sidebar.radio("Módulos:", ["Home", "Ejercicios"]) == "Home":
        renderizar_home()
    else:
        renderizar_ejercicios()

if __name__ == "__main__":
    main()
