import re
from datetime import datetime


class ValidacionesService:
    """Servicio para validaciones de datos"""

    @staticmethod
    def validar_dni(dni: str) -> tuple[bool, str]:
        """
        Valida formato de DNI (7-8 dígitos).

        Returns:
            tuple[bool, str]: (es_valido, mensaje_error)
        """
        if not dni:
            return False, "El DNI es obligatorio"
        if not re.match(r'^\d{7,8}$', dni):
            return False, "El DNI debe tener 7 u 8 dígitos numéricos"
        return True, ""

    @staticmethod
    def validar_email(email: str) -> tuple[bool, str]:
        """
        Valida formato de email.

        Returns:
            tuple[bool, str]: (es_valido, mensaje_error)
        """
        if not email:
            return False, "El email es obligatorio"
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, email):
            return False, "El formato del email no es válido"
        return True, ""

    @staticmethod
    def validar_monto(monto: str) -> tuple[bool, str]:
        """
        Valida que el monto sea un número positivo.

        Returns:
            tuple[bool, str]: (es_valido, mensaje_error)
        """
        if not monto:
            return False, "El monto es obligatorio"
        try:
            valor = float(monto)
            if valor <= 0:
                return False, "El monto debe ser mayor a 0"
            return True, ""
        except ValueError:
            return False, "El monto debe ser un número válido"

    @staticmethod
    def validar_fechas_contrato(fecha_inicio: str, fecha_fin: str) -> tuple[bool, str]:
        """
        Valida que fecha_fin sea posterior a fecha_inicio.

        Returns:
            tuple[bool, str]: (es_valido, mensaje_error)
        """
        if not fecha_inicio or not fecha_fin:
            return False, "Las fechas de inicio y fin son obligatorias"
        try:
            inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
            if fin <= inicio:
                return False, "La fecha de fin debe ser posterior a la fecha de inicio"
            return True, ""
        except ValueError:
            return False, "Formato de fecha inválido"

    @staticmethod
    def validar_campos_obligatorios(**campos) -> tuple[bool, str]:
        """
        Valida que campos obligatorios no estén vacíos.

        Args:
            **campos: Diccionario con nombre_campo: valor

        Returns:
            tuple[bool, str]: (es_valido, mensaje_error)
        """
        for nombre, valor in campos.items():
            if not valor:
                nombre_legible = nombre.replace("_", " ").capitalize()
                return False, f"{nombre_legible} es obligatorio"
        return True, ""
