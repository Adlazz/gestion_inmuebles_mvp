import reflex as rx
from typing import List
from sqlmodel import select, func
from sqlalchemy.orm import selectinload
from .models import Propietario, Inmueble, Inquilino, Contrato, Pago


class State(rx.State):
    # Configuración para desactivar setters automáticos
    state_auto_setters = False

    # --- VARIABLES PROPIETARIO ---
    form_prop_nombre: str = ""
    form_prop_apellido: str = ""
    form_prop_dni: str = ""
    form_prop_email: str = ""
    lista_propietarios: List[Propietario] = []

    # --- VARIABLES INMUEBLE ---
    inm_calle: str = ""
    inm_altura: str = ""
    inm_barrio: str = ""
    inm_localidad: str = ""
    inm_cp: str = ""
    inm_propietario_select: str = ""
    lista_inmuebles: List[Inmueble] = []

    # --- VARIABLES INQUILINO ---
    form_inq_nombre: str = ""
    form_inq_apellido: str = ""
    form_inq_dni: str = ""
    form_inq_email: str = ""
    lista_inquilinos: List[Inquilino] = []

    # --- VARIABLES CONTRATO ---
    con_inmueble_select: str = ""
    con_inquilino_select: str = ""
    con_fecha_inicio: str = ""
    con_fecha_fin: str = ""
    con_monto: str = ""
    lista_contratos: List[Contrato] = []

    # --- VARIABLES PAGO ---
    pago_contrato_select: str = ""
    pago_periodo: str = ""
    pago_fecha: str = ""
    pago_monto: str = ""
    lista_pagos: List[Pago] = []

    # --- VARIABLES DEL DASHBOARD ---
    stat_propietarios: int = 0
    stat_inmuebles: int = 0
    stat_contratos_activos: int = 0
    stat_total_pagos: float = 0.0

    # --- SETTERS EXPLÍCITOS ---
    def set_form_prop_nombre(self, value: str):
        self.form_prop_nombre = value

    def set_form_prop_apellido(self, value: str):
        self.form_prop_apellido = value

    def set_form_prop_dni(self, value: str):
        self.form_prop_dni = value

    def set_form_prop_email(self, value: str):
        self.form_prop_email = value

    def set_inm_propietario_select(self, value: str):
        self.inm_propietario_select = value

    def set_inm_calle(self, value: str):
        self.inm_calle = value

    def set_inm_altura(self, value: str):
        self.inm_altura = value

    def set_inm_barrio(self, value: str):
        self.inm_barrio = value

    def set_inm_localidad(self, value: str):
        self.inm_localidad = value

    def set_inm_cp(self, value: str):
        self.inm_cp = value

    def set_form_inq_nombre(self, value: str):
        self.form_inq_nombre = value

    def set_form_inq_apellido(self, value: str):
        self.form_inq_apellido = value

    def set_form_inq_dni(self, value: str):
        self.form_inq_dni = value

    def set_form_inq_email(self, value: str):
        self.form_inq_email = value

    def set_con_inmueble_select(self, value: str):
        self.con_inmueble_select = value

    def set_con_inquilino_select(self, value: str):
        self.con_inquilino_select = value

    def set_con_fecha_inicio(self, value: str):
        self.con_fecha_inicio = value

    def set_con_fecha_fin(self, value: str):
        self.con_fecha_fin = value

    def set_con_monto(self, value: str):
        self.con_monto = value

    def set_pago_contrato_select(self, value: str):
        self.pago_contrato_select = value

    def set_pago_periodo(self, value: str):
        self.pago_periodo = value

    def set_pago_monto(self, value: str):
        self.pago_monto = value

    def set_pago_fecha(self, value: str):
        self.pago_fecha = value

    # --- CARGA GENERAL ---
    def cargar_datos(self):
        with rx.session() as session:
            # Cargas de listas
            self.lista_propietarios = session.exec(select(Propietario)).all()
            self.lista_inmuebles = session.exec(select(Inmueble).options(selectinload(Inmueble.propietario))).all()
            self.lista_inquilinos = session.exec(select(Inquilino)).all()
            self.lista_contratos = session.exec(select(Contrato).options(selectinload(Contrato.inmueble), selectinload(Contrato.inquilino))).all()
            self.lista_pagos = session.exec(select(Pago).options(selectinload(Pago.contrato).selectinload(Contrato.inmueble), selectinload(Pago.contrato).selectinload(Contrato.inquilino))).all()

            # Cálculos para el dashboard
            self.stat_propietarios = session.exec(select(func.count(Propietario.id))).one()
            self.stat_inmuebles = session.exec(select(func.count(Inmueble.id))).one()
            self.stat_contratos_activos = session.exec(select(func.count(Contrato.id))).one()

            total = session.exec(select(func.sum(Pago.monto))).one()
            self.stat_total_pagos = total if total else 0.0

    # --- GUARDAR ENTIDADES ---
    def guardar_propietario(self):
        with rx.session() as session:
            nuevo = Propietario(
                nombre=self.form_prop_nombre,
                apellido=self.form_prop_apellido,
                dni=self.form_prop_dni,
                email=self.form_prop_email
            )
            session.add(nuevo)
            session.commit()
            session.refresh(nuevo)
        self.cargar_datos()
        self.form_prop_nombre = ""
        self.form_prop_apellido = ""
        self.form_prop_dni = ""
        self.form_prop_email = ""

    @rx.var
    def opciones_propietarios(self) -> List[str]:
        return [f"{p.id} - {p.nombre} {p.apellido}" for p in self.lista_propietarios]

    def guardar_inmueble(self):
        if not self.inm_propietario_select:
            return
        id_dueno = int(self.inm_propietario_select.split(" - ")[0])
        with rx.session() as session:
            nuevo = Inmueble(
                calle=self.inm_calle,
                altura=self.inm_altura,
                barrio=self.inm_barrio,
                localidad=self.inm_localidad,
                cp=self.inm_cp,
                propietario_id=id_dueno
            )
            session.add(nuevo)
            session.commit()
            session.refresh(nuevo)
        self.cargar_datos()
        self.inm_calle = ""
        self.inm_altura = ""
        self.inm_barrio = ""

    def guardar_inquilino(self):
        with rx.session() as session:
            nuevo = Inquilino(
                nombre=self.form_inq_nombre,
                apellido=self.form_inq_apellido,
                dni=self.form_inq_dni,
                email=self.form_inq_email
            )
            session.add(nuevo)
            session.commit()
            session.refresh(nuevo)
        self.cargar_datos()
        self.form_inq_nombre = ""
        self.form_inq_apellido = ""
        self.form_inq_dni = ""
        self.form_inq_email = ""

    @rx.var
    def opciones_inmuebles_select(self) -> List[str]:
        return [f"{i.id} - {i.calle} {i.altura} ({i.barrio})" for i in self.lista_inmuebles]

    @rx.var
    def opciones_inquilinos_select(self) -> List[str]:
        return [f"{i.id} - {i.nombre} {i.apellido}" for i in self.lista_inquilinos]

    def guardar_contrato(self):
        if not self.con_inmueble_select or not self.con_inquilino_select:
            return
        id_inm = int(self.con_inmueble_select.split(" - ")[0])
        id_inq = int(self.con_inquilino_select.split(" - ")[0])
        with rx.session() as session:
            nuevo = Contrato(
                inmueble_id=id_inm,
                inquilino_id=id_inq,
                fecha_inicio=self.con_fecha_inicio,
                fecha_fin=self.con_fecha_fin,
                monto=float(self.con_monto) if self.con_monto else 0.0
            )
            session.add(nuevo)
            session.commit()
            session.refresh(nuevo)
        self.cargar_datos()
        self.con_monto = ""

    @rx.var
    def opciones_contratos_select(self) -> List[str]:
        """Muestra una lista legible de contratos para cobrar"""
        return [f"{c.id} - {c.inmueble.calle} (Inq: {c.inquilino.apellido})" for c in self.lista_contratos]

    def guardar_pago(self):
        if not self.pago_contrato_select:
            return
        id_con = int(self.pago_contrato_select.split(" - ")[0])

        with rx.session() as session:
            nuevo = Pago(
                contrato_id=id_con,
                periodo=self.pago_periodo,
                fecha=self.pago_fecha,
                monto=float(self.pago_monto) if self.pago_monto else 0.0
            )
            session.add(nuevo)
            session.commit()
            session.refresh(nuevo)
        self.cargar_datos()
        self.pago_periodo = ""
        self.pago_monto = ""
