# datos.py
import pandas as pd
import numpy as np
from modelos import ModeloProduccionIPR
from calculos import calcular_ipr_completo 

def generar_datos_curva_ipr(modelo: ModeloProduccionIPR, num_puntos: int = 50) -> pd.DataFrame:
    pwf_array = np.linspace(modelo.pr, 0, num_puntos)
    caudales = []
    
    for pwf_actual in pwf_array:
        mod_temp = ModeloProduccionIPR(modelo.pr, modelo.pb, modelo.j, pwf_actual)
        res = calcular_ipr_completo(mod_temp)
        caudales.append(res["qo"])
        
    return pd.DataFrame({
        "Presion_Fondo_Pwf_psi": pwf_array, 
        "Caudal_Qo_STBd": caudales
    })

def preparar_datos_poes_grafico(poes: float, recuperable: float) -> pd.DataFrame:
    return pd.DataFrame({
        "Categoría": ["POES", "Recuperable"],
        "Volumen_MMSTB": [poes / 1_000_000, recuperable / 1_000_000]
    })
