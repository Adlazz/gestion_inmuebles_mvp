from sqlmodel import Session, select, func
from sqlalchemy.orm import selectinload
from typing import List, Optional
from ..models import Pago, Contrato


class PagoService:
    """Servicio para operaciones CRUD de Pagos"""

    @staticmethod
    def crear(
        session: Session,
        contrato_id: int,
        periodo: str,
        fecha: str,
        monto: float
    ) -> Pago:
        """Crea un nuevo pago"""
        pago = Pago(
            contrato_id=contrato_id,
            periodo=periodo,
            fecha=fecha,
            monto=monto
        )
        session.add(pago)
        session.commit()
        session.refresh(pago)
        return pago

    @staticmethod
    def obtener_todos(session: Session) -> List[Pago]:
        """Obtiene todos los pagos con sus relaciones"""
        return session.exec(
            select(Pago).options(
                selectinload(Pago.contrato).selectinload(Contrato.inmueble),
                selectinload(Pago.contrato).selectinload(Contrato.inquilino)
            )
        ).all()

    @staticmethod
    def obtener_por_id(session: Session, id: int) -> Optional[Pago]:
        """Obtiene un pago por ID con sus relaciones"""
        return session.exec(
            select(Pago)
            .where(Pago.id == id)
            .options(
                selectinload(Pago.contrato).selectinload(Contrato.inmueble),
                selectinload(Pago.contrato).selectinload(Contrato.inquilino)
            )
        ).first()

    @staticmethod
    def actualizar(
        session: Session,
        id: int,
        contrato_id: int,
        periodo: str,
        fecha: str,
        monto: float
    ) -> Optional[Pago]:
        """Actualiza un pago existente"""
        pago = session.get(Pago, id)
        if pago:
            pago.contrato_id = contrato_id
            pago.periodo = periodo
            pago.fecha = fecha
            pago.monto = monto
            session.add(pago)
            session.commit()
        return pago

    @staticmethod
    def eliminar(session: Session, id: int) -> bool:
        """Elimina un pago"""
        pago = session.get(Pago, id)
        if pago:
            session.delete(pago)
            session.commit()
            return True
        return False

    @staticmethod
    def calcular_total_pagos(session: Session) -> float:
        """Calcula el total histórico de todos los pagos"""
        total = session.exec(select(func.sum(Pago.monto))).one()
        return total if total else 0.0
