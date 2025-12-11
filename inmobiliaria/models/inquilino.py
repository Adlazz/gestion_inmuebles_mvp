import reflex as rx
from typing import List, Optional
from sqlmodel import Relationship

class Inquilino(rx.Model, table=True):
    nombre: str
    apellido: str
    dni: str
    email: str
    
    contratos: List["Contrato"] = Relationship(back_populates="inquilino")