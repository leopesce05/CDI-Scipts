def get_quality_rating(percentage, is_inverse=False):
    """
    Determina la calificación de calidad basada en el porcentaje y el tipo de métrica.
    
    Args:
        percentage (float): El porcentaje a evaluar (0-100)
        is_inverse (bool): True si la métrica es inversa (bajo % = bueno), False si es directa (alto % = bueno)
    
    Returns:
        str: La calificación de calidad ('Mala', 'Buena', 'Muy buena', 'Excelente')
    """
    if is_inverse:
        # Para métricas inversas (bajo % = bueno)
        if percentage <= 9:
            return 'Excelente'
        elif percentage <= 40:
            return 'Muy buena'
        elif percentage <= 70:
            return 'Buena'
        else:
            return 'Mala'
    else:
        # Para métricas directas (alto % = bueno)
        if percentage <= 30:
            return 'Mala'
        elif percentage <= 60:
            return 'Buena'
        elif percentage <= 90:
            return 'Muy buena'
        else:
            return 'Excelente'

# Diccionario de métricas y su tipo (inverso o directo)
METRIC_TYPES = {
    'ExactSint-ReglaCorrecta-ISBN_ap': False,  # Directa
    'IntDominio-OutBounds-Gen-ContarNum_ap': False,  # Directa
    'Precision-Fechas_ap': False,  # Directa
    'Densidad-Grado-Contar_ap': True,  # Inversa
    'NoDuplicacion-CantDups-Contar_ap': True,  # Inversa
    'IntInterRel-Pertenencia_ap': True,  # Inversa
} 