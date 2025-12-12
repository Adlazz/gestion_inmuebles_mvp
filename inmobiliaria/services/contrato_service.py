from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from ..models import Contrato, Pago


class ContratoService:
    """Servicio para operaciones CRUD de Contratos"""

    @staticmethod
    def crear(
        session: Session,
        inmueble_id: int,
        inquilino_id: int,
        fecha_inicio: str,
        fecha_fin: str,
        monto: float
    ) -> Contrato:
        """Crea un nuevo contrato"""
        contrato = Contrato(
            inmueble_id=inmueble_id,
            inquilino_id=inquilino_id,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            monto=monto
        )
        session.add(contrato)
        session.commit()
        session.refresh(contrato)
        return contrato

    @staticmethod
    def obtener_todos(session: Session) -> List[Contrato]:
        """Obtiene todos los contratos con sus relaciones"""
        return session.exec(
            select(Contrato).options(
                selectinload(Contrato.inmueble),
                selectinload(Contrato.inquilino)
            )
        ).all()

    @staticmethod
    def obtener_por_id(session: Session, id: int) -> Optional[Contrato]:
        """Obtiene un contrato por ID con sus relaciones"""
        return session.exec(
            select(Contrato)
            .where(Contrato.id == id)
            .options(
                selectinload(Contrato.inmueble),
                selectinload(Contrato.inquilino)
            )
        ).first()

    @staticmethod
    def actualizar(
        session: Session,
        id: int,
        inmueble_id: int,
        inquilino_id: int,
        fecha_inicio: str,
        fecha_fin: str,
        monto: float
    ) -> Optional[Contrato]:
        """Actualiza un contrato existente"""
        contrato = session.get(Contrato, id)
        if contrato:
            contrato.inmueble_id = inmueble_id
            contrato.inquilino_id = inquilino_id
            contrato.fecha_inicio = fecha_inicio
            contrato.fecha_fin = fecha_fin
            contrato.monto = monto
            session.add(contrato)
            session.commit()
        return contrato

    @staticmethod
    def eliminar(session: Session, id: int) -> bool:
        """Elimina un contrato"""
        contrato = session.get(Contrato, id)
        if contrato:
            session.delete(contrato)
            session.commit()
            return True
        return False

    @staticmethod
    def tiene_pagos(session: Session, id: int) -> tuple[bool, int]:
        """
        Verifica si un contrato tiene pagos asociados.

        Returns:
            tuple[bool, int]: (tiene_pagos, cantidad)
        """
        pagos = session.exec(
            select(Pago).where(Pago.contrato_id == id)
        ).all()
        return len(pagos) > 0, len(pagos)
