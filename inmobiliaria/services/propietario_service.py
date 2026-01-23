from sqlmodel import Session, select
from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from ..models import Propietario, Inmueble, Pago


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
        try:
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
        except SQLAlchemyError as e:
            session.rollback()
            raise Exception(f"Error al crear propietario en la base de datos: {str(e)}")

    @staticmethod
    def obtener_todos(session: Session) -> List[Propietario]:
        """Obtiene todos los propietarios"""
        return session.exec(select(Propietario)).all()

    @staticmethod
    def obtener_por_id(session: Session, id: int) -> Optional[Propietario]:
        """Obtiene un propietario por ID"""
        return session.get(Propietario, id)

    @staticmethod
    def obtener_por_id_con_relaciones(session: Session, id: int) -> Optional[Propietario]:
        """Obtiene un propietario por ID con sus inmuebles cargados"""
        from sqlalchemy.orm import selectinload
        return session.exec(
            select(Propietario)
            .where(Propietario.id == id)
            .options(selectinload(Propietario.inmuebles))
        ).first()

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
        try:
            propietario = session.get(Propietario, id)
            if propietario:
                propietario.nombre = nombre
                propietario.apellido = apellido
                propietario.dni = dni
                propietario.email = email
                session.add(propietario)
                session.commit()
                session.refresh(propietario)
            return propietario
        except SQLAlchemyError as e:
            session.rollback()
            raise Exception(f"Error al actualizar propietario en la base de datos: {str(e)}")

    @staticmethod
    def eliminar(session: Session, id: int) -> bool:
        """Elimina un propietario"""
        try:
            propietario = session.get(Propietario, id)
            if propietario:
                session.delete(propietario)
                session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            raise Exception(f"Error al eliminar propietario en la base de datos: {str(e)}")

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

    @staticmethod
    def tiene_inmuebles_con_contratos_activos(session: Session, id: int) -> tuple[bool, int, list]:
        """
        Verifica si un propietario tiene inmuebles con contratos activos.

        Returns:
            tuple[bool, int, list]: (tiene_contratos_activos, cantidad_total_contratos, inmuebles_con_contratos)
        """
        from ..models import Contrato
        from datetime import datetime
        from sqlalchemy.orm import selectinload

        inmuebles = session.exec(
            select(Inmueble)
            .where(Inmueble.propietario_id == id)
            .options(selectinload(Inmueble.contratos))
        ).all()

        contratos_activos = 0
        inmuebles_con_contratos = []
        hoy = datetime.now().date().isoformat()

        for inmueble in inmuebles:
            for contrato in inmueble.contratos:
                # Verificar si el contrato está activo
                if contrato.fecha_inicio <= hoy <= contrato.fecha_fin:
                    contratos_activos += 1
                    if inmueble not in inmuebles_con_contratos:
                        inmuebles_con_contratos.append(inmueble)

        return contratos_activos > 0, contratos_activos, inmuebles_con_contratos

    @staticmethod
    def obtener_estadisticas(session: Session, id: int) -> dict:
        """
        Obtiene las estadísticas completas de un propietario.

        Returns:
            dict: {
                'total_inmuebles': int,
                'inmuebles_alquilados': int,
                'inmuebles_disponibles': int,
                'ingresos_totales': float,
                'ingresos_mes_actual': float,
                'promedio_mensual': float,
                'contratos_activos': int,
                'contratos_proximos_vencer': int
            }
        """
        from ..models import Contrato, Pago
        from datetime import datetime, timedelta
        from sqlalchemy.orm import selectinload
        from sqlmodel import func

        # Obtener todos los inmuebles del propietario con sus contratos
        inmuebles = session.exec(
            select(Inmueble)
            .where(Inmueble.propietario_id == id)
            .options(selectinload(Inmueble.contratos))
        ).all()

        total_inmuebles = len(inmuebles)
        hoy = datetime.now().date()
        hoy_str = hoy.isoformat()

        # Contar inmuebles alquilados y disponibles
        inmuebles_alquilados = 0
        contratos_activos = 0
        contratos_proximos_vencer = 0
        contratos_ids = []

        for inmueble in inmuebles:
            tiene_contrato_activo = False
            for contrato in inmueble.contratos:
                if contrato.fecha_inicio <= hoy_str <= contrato.fecha_fin:
                    tiene_contrato_activo = True
                    contratos_activos += 1
                    contratos_ids.append(contrato.id)

                    # Verificar si está próximo a vencer (30 días)
                    fecha_fin = datetime.fromisoformat(contrato.fecha_fin).date()
                    dias_restantes = (fecha_fin - hoy).days
                    if 0 < dias_restantes <= 30:
                        contratos_proximos_vencer += 1
                    break

            if tiene_contrato_activo:
                inmuebles_alquilados += 1

        inmuebles_disponibles = total_inmuebles - inmuebles_alquilados

        # Calcular ingresos totales de todos los contratos del propietario
        if contratos_ids:
            ingresos_totales = session.exec(
                select(func.sum(Pago.monto))
                .where(Pago.contrato_id.in_(contratos_ids))
            ).one() or 0.0

            # Calcular ingresos del mes actual
            primer_dia_mes = hoy.replace(day=1).isoformat()
            ingresos_mes_actual = session.exec(
                select(func.sum(Pago.monto))
                .where(Pago.contrato_id.in_(contratos_ids))
                .where(Pago.fecha >= primer_dia_mes)
            ).one() or 0.0

            # Obtener fecha del primer pago para calcular promedio
            primer_pago = session.exec(
                select(Pago.fecha)
                .where(Pago.contrato_id.in_(contratos_ids))
                .order_by(Pago.fecha)
            ).first()

            if primer_pago and ingresos_totales > 0:
                fecha_primer_pago = datetime.fromisoformat(primer_pago).date()
                meses_transcurridos = max(1, ((hoy - fecha_primer_pago).days / 30))
                promedio_mensual = ingresos_totales / meses_transcurridos
            else:
                promedio_mensual = 0.0
        else:
            ingresos_totales = 0.0
            ingresos_mes_actual = 0.0
            promedio_mensual = 0.0

        return {
            'total_inmuebles': total_inmuebles,
            'inmuebles_alquilados': inmuebles_alquilados,
            'inmuebles_disponibles': inmuebles_disponibles,
            'ingresos_totales': ingresos_totales,
            'ingresos_mes_actual': ingresos_mes_actual,
            'promedio_mensual': promedio_mensual,
            'contratos_activos': contratos_activos,
            'contratos_proximos_vencer': contratos_proximos_vencer
        }

    @staticmethod
    def obtener_inmuebles_con_detalles(session: Session, id: int) -> List[dict]:
        """
        Obtiene todos los inmuebles del propietario con información de estado.

        Returns:
            List[dict]: Lista de inmuebles con {inmueble, estado, contrato_activo, inquilino}
        """
        from ..models import Contrato
        from datetime import datetime
        from sqlalchemy.orm import selectinload

        inmuebles = session.exec(
            select(Inmueble)
            .where(Inmueble.propietario_id == id)
            .options(
                selectinload(Inmueble.contratos).selectinload(Contrato.inquilino)
            )
        ).all()

        hoy = datetime.now().date().isoformat()
        resultado = []

        for inmueble in inmuebles:
            contrato_activo = None
            inquilino_actual = None

            for contrato in inmueble.contratos:
                if contrato.fecha_inicio <= hoy <= contrato.fecha_fin:
                    contrato_activo = contrato
                    inquilino_actual = contrato.inquilino
                    break

            resultado.append({
                'inmueble': inmueble,
                'estado': 'Alquilado' if contrato_activo else 'Disponible',
                'contrato_activo': contrato_activo,
                'inquilino': inquilino_actual
            })

        return resultado

    @staticmethod
    def obtener_pagos_recibidos(session: Session, id: int) -> List[Pago]:
        """
        Obtiene todos los pagos recibidos de los contratos del propietario.

        Returns:
            List[Pago]: Lista de pagos ordenados por fecha descendente
        """
        from ..models import Contrato, Pago
        from sqlalchemy.orm import selectinload

        # Obtener IDs de contratos del propietario
        contratos = session.exec(
            select(Contrato)
            .join(Inmueble)
            .where(Inmueble.propietario_id == id)
        ).all()

        contratos_ids = [c.id for c in contratos]

        if not contratos_ids:
            return []

        # Obtener todos los pagos de esos contratos
        pagos = session.exec(
            select(Pago)
            .where(Pago.contrato_id.in_(contratos_ids))
            .options(
                selectinload(Pago.contrato).selectinload(Contrato.inmueble),
                selectinload(Pago.contrato).selectinload(Contrato.inquilino)
            )
            .order_by(Pago.fecha.desc())
        ).all()

        return pagos
