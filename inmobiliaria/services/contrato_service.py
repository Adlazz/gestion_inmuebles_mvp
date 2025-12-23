from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import datetime
from ..models import Contrato, Pago


def obtener_estado_contrato(fecha_inicio: str, fecha_fin: str) -> str:
    """Retorna el estado del contrato basado en las fechas"""
    hoy = datetime.now().date().isoformat()

    if hoy < fecha_inicio:
        return "Futuro"
    elif hoy > fecha_fin:
        return "Vencido"
    else:
        return "Activo"


def obtener_color_estado(estado: str) -> str:
    """Retorna el color según el estado"""
    if estado == "Activo":
        return "green"
    elif estado == "Vencido":
        return "red"
    else:  # Futuro
        return "blue"


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

    @staticmethod
    def inmueble_tiene_contrato_activo(
        session: Session,
        inmueble_id: int,
        fecha_inicio: str,
        fecha_fin: str,
        excluir_contrato_id: Optional[int] = None
    ) -> tuple[bool, Optional[Contrato]]:
        """
        Verifica si un inmueble tiene un contrato activo que se solape con las fechas dadas.

        Args:
            session: Sesión de base de datos
            inmueble_id: ID del inmueble a verificar
            fecha_inicio: Fecha de inicio del nuevo contrato (formato YYYY-MM-DD)
            fecha_fin: Fecha de fin del nuevo contrato (formato YYYY-MM-DD)
            excluir_contrato_id: ID de contrato a excluir (para ediciones)

        Returns:
            tuple[bool, Optional[Contrato]]: (tiene_contrato_activo, contrato_conflictivo)
        """
        # Obtener todos los contratos del inmueble con sus relaciones
        query = select(Contrato).where(Contrato.inmueble_id == inmueble_id).options(
            selectinload(Contrato.inmueble),
            selectinload(Contrato.inquilino)
        )

        # Excluir el contrato actual si estamos editando
        if excluir_contrato_id:
            query = query.where(Contrato.id != excluir_contrato_id)

        contratos = session.exec(query).all()

        # Verificar si hay solapamiento de fechas
        for contrato in contratos:
            # Verificar si las fechas se solapan
            # Solapamiento: nuevo_inicio <= contrato_fin AND nuevo_fin >= contrato_inicio
            if fecha_inicio <= contrato.fecha_fin and fecha_fin >= contrato.fecha_inicio:
                return True, contrato

        return False, None
