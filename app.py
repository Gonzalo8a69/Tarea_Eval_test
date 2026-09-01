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
            <b>Desarrollador:</b> José Gonzalo Ochoa Paz<br>
            <b>Propósito:</b> Integración de modelos matemáticos para Producción (IPR), Perforación e Ingeniería de Reservorios.
        </p>
    </div>
    """, unsafe_allow_html=True)

def renderizar_ejercicios():
    st.title("Módulo Técnico: Ejercicios")
    tab_prod, tab_perf, tab_res = st.tabs(["Producción", "Perforación", "Reservorios"])
    
    with tab_prod:
        mostrar_header_seccion("Cálculo IPR Compuesta", "Modelo de reservorio subsaturado y diagnóstico de afluencia.")
        col_in_prod, col_out_prod = st.columns([1, 2])
        
        with col_in_prod:
            pr = st.number_input("Presión de Reservorio (Pr) [psi]", min_value=0.0, value=3000.0)
            pb = st.number_input("Presión de Burbuja (Pb) [psi]", min_value=0.0, value=2500.0)
            j = st.number_input("Índice de Productividad (J) [STB/d/psi]", min_value=0.0, value=0.5)
            pwf = st.number_input("Presión de Fondo (Pwf) [psi]", min_value=0.0, value=2000.0)
            qo_obj = st.number_input("Caudal Objetivo (Opcional) [STB/d]", min_value=0.0, value=0.0)
            btn_ipr = st.button("Generar Curva IPR", type="primary", use_container_width=True)
            
        with col_out_prod:
            if btn_ipr:
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

    with tab_perf:
        mostrar_header_seccion("Presión Hidrostática", "Evaluación del lodo de perforación y gradiente de presión.")
        col_in_perf, col_out_perf = st.columns([1, 2])
        
        with col_in_perf:
            mw = st.number_input("Peso lodo (MW) [ppg]", value=10.0, step=0.1)
            md = st.number_input("Profundidad Medida (MD) [ft]", value=10000.0, step=100.0)
            tvd = st.number_input("Prof. Vertical (TVD) [ft]", value=9500.0, step=100.0)
            pform = st.number_input("Presión Formación [psi]", value=4800.0, step=100.0)
            btn_perf = st.button("Calcular Hidrostática", type="primary", use_container_width=True)
            
        with col_out_perf:
            if btn_perf:
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
        mostrar_header_seccion("Estimación Volumétrica", "Cálculo del Petróleo Original en Sitio (POES).")
        col_in_res, col_out_res = st.columns([1, 2])
        
        with col_in_res:
            a = st.number_input("Área [acres]", value=500.0)
            h = st.number_input("Espesor bruto [ft]", value=50.0)
            ntg = st.number_input("NTG [fracción]", value=0.8, step=0.05)
            poro = st.number_input("Porosidad [fracción]", value=0.2, step=0.05)
            swi = st.number_input("Swi [fracción]", value=0.25, step=0.05)
            boi = st.number_input("Boi [rb/STB]", value=1.2, step=0.1)
            fr = st.number_input("Factor Recobro", value=0.3, step=0.05)
            btn_res = st.button("Estimar POES", type="primary", use_container_width=True)
            
        with col_out_res:
            if btn_res:
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
    
    # Ruteo lateral clásico[cite: 4]
    if st.sidebar.radio("Módulos:", ["Home", "Ejercicios"]) == "Home":
        renderizar_home()
    else:
        renderizar_ejercicios()

if __name__ == "__main__":
    main()

def renderizar_home():
    """Renderiza la página principal con diseño corporativo."""
    mostrar_header_seccion(
        "Bootcamp Data Analytics for Oil & Gas", 
        "Plataforma Avanzada de Cálculos de Ingeniería"
    )
    
    # Uso de la tarjeta personalizada para la identidad del desarrollador
    st.markdown("""
    <div class='card-resultado' style='border-left-color: var(--color-secondary);'>
        <div class='card-titulo'>Identidad del Proyecto</div>
        <p style='color: var(--color-text-primary); font-size: 1.1em; margin-top: 10px;'>
            <b>Organización:</b> CONSORCIO BESTENERGY REDO<br>
            <b>Propósito:</b> Integración de modelos matemáticos para Producción (IPR), Perforación (Hidrostática) y Reservorios (POES).
        </p>
    </div>
    """, unsafe_allow_html=True)

def renderizar_ejercicios():
    """Orquesta el flujo técnico y consume los componentes visuales personalizados."""
    st.title("Módulo Técnico: Ejercicios")
    
    # Creación de tabs nativos de Streamlit[cite: 2]
    tab_prod, tab_perf, tab_res = st.tabs(["Producción", "Perforación", "Reservorios"])[cite: 2]
    
    # ==========================================
    # TAB 1: PRODUCCIÓN (IPR)
    # ==========================================
    with tab_prod:
        mostrar_header_seccion("Cálculo IPR Compuesta", "Modelo de reservorio subsaturado y diagnóstico de afluencia.")[cite: 2]
        
        col_in_prod, col_out_prod = st.columns([1, 2])
        with col_in_prod:
            pr = st.number_input("Presión de Reservorio (Pr) [psi]", min_value=0.0, value=3000.0)[cite: 2]
            pb = st.number_input("Presión de Burbuja (Pb) [psi]", min_value=0.0, value=2500.0)[cite: 2]
            j = st.number_input("Índice de Productividad (J) [STB/d/psi]", min_value=0.0, value=0.5)[cite: 2]
            pwf = st.number_input("Presión de Fondo (Pwf) [psi]", min_value=0.0, value=2000.0)[cite: 2]
            qo_obj = st.number_input("Caudal Objetivo (Opcional) [STB/d]", min_value=0.0, value=0.0)
            btn_ipr = st.button("Generar Curva IPR", type="primary", use_container_width=True)
            
        with col_out_prod:
            if btn_ipr:
                valido, msj = validar_produccion_ipr(pr, pb, j, pwf)
                if not valido:
                    st.error(msj)
                else:
                    mod_ipr = ModeloProduccionIPR(pr, pb, j, pwf, qo_obj if qo_obj > 0 else None)
                    res_ipr = calcular_ipr_completo(mod_ipr)
                    
                    # Interfaz avanzada: Tarjetas y Semáforos
                    mostrar_tarjeta_resultado("Caudal Estimado (qo)", res_ipr['qo'], "STB/d")
                    mostrar_semaforo_ipr(res_ipr["potencial"])[cite: 1]
                    
                    # Gráfico nativo optimizado[cite: 2]
                    df_curva = generar_datos_curva_ipr(mod_ipr)
                    st.line_chart(df_curva.set_index("Caudal_Qo_STBd")["Presion_Fondo_Pwf_psi"])

    # ==========================================
    # TAB 2: PERFORACIÓN
    # ==========================================
    with tab_perf:
        mostrar_header_seccion("Presión Hidrostática", "Evaluación del lodo de perforación y gradiente de presión.")[cite: 2]
        
        col_in_perf, col_out_perf = st.columns([1, 2])
        with col_in_perf:
            mw = st.number_input("Peso lodo (MW) [ppg]", value=10.0, step=0.1)[cite: 2]
            md = st.number_input("Profundidad Medida (MD) [ft]", value=10000.0, step=100.0)[cite: 2]
            tvd = st.number_input("Prof. Vertical (TVD) [ft]", value=9500.0, step=100.0)[cite: 2]
            pform = st.number_input("Presión Formación [psi]", value=4800.0, step=100.0)[cite: 2]
            btn_perf = st.button("Calcular Hidrostática", type="primary", use_container_width=True)
            
        with col_out_perf:
            if btn_perf:
                valido, msj = validar_perforacion_hidrostatica(mw, md, tvd, pform)
                if not valido: 
                    st.error(msj)
                else:
                    res_perf = calcular_presion_hidrostatica(ModeloPerforacion(mw, md, tvd, pform))
                    
                    # Interfaz avanzada: Tarjetas Flexbox
                    m1, m2 = st.columns(2)
                    with m1:
                        mostrar_tarjeta_resultado("P. Hidrostática", res_perf['presion_hidrostatica_psi'], "psi")
                    with m2:
                        mostrar_tarjeta_resultado("Diferencial (\u0394P)", res_perf['diferencial_presion_psi'], "psi", borde_color="var(--color-warning)")
                    
                    st.info(f"**Gradiente Calculado:** {res_perf['gradiente_psi_ft']:.3f} psi/ft")[cite: 2]

    # ==========================================
    # TAB 3: RESERVORIOS
    # ==========================================
    with tab_res:
        mostrar_header_seccion("Estimación Volumétrica", "Cálculo del Petróleo Original en Sitio (POES).")[cite: 2]
        
        col_in_res, col_out_res = st.columns([1, 2])
        with col_in_res:
            a = st.number_input("Área [acres]", value=500.0)[cite: 2]
            h = st.number_input("Espesor bruto [ft]", value=50.0)[cite: 2]
            ntg = st.number_input("NTG [fracción]", value=0.8, step=0.05)[cite: 2]
            poro = st.number_input("Porosidad [fracción]", value=0.2, step=0.05)[cite: 2]
            swi = st.number_input("Swi [fracción]", value=0.25, step=0.05)[cite: 2]
            boi = st.number_input("Boi [rb/STB]", value=1.2, step=0.1)[cite: 2]
            fr = st.number_input("Factor Recobro", value=0.3, step=0.05)[cite: 2]
            btn_res = st.button("Estimar POES", type="primary", use_container_width=True)
            
        with col_out_res:
            if btn_res:
                valido, msj = validar_reservorios_poes(a, h, ntg, poro, swi, boi, fr)
                if not valido: 
                    st.error(msj)
                else:
                    res = calcular_volumetria_poes(ModeloReservorioPOES(a, h, ntg, poro, swi, boi, fr))
                    
                    # Interfaz avanzada: Tarjetas KPI para Reservorios
                    c1, c2 = st.columns(2)
                    with c1:
                        mostrar_tarjeta_resultado("POES", res['poes_mmstb'], "MMSTB", borde_color="var(--color-primary)")[cite: 2]
                    with c2:
                        mostrar_tarjeta_resultado("Recuperable", res['recuperable_mmstb'], "MMSTB", borde_color="var(--color-secondary)")[cite: 2]
                    
                    df_poes = preparar_datos_poes_grafico(res['poes_stb'], res['recuperable_stb'])[cite: 2]
                    st.bar_chart(df_poes.set_index("Categoría"))

def main():
    # 2. Inyección global de estilos (Asegura que las clases CSS existan)
    inyectar_estilos_css()
    
    # 3. Navegación Estricta[cite: 2, 4]
    st.sidebar.title("Navegación")
    opcion = st.sidebar.radio("Módulos:", ["Home", "Ejercicios"])
    
    if opcion == "Home":
        renderizar_home()
    else:
        renderizar_ejercicios()

if __name__ == "__main__":
    main()
