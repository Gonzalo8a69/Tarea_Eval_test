# app.py
import streamlit as st
import pandas as pd

from interfaz import inyectar_estilos_css, mostrar_logo_corporativo, mostrar_semaforo_ipr, mostrar_indicador_balance, mostrar_tarjetas_poes
from modelos import ModeloProduccionIPR, ModeloPerforacion, ModeloReservorioPOES
from validaciones import validar_produccion_ipr, validar_perforacion_hidrostatica, validar_reservorios_poes
from calculos import calcular_ipr_completo, calcular_presion_hidrostatica, calcular_volumetria_poes
from datos import generar_datos_curva_ipr, preparar_datos_poes_grafico

st.set_page_config(page_title="App SPE - Oil & Gas", page_icon="🛢️", layout="wide")

def renderizar_home():
    mostrar_logo_corporativo()
    st.title("Bootcamp Data Analytics for Oil & Gas")
    
    st.markdown("""
    <div class='tarjeta-kpi'>
        <h4>Información General</h4>
        <p><b>Desarrollador:</b> José Gonzalo Ochoa Paz</p>
        <p><b>Propósito:</b> Plataforma analítica para cálculos de Producción (IPR), Perforación y Reservorios, integrando modelos matemáticos y flujos de evaluación de la SPE.</p>
    </div>
    """, unsafe_allow_html=True)

def renderizar_ejercicios():
    st.title("Módulo Técnico: Ejercicios")
    tab_prod, tab_perf, tab_res = st.tabs(["Producción", "Perforación", "Reservorios"])
    
    with tab_prod:
        col1, col2 = st.columns([1, 2])
        with col1:
            pr = st.number_input("Presión de Reservorio (Pr)", min_value=0.0, value=3000.0)
            pb = st.number_input("Presión de Burbuja (Pb)", min_value=0.0, value=2500.0)
            j = st.number_input("Índice de Productividad (J)", min_value=0.0, value=0.5)
            pwf = st.number_input("Presión de Fondo (Pwf)", min_value=0.0, value=2000.0)
            qo_obj = st.number_input("Caudal Objetivo (Opcional)", min_value=0.0, value=0.0)
            btn_ipr = st.button("Generar IPR", type="primary")
            
        with col2:
            if btn_ipr:
                valido, msj = validar_produccion_ipr(pr, pb, j, pwf)
                if not valido: st.error(msj)
                else:
                    mod_ipr = ModeloProduccionIPR(pr, pb, j, pwf, qo_obj if qo_obj > 0 else None)
                    res_ipr = calcular_ipr_completo(mod_ipr)
                    
                    df_curva = generar_datos_curva_ipr(mod_ipr)
                    st.line_chart(df_curva.set_index("Caudal_Qo_STBd")["Presion_Fondo_Pwf_psi"])
                    mostrar_semaforo_ipr(res_ipr["potencial"])
                    st.success(f"Caudal estimado (qo): {res_ipr['qo']:.2f} STB/d")

    with tab_perf:
        cp1, cp2 = st.columns([1, 2])
        with cp1:
            mw = st.number_input("Peso lodo (MW) [ppg]", value=10.0, step=0.1)
            md = st.number_input("Profundidad Medida (MD) [ft]", value=10000.0, step=100.0)
            tvd = st.number_input("Prof. Vertical (TVD) [ft]", value=9500.0, step=100.0)
            pform = st.number_input("Presión Formación [psi]", value=4800.0, step=100.0)
            btn_perf = st.button("Calcular Hidrostática", type="primary")
            
        with cp2:
            if btn_perf:
                valido, msj = validar_perforacion_hidrostatica(mw, md, tvd, pform)
                if not valido: st.error(msj)
                else:
                    res_perf = calcular_presion_hidrostatica(ModeloPerforacion(mw, md, tvd, pform))
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Gradiente", f"{res_perf['gradiente_psi_ft']:.3f} psi/ft")
                    m2.metric("P. Hidrostática", f"{res_perf['presion_hidrostatica_psi']:.1f} psi")
                    m3.metric("\u0394P", f"{res_perf['diferencial_presion_psi']:.1f} psi")
                    mostrar_indicador_balance(res_perf['diferencial_presion_psi'])

    with tab_res:
        cr1, cr2 = st.columns([1, 2])
        with cr1:
            a = st.number_input("Área [acres]", value=500.0)
            h = st.number_input("Espesor bruto [ft]", value=50.0)
            ntg = st.number_input("NTG [fracción]", value=0.8)
            poro = st.number_input("Porosidad [fracción]", value=0.2)
            swi = st.number_input("Swi [fracción]", value=0.25)
            boi = st.number_input("Boi [rb/STB]", value=1.2)
            fr = st.number_input("Factor Recobro", value=0.3)
            btn_res = st.button("Estimar Volumetría", type="primary")
            
        with cr2:
            if btn_res:
                valido, msj = validar_reservorios_poes(a, h, ntg, poro, swi, boi, fr)
                if not valido: st.error(msj)
                else:
                    res = calcular_volumetria_poes(ModeloReservorioPOES(a, h, ntg, poro, swi, boi, fr))
                    mostrar_tarjetas_poes(res['poes_mmstb'], res['recuperable_mmstb'])
                    df_poes = preparar_datos_poes_grafico(res['poes_stb'], res['recuperable_stb'])
                    st.bar_chart(df_poes.set_index("Categoría"))

def main():
    inyectar_estilos_css()
    st.sidebar.title("Navegación")
    if st.sidebar.radio("Ir a:", ["Home", "Ejercicios"]) == "Home":
        renderizar_home()
    else:
        renderizar_ejercicios()

if __name__ == "__main__":
    main()