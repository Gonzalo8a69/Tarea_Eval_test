# app.py
import streamlit as st
import pandas as pd

from interfaz import inyectar_estilos_css, mostrar_header_seccion, mostrar_tarjeta_resultado, mostrar_semaforo_ipr
from modelos import ModeloProduccionIPR, ModeloPerforacion, ModeloReservorioPOES
from validaciones import validar_produccion_ipr, validar_perforacion_hidrostatica, validar_reservorios_poes
from calculos import calcular_ipr_completo, calcular_presion_hidrostatica, calcular_volumetria_poes
from datos import generar_datos_curva_ipr, preparar_datos_poes_grafico

st.set_page_config(page_title="App SPE - Análisis de Ingeniería", page_icon="🛢️", layout="wide")

def renderizar_home():
    mostrar_header_seccion("Bootcamp Data Analytics for Oil & Gas", "Plataforma Avanzada de Cálculos de Ingeniería")
    st.markdown("""
    <div class='card-resultado' style='border-left-color: var(--color-secondary);'>
        <div class='card-titulo'>Identidad del Proyecto</div>
        <p style='color: var(--color-text-primary); font-size: 1.1em; margin-top: 10px;'>
            <b>Organización:</b> CONSORCIO BESTENERGY REDO<br>
            <b>Propósito:</b> Integración reactiva de modelos matemáticos para Producción (IPR), Perforación e Ingeniería de Reservorios.
        </p>
    </div>
    """, unsafe_allow_html=True)

def renderizar_ejercicios():
    st.title("Módulo Técnico: Ejercicios")
    tab_prod, tab_perf, tab_res = st.tabs(["Producción", "Perforación", "Reservorios"])
    
    with tab_prod:
        mostrar_header_seccion("Cálculo IPR Compuesta", "Modelo subsaturado interactivo.")
        col_in_prod, col_out_prod = st.columns([1, 2])
        
        with col_in_prod:
            pr = st.number_input("Presión de Reservorio (Pr) [psi]", min_value=1.0, value=3000.0, step=100.0)
            pb = st.number_input("Presión de Burbuja (Pb) [psi]", min_value=0.0, value=2500.0, step=100.0)
            j = st.number_input("Índice de Productividad (J)", min_value=0.01, value=0.5, step=0.1)
            pwf = st.number_input("Presión de Fondo (Pwf) [psi]", min_value=0.0, value=2000.0, step=100.0)
            qo_obj = st.number_input("Caudal Objetivo (Opcional)", min_value=0.0, value=0.0)
            
        with col_out_prod:
            valido, msj = validar_produccion_ipr(pr, pb, j, pwf)
            if not valido:
                st.error(msj)
            else:
                mod_ipr = ModeloProduccionIPR(pr, pb, j, pwf, qo_obj if qo_obj > 0 else None)
                res_ipr = calcular_ipr_completo(mod_ipr)
                
                # Renderizado automático y reactivo
                mostrar_tarjeta_resultado("Caudal Estimado (qo)", res_ipr['qo'], "STB/d")
                mostrar_semaforo_ipr(res_ipr["potencial"])
                
                df_curva = generar_datos_curva_ipr(mod_ipr)
                st.line_chart(df_curva.set_index("Caudal_Qo_STBd")["Presion_Fondo_Pwf_psi"])

    with tab_perf:
        mostrar_header_seccion("Presión Hidrostática", "Evaluación reactiva del lodo.")
        col_in_perf, col_out_perf = st.columns([1, 2])
        
        with col_in_perf:
            mw = st.number_input("Peso lodo (MW) [ppg]", min_value=0.1, value=10.0, step=0.1)
            md = st.number_input("Profundidad Medida (MD) [ft]", min_value=1.0, value=10000.0, step=100.0)
            tvd = st.number_input("Prof. Vertical (TVD) [ft]", min_value=1.0, value=9500.0, step=100.0)
            pform = st.number_input("Presión Formación [psi]", min_value=0.0, value=4800.0, step=100.0)
            
        with col_out_perf:
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

    with tab_res:
        mostrar_header_seccion("Estimación Volumétrica", "Cálculo instantáneo de POES.")
        col_in_res, col_out_res = st.columns([1, 2])
        
        with col_in_res:
            a = st.number_input("Área [acres]", min_value=0.1, value=500.0)
            h = st.number_input("Espesor bruto [ft]", min_value=0.1, value=50.0)
            ntg = st.number_input("NTG [fracción]", min_value=0.0, max_value=1.0, value=0.8, step=0.05)
            poro = st.number_input("Porosidad [fracción]", min_value=0.0, max_value=1.0, value=0.2, step=0.05)
            swi = st.number_input("Swi [fracción]", min_value=0.0, max_value=1.0, value=0.25, step=0.05)
            boi = st.number_input("Boi [rb/STB]", min_value=0.1, value=1.2, step=0.1)
            fr = st.number_input("Factor Recobro", min_value=0.0, max_value=1.0, value=0.3, step=0.05)
            
        with col_out_res:
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

def main():
    inyectar_estilos_css()
    st.sidebar.title("Navegación")
    
    if st.sidebar.radio("Módulos:", ["Home", "Ejercicios"]) == "Home":
        renderizar_home()
    else:
        renderizar_ejercicios()

if __name__ == "__main__":
    main()
