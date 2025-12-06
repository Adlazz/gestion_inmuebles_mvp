import reflex as rx
from typing import Optional, List
from sqlmodel import Field, Relationship

# Aquí agrupamos todas las tablas para evitar errores de importación circular

class Propietario(rx.Model, table=True):
    nombre: str
    apellido: str
    dni: str
    email: str
    inmuebles: List["Inmueble"] = Relationship(back_populates="propietario")

class Inmueble(rx.Model, table=True):
    calle: str
    altura: str
    barrio: str
    localidad: str
    cp: str
    propietario_id: int = Field(foreign_key="propietario.id")
    propietario: Optional[Propietario] = Relationship(back_populates="inmuebles")
    contratos: List["Contrato"] = Relationship(back_populates="inmueble")

class Inquilino(rx.Model, table=True):
    nombre: str
    apellido: str
    dni: str
    email: str
    contratos: List["Contrato"] = Relationship(back_populates="inquilino")

class Contrato(rx.Model, table=True):
    fecha_inicio: str
    fecha_fin: str
    monto: float
    inmueble_id: int = Field(foreign_key="inmueble.id")
    inmueble: Optional[Inmueble] = Relationship(back_populates="contratos")
    inquilino_id: int = Field(foreign_key="inquilino.id")
    inquilino: Optional[Inquilino] = Relationship(back_populates="contratos")
    pagos: List["Pago"] = Relationship(back_populates="contrato")

class Pago(rx.Model, table=True):
    fecha: str
    periodo: str
    monto: float
    contrato_id: int = Field(foreign_key="contrato.id")
    contrato: Optional[Contrato] = Relationship(back_populates="pagos")