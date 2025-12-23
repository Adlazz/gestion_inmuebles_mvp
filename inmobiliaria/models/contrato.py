import reflex as rx
from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, Relationship

class Contrato(rx.Model, table=True):
    fecha_inicio: str
    fecha_fin: str
    monto: float

    inmueble_id: int = Field(foreign_key="inmueble.id")
    inmueble: Optional["Inmueble"] = Relationship(back_populates="contratos")

    inquilino_id: int = Field(foreign_key="inquilino.id")
    inquilino: Optional["Inquilino"] = Relationship(back_populates="contratos")

    pagos: List["Pago"] = Relationship(back_populates="contrato")

    @property
    def estado(self) -> str:
        """Retorna el estado del contrato: 'Activo', 'Vencido' o 'Futuro'"""
        hoy = datetime.now().date()
        fecha_inicio = datetime.strptime(self.fecha_inicio, "%Y-%m-%d").date()
        fecha_fin = datetime.strptime(self.fecha_fin, "%Y-%m-%d").date()

        if hoy < fecha_inicio:
            return "Futuro"
        elif hoy > fecha_fin:
            return "Vencido"
        else:
            return "Activo"

    @property
    def color_estado(self) -> str:
        """Retorna el color según el estado"""
        estado = self.estado
        if estado == "Activo":
            return "green"
        elif estado == "Vencido":
            return "red"
        else:  # Futuro
            return "blue"