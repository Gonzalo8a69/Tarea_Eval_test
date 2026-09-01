# validaciones.py

def validar_produccion_ipr(pr: float, pb: float, j: float, pwf: float) -> tuple[bool, str]:
    if pr <= 0 or j <= 0:
        return False, "La Presión de Reservorio (Pr) y el Índice de Productividad (J) deben ser mayores a 0."
    if pb < 0 or pwf < 0:
        return False, "Las presiones (Pb, Pwf) no pueden ser negativas."
    if pb >= pr:
        return False, "Para un reservorio subsaturado, Pb debe ser menor a Pr."
    if pwf > pr:
        return False, "Físicamente imposible: Pwf no puede ser mayor que Pr."
    return True, "Válido"

def validar_perforacion_hidrostatica(mw: float, md: float, tvd: float, pform: float) -> tuple[bool, str]:
    if mw <= 0 or md <= 0 or tvd <= 0:
        return False, "El peso del lodo (MW) y las profundidades (MD, TVD) deben ser mayores a 0."
    if pform < 0:
        return False, "La presión de formación no puede ser negativa."
    if tvd > md:
        return False, "Inconsistencia geométrica: TVD no puede ser mayor que MD."
    return True, "Válido"

def validar_reservorios_poes(area: float, h: float, ntg: float, porosidad: float, swi: float, boi: float, fr: float) -> tuple[bool, str]:
    if area <= 0 or h <= 0 or boi <= 0:
        return False, "Área, espesor bruto y Boi deben ser mayores a 0."
    
    fracciones = {"NTG": ntg, "Porosidad": porosidad, "Swi": swi, "Factor de Recobro": fr}
    for nombre, valor in fracciones.items():
        if not (0 <= valor <= 1):
            return False, f"El parámetro {nombre} debe ser una fracción entre 0 y 1."
    return True, "Válido"
