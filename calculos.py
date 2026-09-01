# calculos.py
import math
from modelos import ModeloProduccionIPR, ModeloPerforacion, ModeloReservorioPOES

def calcular_ipr_completo(modelo: ModeloProduccionIPR) -> dict:
    qb = modelo.j * (modelo.pr - modelo.pb)
    qo_max = qb + (modelo.j * modelo.pb) / 1.8
    
    # Selección de régimen de flujo
    if modelo.pwf >= modelo.pb:
        qo = modelo.j * (modelo.pr - modelo.pwf)
    else:
        relacion_presion = modelo.pwf / modelo.pb
        termino_vogel = 1 - 0.2 * (relacion_presion) - 0.8 * (relacion_presion)**2
        qo = qb + ((modelo.j * modelo.pb) / 1.8) * termino_vogel
        
    resultados = {
        "qb": qb,
        "qo_max": qo_max,
        "qo": qo,
        "drawdown_total": modelo.pr - modelo.pwf,
        "drawdown_critico": modelo.pr - modelo.pb,
        "ratio_eficiencia": (modelo.pr - modelo.pwf) / modelo.pr,
        "potencial": (qo / qo_max) * 100 if qo_max > 0 else 0
    }
    
    # Cálculo del problema inverso
    if modelo.qo_objetivo is not None:
        if modelo.qo_objetivo <= qb:
            pwf_requerida = modelo.pr - (modelo.qo_objetivo / modelo.j)
        else:
            c = (modelo.j * modelo.pb) / 1.8
            d = ((modelo.qo_objetivo - qb) / c) - 1
            radicando = max(0, 0.04 - 3.2 * d)
            pwf_requerida = modelo.pb * ((-0.2 + math.sqrt(radicando)) / 1.6)
        resultados["pwf_requerida"] = pwf_requerida
        
    return resultados

def calcular_presion_hidrostatica(modelo: ModeloPerforacion) -> dict:
    ph = 0.052 * modelo.mw * modelo.tvd
    return {
        "gradiente_psi_ft": 0.052 * modelo.mw,
        "presion_hidrostatica_psi": ph,
        "diferencial_presion_psi": ph - modelo.pform
    }

def calcular_volumetria_poes(modelo: ModeloReservorioPOES) -> dict:
    hn = modelo.espesor_bruto * modelo.ntg
    poes_stb = (7758 * modelo.area * hn * modelo.porosidad * (1 - modelo.swi)) / modelo.boi
    recuperable_stb = poes_stb * modelo.factor_recobro
    return {
        "espesor_neto_ft": hn,
        "poes_stb": poes_stb,
        "poes_mmstb": poes_stb / 1_000_000,
        "recuperable_stb": recuperable_stb,
        "recuperable_mmstb": recuperable_stb / 1_000_000
    }
