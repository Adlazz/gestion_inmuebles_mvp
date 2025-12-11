import reflex as rx
from typing import List, Optional
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