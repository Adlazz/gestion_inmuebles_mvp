from sqlmodel import Session, select
from typing import List, Optional
from ..models import Propietario, Inmueble


class PropietarioService:
    """Servicio para operaciones CRUD de Propietarios"""

    @staticmethod
    def crear(
        session: Session,
        nombre: str,
        apellido: str,
        dni: str,
        email: str
    ) -> Propietario:
        """Crea un nuevo propietario"""
        propietario = Propietario(
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            email=email
        )
        session.add(propietario)
        session.commit()
        session.refresh(propietario)
        return propietario

    @staticmethod
    def obtener_todos(session: Session) -> List[Propietario]:
        """Obtiene todos los propietarios"""
        return session.exec(select(Propietario)).all()

    @staticmethod
    def obtener_por_id(session: Session, id: int) -> Optional[Propietario]:
        """Obtiene un propietario por ID"""
        return session.get(Propietario, id)

    @staticmethod
    def actualizar(
        session: Session,
        id: int,
        nombre: str,
        apellido: str,
        dni: str,
        email: str
    ) -> Optional[Propietario]:
        """Actualiza un propietario existente"""
        propietario = session.get(Propietario, id)
        if propietario:
            propietario.nombre = nombre
            propietario.apellido = apellido
            propietario.dni = dni
            propietario.email = email
            session.add(propietario)
            session.commit()
        return propietario

    @staticmethod
    def eliminar(session: Session, id: int) -> bool:
        """Elimina un propietario"""
        propietario = session.get(Propietario, id)
        if propietario:
            session.delete(propietario)
            session.commit()
            return True
        return False

    @staticmethod
    def buscar_por_dni(
        session: Session,
        dni: str,
        excluir_id: Optional[int] = None
    ) -> Optional[Propietario]:
        """Busca un propietario por DNI"""
        query = select(Propietario).where(Propietario.dni == dni)
        if excluir_id:
            query = query.where(Propietario.id != excluir_id)
        return session.exec(query).first()

    @staticmethod
    def buscar_por_email(
        session: Session,
        email: str,
        excluir_id: Optional[int] = None
    ) -> Optional[Propietario]:
        """Busca un propietario por email"""
        query = select(Propietario).where(Propietario.email == email)
        if excluir_id:
            query = query.where(Propietario.id != excluir_id)
        return session.exec(query).first()

    @staticmethod
    def tiene_inmuebles(session: Session, id: int) -> tuple[bool, int]:
        """
        Verifica si un propietario tiene inmuebles asociados.

        Returns:
            tuple[bool, int]: (tiene_inmuebles, cantidad)
        """
        inmuebles = session.exec(
            select(Inmueble).where(Inmueble.propietario_id == id)
        ).all()
        return len(inmuebles) > 0, len(inmuebles)
