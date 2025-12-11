import reflex as rx
from typing import List, Optional
from sqlmodel import Field, Relationship

class Inmueble(rx.Model, table=True):
    calle: str
    altura: str
    barrio: str
    localidad: str
    cp: str
    
    # Clave foránea (se refiere a la tabla de base de datos 'propietario')
    propietario_id: int = Field(foreign_key="propietario.id")
    
    # Relación (se refiere a la clase Python "Propietario")
    propietario: Optional["Propietario"] = Relationship(back_populates="inmuebles")
    
    contratos: List["Contrato"] = Relationship(back_populates="inmueble")