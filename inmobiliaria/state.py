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

    # --- VARIABLES PARA EDICIÓN ---
    editando_propietario_id: int | None = None
    editando_inmueble_id: int | None = None
    editando_inquilino_id: int | None = None
    editando_contrato_id: int | None = None
    editando_pago_id: int | None = None

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
            if self.editando_propietario_id:
                # Editar propietario existente
                prop = session.get(Propietario, self.editando_propietario_id)
                if prop:
                    prop.nombre = self.form_prop_nombre
                    prop.apellido = self.form_prop_apellido
                    prop.dni = self.form_prop_dni
                    prop.email = self.form_prop_email
                    session.add(prop)
                    session.commit()
                self.editando_propietario_id = None
            else:
                # Crear nuevo propietario
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

    def editar_propietario(self, prop_id: int):
        with rx.session() as session:
            prop = session.get(Propietario, prop_id)
            if prop:
                self.form_prop_nombre = prop.nombre
                self.form_prop_apellido = prop.apellido
                self.form_prop_dni = prop.dni
                self.form_prop_email = prop.email
                self.editando_propietario_id = prop_id

    def eliminar_propietario(self, prop_id: int):
        with rx.session() as session:
            prop = session.get(Propietario, prop_id)
            if prop:
                session.delete(prop)
                session.commit()
        self.cargar_datos()

    @rx.var
    def opciones_propietarios(self) -> List[str]:
        return [f"{p.id} - {p.nombre} {p.apellido}" for p in self.lista_propietarios]

    def guardar_inmueble(self):
        if not self.inm_propietario_select:
            return
        id_dueno = int(self.inm_propietario_select.split(" - ")[0])
        with rx.session() as session:
            if self.editando_inmueble_id:
                # Editar inmueble existente
                inm = session.get(Inmueble, self.editando_inmueble_id)
                if inm:
                    inm.calle = self.inm_calle
                    inm.altura = self.inm_altura
                    inm.barrio = self.inm_barrio
                    inm.localidad = self.inm_localidad
                    inm.cp = self.inm_cp
                    inm.propietario_id = id_dueno
                    session.add(inm)
                    session.commit()
                self.editando_inmueble_id = None
            else:
                # Crear nuevo inmueble
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
        self.inm_localidad = ""
        self.inm_cp = ""

    def editar_inmueble(self, inm_id: int):
        with rx.session() as session:
            inm = session.get(Inmueble, inm_id)
            if inm:
                self.inm_calle = inm.calle
                self.inm_altura = inm.altura
                self.inm_barrio = inm.barrio
                self.inm_localidad = inm.localidad
                self.inm_cp = inm.cp
                self.inm_propietario_select = f"{inm.propietario_id} - {inm.propietario.nombre} {inm.propietario.apellido}"
                self.editando_inmueble_id = inm_id

    def eliminar_inmueble(self, inm_id: int):
        with rx.session() as session:
            inm = session.get(Inmueble, inm_id)
            if inm:
                session.delete(inm)
                session.commit()
        self.cargar_datos()

    def guardar_inquilino(self):
        with rx.session() as session:
            if self.editando_inquilino_id:
                # Editar inquilino existente
                inq = session.get(Inquilino, self.editando_inquilino_id)
                if inq:
                    inq.nombre = self.form_inq_nombre
                    inq.apellido = self.form_inq_apellido
                    inq.dni = self.form_inq_dni
                    inq.email = self.form_inq_email
                    session.add(inq)
                    session.commit()
                self.editando_inquilino_id = None
            else:
                # Crear nuevo inquilino
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

    def editar_inquilino(self, inq_id: int):
        with rx.session() as session:
            inq = session.get(Inquilino, inq_id)
            if inq:
                self.form_inq_nombre = inq.nombre
                self.form_inq_apellido = inq.apellido
                self.form_inq_dni = inq.dni
                self.form_inq_email = inq.email
                self.editando_inquilino_id = inq_id

    def eliminar_inquilino(self, inq_id: int):
        with rx.session() as session:
            inq = session.get(Inquilino, inq_id)
            if inq:
                session.delete(inq)
                session.commit()
        self.cargar_datos()

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
            if self.editando_contrato_id:
                # Editar contrato existente
                con = session.get(Contrato, self.editando_contrato_id)
                if con:
                    con.inmueble_id = id_inm
                    con.inquilino_id = id_inq
                    con.fecha_inicio = self.con_fecha_inicio
                    con.fecha_fin = self.con_fecha_fin
                    con.monto = float(self.con_monto) if self.con_monto else 0.0
                    session.add(con)
                    session.commit()
                self.editando_contrato_id = None
            else:
                # Crear nuevo contrato
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
        self.con_fecha_inicio = ""
        self.con_fecha_fin = ""
        self.con_monto = ""

    def editar_contrato(self, con_id: int):
        with rx.session() as session:
            con = session.exec(
                select(Contrato)
                .where(Contrato.id == con_id)
                .options(selectinload(Contrato.inmueble), selectinload(Contrato.inquilino))
            ).first()
            if con:
                self.con_inmueble_select = f"{con.inmueble_id} - {con.inmueble.calle} {con.inmueble.altura} ({con.inmueble.barrio})"
                self.con_inquilino_select = f"{con.inquilino_id} - {con.inquilino.nombre} {con.inquilino.apellido}"
                self.con_fecha_inicio = con.fecha_inicio
                self.con_fecha_fin = con.fecha_fin
                self.con_monto = str(con.monto)
                self.editando_contrato_id = con_id

    def eliminar_contrato(self, con_id: int):
        with rx.session() as session:
            con = session.get(Contrato, con_id)
            if con:
                session.delete(con)
                session.commit()
        self.cargar_datos()

    @rx.var
    def opciones_contratos_select(self) -> List[str]:
        """Muestra una lista legible de contratos para cobrar"""
        return [f"{c.id} - {c.inmueble.calle} (Inq: {c.inquilino.apellido})" for c in self.lista_contratos]

    def guardar_pago(self):
        if not self.pago_contrato_select:
            return
        id_con = int(self.pago_contrato_select.split(" - ")[0])

        with rx.session() as session:
            if self.editando_pago_id:
                # Editar pago existente
                pago = session.get(Pago, self.editando_pago_id)
                if pago:
                    pago.contrato_id = id_con
                    pago.periodo = self.pago_periodo
                    pago.fecha = self.pago_fecha
                    pago.monto = float(self.pago_monto) if self.pago_monto else 0.0
                    session.add(pago)
                    session.commit()
                self.editando_pago_id = None
            else:
                # Crear nuevo pago
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
        self.pago_fecha = ""
        self.pago_monto = ""

    def editar_pago(self, pago_id: int):
        with rx.session() as session:
            pago = session.exec(
                select(Pago)
                .where(Pago.id == pago_id)
                .options(selectinload(Pago.contrato).selectinload(Contrato.inmueble), selectinload(Pago.contrato).selectinload(Contrato.inquilino))
            ).first()
            if pago:
                self.pago_contrato_select = f"{pago.contrato_id} - {pago.contrato.inmueble.calle} (Inq: {pago.contrato.inquilino.apellido})"
                self.pago_periodo = pago.periodo
                self.pago_fecha = pago.fecha
                self.pago_monto = str(pago.monto)
                self.editando_pago_id = pago_id

    def eliminar_pago(self, pago_id: int):
        with rx.session() as session:
            pago = session.get(Pago, pago_id)
            if pago:
                session.delete(pago)
                session.commit()
        self.cargar_datos()
