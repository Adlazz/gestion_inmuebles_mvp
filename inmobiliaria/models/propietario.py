import reflex as rx
from typing import List, Optional
from sqlmodel import Relationship

class Propietario(rx.Model, table=True):
    nombre: str
    apellido: str
    dni: str
    email: str

    # Nota las comillas en "Inmueble" para evitar el error circular
    inmuebles: List["Inmueble"] = Relationship(back_populates="propietario")