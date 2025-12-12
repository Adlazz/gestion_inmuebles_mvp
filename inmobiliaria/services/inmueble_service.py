from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from ..models import Inmueble, Contrato


class InmuebleService:
    """Servicio para operaciones CRUD de Inmuebles"""

    @staticmethod
    def crear(
        session: Session,
        calle: str,
        altura: str,
        barrio: str,
        localidad: str,
        cp: str,
        propietario_id: int
    ) -> Inmueble:
        """Crea un nuevo inmueble"""
        inmueble = Inmueble(
            calle=calle,
            altura=altura,
            barrio=barrio,
            localidad=localidad,
            cp=cp,
            propietario_id=propietario_id
        )
        session.add(inmueble)
        session.commit()
        session.refresh(inmueble)
        return inmueble

    @staticmethod
    def obtener_todos(session: Session) -> List[Inmueble]:
        """Obtiene todos los inmuebles con sus propietarios"""
        return session.exec(
            select(Inmueble).options(selectinload(Inmueble.propietario))
        ).all()

    @staticmethod
    def obtener_por_id(session: Session, id: int) -> Optional[Inmueble]:
        """Obtiene un inmueble por ID con su propietario"""
        return session.exec(
            select(Inmueble)
            .where(Inmueble.id == id)
            .options(selectinload(Inmueble.propietario))
        ).first()

    @staticmethod
    def actualizar(
        session: Session,
        id: int,
        calle: str,
        altura: str,
        barrio: str,
        localidad: str,
        cp: str,
        propietario_id: int
    ) -> Optional[Inmueble]:
        """Actualiza un inmueble existente"""
        inmueble = session.get(Inmueble, id)
        if inmueble:
            inmueble.calle = calle
            inmueble.altura = altura
            inmueble.barrio = barrio
            inmueble.localidad = localidad
            inmueble.cp = cp
            inmueble.propietario_id = propietario_id
            session.add(inmueble)
            session.commit()
        return inmueble

    @staticmethod
    def eliminar(session: Session, id: int) -> bool:
        """Elimina un inmueble"""
        inmueble = session.get(Inmueble, id)
        if inmueble:
            session.delete(inmueble)
            session.commit()
            return True
        return False

    @staticmethod
    def tiene_contratos(session: Session, id: int) -> tuple[bool, int]:
        """
        Verifica si un inmueble tiene contratos asociados.

        Returns:
            tuple[bool, int]: (tiene_contratos, cantidad)
        """
        contratos = session.exec(
            select(Contrato).where(Contrato.inmueble_id == id)
        ).all()
        return len(contratos) > 0, len(contratos)
