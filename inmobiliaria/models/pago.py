import reflex as rx
from typing import Optional
from sqlmodel import Field, Relationship

class Pago(rx.Model, table=True):
    fecha: str
    periodo: str
    monto: float
    
    contrato_id: int = Field(foreign_key="contrato.id")
    contrato: Optional["Contrato"] = Relationship(back_populates="pagos")