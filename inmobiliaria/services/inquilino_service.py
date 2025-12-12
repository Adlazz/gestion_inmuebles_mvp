from sqlmodel import Session, select
from typing import List, Optional
from ..models import Inquilino, Contrato


class InquilinoService:
    """Servicio para operaciones CRUD de Inquilinos"""

    @staticmethod
    def crear(
        session: Session,
        nombre: str,
        apellido: str,
        dni: str,
        email: str
    ) -> Inquilino:
        """Crea un nuevo inquilino"""
        inquilino = Inquilino(
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            email=email
        )
        session.add(inquilino)
        session.commit()
        session.refresh(inquilino)
        return inquilino

    @staticmethod
    def obtener_todos(session: Session) -> List[Inquilino]:
        """Obtiene todos los inquilinos"""
        return session.exec(select(Inquilino)).all()

    @staticmethod
    def obtener_por_id(session: Session, id: int) -> Optional[Inquilino]:
        """Obtiene un inquilino por ID"""
        return session.get(Inquilino, id)

    @staticmethod
    def actualizar(
        session: Session,
        id: int,
        nombre: str,
        apellido: str,
        dni: str,
        email: str
    ) -> Optional[Inquilino]:
        """Actualiza un inquilino existente"""
        inquilino = session.get(Inquilino, id)
        if inquilino:
            inquilino.nombre = nombre
            inquilino.apellido = apellido
            inquilino.dni = dni
            inquilino.email = email
            session.add(inquilino)
            session.commit()
        return inquilino

    @staticmethod
    def eliminar(session: Session, id: int) -> bool:
        """Elimina un inquilino"""
        inquilino = session.get(Inquilino, id)
        if inquilino:
            session.delete(inquilino)
            session.commit()
            return True
        return False

    @staticmethod
    def buscar_por_dni(
        session: Session,
        dni: str,
        excluir_id: Optional[int] = None
    ) -> Optional[Inquilino]:
        """Busca un inquilino por DNI"""
        query = select(Inquilino).where(Inquilino.dni == dni)
        if excluir_id:
            query = query.where(Inquilino.id != excluir_id)
        return session.exec(query).first()

    @staticmethod
    def buscar_por_email(
        session: Session,
        email: str,
        excluir_id: Optional[int] = None
    ) -> Optional[Inquilino]:
        """Busca un inquilino por email"""
        query = select(Inquilino).where(Inquilino.email == email)
        if excluir_id:
            query = query.where(Inquilino.id != excluir_id)
        return session.exec(query).first()

    @staticmethod
    def tiene_contratos(session: Session, id: int) -> tuple[bool, int]:
        """
        Verifica si un inquilino tiene contratos asociados.

        Returns:
            tuple[bool, int]: (tiene_contratos, cantidad)
        """
        contratos = session.exec(
            select(Contrato).where(Contrato.inquilino_id == id)
        ).all()
        return len(contratos) > 0, len(contratos)
