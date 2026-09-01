# modelos.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class ModeloProduccionIPR:
    pr: float
    pb: float
    j: float
    pwf: float
    qo_objetivo: Optional[float] = None 

@dataclass
class ModeloPerforacion:
    mw: float
    md: float
    tvd: float
    pform: float

@dataclass
class ModeloReservorioPOES:
    area: float
    espesor_bruto: float
    ntg: float
    porosidad: float
    swi: float
    boi: float
    factor_recobro: float