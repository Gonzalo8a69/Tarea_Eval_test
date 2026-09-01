# validaciones.py

def validar_produccion_ipr(pr: float, pb: float, j: float, pwf: float) -> tuple[bool, str]:
    if any(val < 0 for val in [pr, pb, j, pwf]):
        return False, "Los parámetros de producción no pueden ser negativos."
    if pb >= pr:
        return False, "Para un reservorio subsaturado, la presión de burbuja (Pb) debe ser menor a la del reservorio (Pr)."
    if pwf > pr:
        return False, "Inconsistencia: La presión de fondo (Pwf) no puede ser mayor que la presión del reservorio (Pr)."
    return True, "Válido"

def validar_perforacion_hidrostatica(mw: float, md: float, tvd: float, pform: float) -> tuple[bool, str]:
    if mw <= 0 or md <= 0 or tvd <= 0:
        return False, "El peso del lodo y las profundidades deben ser mayores a cero."
    if pform < 0:
        return False, "La presión de formación no puede ser negativa."
    if tvd > md:
        return False, "Inconsistencia geométrica: TVD no puede ser mayor que MD."
    return True, "Válido"

def validar_reservorios_poes(area: float, h: float, ntg: float, porosidad: float, swi: float, boi: float, fr: float) -> tuple[bool, str]:
    if area <= 0 or h <= 0 or boi <= 0:
        return False, "Área, espesor bruto y Boi deben ser mayores a cero."
    
    fracciones = {"NTG": ntg, "Porosidad": porosidad, "Swi": swi, "Factor de Recobro": fr}
    for nombre, valor in fracciones.items():
        if not (0 <= valor <= 1):
            return False, f"El parámetro {nombre} debe ingresarse como fracción (entre 0 y 1)."
    return True, "Válido"
    
    fracciones = {"NTG": ntg, "Porosidad": porosidad, "Swi": swi, "Factor de Recobro": fr}
    for nombre, valor in fracciones.items():
        if not (0 <= valor <= 1):
            return False, f"El parámetro {nombre} debe ingresarse como fracción (entre 0 y 1)."
    return True, "Válido"
