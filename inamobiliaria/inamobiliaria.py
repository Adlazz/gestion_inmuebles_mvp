import reflex as rx
from typing import Optional, List
from sqlmodel import select, func, cast, Float
from .models import Propietario, Inmueble, Inquilino, Contrato, Pago
from sqlalchemy.orm import selectinload

# --- 1. ESTADO (LOGICA) ---
class State(rx.State):
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

    # --- VARIABLES PAGO (NUEVO) ---
    pago_contrato_select: str = ""
    pago_periodo: str = ""
    pago_fecha: str = ""
    pago_monto: str = ""
    lista_pagos: List[Pago] = []

    # --- VARIABLES DEL DASHBOARD (NUEVO) ---
    stat_propietarios: int = 0
    stat_inmuebles: int = 0
    stat_contratos_activos: int = 0
    stat_total_pagos: float = 0.0

    # --- CARGA GENERAL ---
    def cargar_datos(self):
            with rx.session() as session:
                # 1. Cargas de listas normales (como ya tenías)
                self.lista_propietarios = session.exec(select(Propietario)).all()
                self.lista_inmuebles = session.exec(select(Inmueble).options(selectinload(Inmueble.propietario))).all()
                self.lista_inquilinos = session.exec(select(Inquilino)).all()
                self.lista_contratos = session.exec(select(Contrato).options(selectinload(Contrato.inmueble), selectinload(Contrato.inquilino))).all()
                self.lista_pagos = session.exec(select(Pago).options(selectinload(Pago.contrato).selectinload(Contrato.inmueble), selectinload(Pago.contrato).selectinload(Contrato.inquilino))).all()

                # 2. CÁLCULOS PARA EL DASHBOARD (NUEVO)
                # Contar filas en cada tabla
                self.stat_propietarios = session.exec(select(func.count(Propietario.id))).one()
                self.stat_inmuebles = session.exec(select(func.count(Inmueble.id))).one()
                self.stat_contratos_activos = session.exec(select(func.count(Contrato.id))).one()
                
                # Sumar el dinero de la tabla Pagos
                # Usamos 'or 0.0' por si la tabla está vacía para que no de error
                total = session.exec(select(func.sum(Pago.monto))).one()
                self.stat_total_pagos = total if total else 0.0

    # --- GUARDAR ENTIDADES ---
    def guardar_propietario(self):
        with rx.session() as session:
            nuevo = Propietario(nombre=self.form_prop_nombre, apellido=self.form_prop_apellido, dni=self.form_prop_dni, email=self.form_prop_email)
            session.add(nuevo); session.commit(); session.refresh(nuevo)
        self.cargar_datos(); self.form_prop_nombre = ""; self.form_prop_apellido = ""; self.form_prop_dni = ""; self.form_prop_email = ""

    @rx.var
    def opciones_propietarios(self) -> List[str]:
        return [f"{p.id} - {p.nombre} {p.apellido}" for p in self.lista_propietarios]

    def guardar_inmueble(self):
        if not self.inm_propietario_select: return
        id_dueno = int(self.inm_propietario_select.split(" - ")[0])
        with rx.session() as session:
            nuevo = Inmueble(calle=self.inm_calle, altura=self.inm_altura, barrio=self.inm_barrio, localidad=self.inm_localidad, cp=self.inm_cp, propietario_id=id_dueno)
            session.add(nuevo); session.commit(); session.refresh(nuevo)
        self.cargar_datos(); self.inm_calle = ""; self.inm_altura = ""; self.inm_barrio = ""

    def guardar_inquilino(self):
        with rx.session() as session:
            nuevo = Inquilino(nombre=self.form_inq_nombre, apellido=self.form_inq_apellido, dni=self.form_inq_dni, email=self.form_inq_email)
            session.add(nuevo); session.commit(); session.refresh(nuevo)
        self.cargar_datos(); self.form_inq_nombre = ""; self.form_inq_apellido = ""; self.form_inq_dni = ""; self.form_inq_email = ""

    @rx.var
    def opciones_inmuebles_select(self) -> List[str]:
        return [f"{i.id} - {i.calle} {i.altura} ({i.barrio})" for i in self.lista_inmuebles]
    
    @rx.var
    def opciones_inquilinos_select(self) -> List[str]:
        return [f"{i.id} - {i.nombre} {i.apellido}" for i in self.lista_inquilinos]

    def guardar_contrato(self):
        if not self.con_inmueble_select or not self.con_inquilino_select: return
        id_inm = int(self.con_inmueble_select.split(" - ")[0])
        id_inq = int(self.con_inquilino_select.split(" - ")[0])
        with rx.session() as session:
            nuevo = Contrato(inmueble_id=id_inm, inquilino_id=id_inq, fecha_inicio=self.con_fecha_inicio, fecha_fin=self.con_fecha_fin, monto=float(self.con_monto) if self.con_monto else 0.0)
            session.add(nuevo); session.commit(); session.refresh(nuevo)
        self.cargar_datos(); self.con_monto = ""

    # --- GUARDAR PAGO (NUEVO) ---
    @rx.var
    def opciones_contratos_select(self) -> List[str]:
        """Muestra una lista legible de contratos para cobrar"""
        return [f"{c.id} - {c.inmueble.calle} (Inq: {c.inquilino.apellido})" for c in self.lista_contratos]

    def guardar_pago(self):
        if not self.pago_contrato_select: return
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

# --- 3. INTERFAZ (VISTAS) ---
def vista_dashboard():
    return rx.vstack(
        rx.heading("Resumen General", size="6", margin_bottom="1em"),
        
        # Grupo de Estadísticas
        rx.flex(
            # Tarjeta 1: Inmuebles
            rx.card(
                rx.vstack(
                    rx.text("Inmuebles", size="2", weight="bold", color="gray"),
                    rx.heading(State.stat_inmuebles, size="7"),
                    rx.icon("building", size=30, color="blue"),
                    align_items="center",
                ),
                width="200px"
            ),
            # Tarjeta 2: Contratos
            rx.card(
                rx.vstack(
                    rx.text("Contratos Activos", size="2", weight="bold", color="gray"),
                    rx.heading(State.stat_contratos_activos, size="7"),
                    rx.icon("file-text", size=30, color="green"),
                    align_items="center",
                ),
                width="200px"
            ),
            # Tarjeta 3: Recaudación
            rx.card(
                rx.vstack(
                    rx.text("Caja Total (Histórico)", size="2", weight="bold", color="gray"),
                    rx.heading(f"${State.stat_total_pagos}", size="7", color="green"),
                    rx.icon("dollar-sign", size=30, color="green"),
                    align_items="center",
                ),
                width="250px"
            ),
            # Tarjeta 4: Propietarios
            rx.card(
                rx.vstack(
                    rx.text("Propietarios", size="2", weight="bold", color="gray"),
                    rx.heading(State.stat_propietarios, size="7"),
                    rx.icon("users", size=30, color="purple"),
                    align_items="center",
                ),
                width="200px"
            ),
            spacing="4",
            flex_wrap="wrap",
            width="100%",
            justify="center"
        ),
        
        rx.divider(margin_top="2em"),
        rx.heading("Accesos Rápidos", size="4", margin_top="1em"),
        rx.text("Seleccione una pestaña arriba para comenzar a gestionar.", color="gray"),
        
        padding="2em",
        width="100%"
    )

def vista_propietarios():
    return rx.vstack(
        rx.heading("Gestión de Propietarios", size="4"),
        rx.flex(rx.input(placeholder="Nombre", value=State.form_prop_nombre, on_change=State.set_form_prop_nombre), rx.input(placeholder="Apellido", value=State.form_prop_apellido, on_change=State.set_form_prop_apellido), rx.input(placeholder="DNI", value=State.form_prop_dni, on_change=State.set_form_prop_dni), rx.input(placeholder="Email", value=State.form_prop_email, on_change=State.set_form_prop_email), rx.button("Guardar", on_click=State.guardar_propietario), spacing="3", direction="column"),
        rx.divider(),
        rx.table.root(rx.table.header(rx.table.row(rx.table.column_header_cell("Nombre"), rx.table.column_header_cell("DNI"))), rx.table.body(rx.foreach(State.lista_propietarios, lambda p: rx.table.row(rx.table.cell(p.nombre + " " + p.apellido), rx.table.cell(p.dni))))),
        spacing="4", width="100%"
    )

def vista_inmuebles():
    return rx.vstack(
        rx.heading("Gestión de Inmuebles", size="4"),
        rx.select(State.opciones_propietarios, placeholder="Seleccione Dueño...", on_change=State.set_inm_propietario_select),
        rx.flex(rx.input(placeholder="Calle", value=State.inm_calle, on_change=State.set_inm_calle), rx.input(placeholder="Altura", value=State.inm_altura, on_change=State.set_inm_altura), rx.input(placeholder="Barrio", value=State.inm_barrio, on_change=State.set_inm_barrio), rx.input(placeholder="Localidad", value=State.inm_localidad, on_change=State.set_inm_localidad), rx.input(placeholder="CP", value=State.inm_cp, on_change=State.set_inm_cp), spacing="3", wrap="wrap"),
        rx.button("Guardar", on_click=State.guardar_inmueble, color_scheme="green"),
        rx.divider(),
        rx.table.root(rx.table.header(rx.table.row(rx.table.column_header_cell("Dirección"), rx.table.column_header_cell("Dueño"))), rx.table.body(rx.foreach(State.lista_inmuebles, lambda i: rx.table.row(rx.table.cell(i.calle + " " + i.altura), rx.table.cell(i.propietario.nombre + " " + i.propietario.apellido))))),
        spacing="4", width="100%"
    )

def vista_inquilinos():
    return rx.vstack(
        rx.heading("Gestión de Inquilinos", size="4"),
        rx.flex(rx.input(placeholder="Nombre", value=State.form_inq_nombre, on_change=State.set_form_inq_nombre), rx.input(placeholder="Apellido", value=State.form_inq_apellido, on_change=State.set_form_inq_apellido), rx.input(placeholder="DNI", value=State.form_inq_dni, on_change=State.set_form_inq_dni), rx.input(placeholder="Email", value=State.form_inq_email, on_change=State.set_form_inq_email), rx.button("Guardar", on_click=State.guardar_inquilino, color_scheme="orange"), spacing="3", direction="column"),
        rx.divider(),
        rx.table.root(rx.table.header(rx.table.row(rx.table.column_header_cell("Inquilino"), rx.table.column_header_cell("Email"))), rx.table.body(rx.foreach(State.lista_inquilinos, lambda i: rx.table.row(rx.table.cell(i.nombre + " " + i.apellido), rx.table.cell(i.email))))),
        spacing="4", width="100%"
    )

def vista_contratos():
    return rx.vstack(
        rx.heading("Nuevo Contrato", size="4"),
        rx.flex(rx.select(State.opciones_inmuebles_select, placeholder="Inmueble...", on_change=State.set_con_inmueble_select, width="100%"), rx.select(State.opciones_inquilinos_select, placeholder="Inquilino...", on_change=State.set_con_inquilino_select, width="100%"), rx.text("Desde - Hasta:"), rx.flex(rx.input(type="date", on_change=State.set_con_fecha_inicio), rx.input(type="date", on_change=State.set_con_fecha_fin), spacing="2"), rx.input(placeholder="Monto Mensual ($)", value=State.con_monto, on_change=State.set_con_monto), rx.button("Crear Contrato", on_click=State.guardar_contrato, color_scheme="crimson"), spacing="3", direction="column", width="100%"),
        rx.divider(),
        rx.heading("Contratos Activos", size="3"),
        rx.table.root(rx.table.header(rx.table.row(rx.table.column_header_cell("Inmueble"), rx.table.column_header_cell("Inquilino"), rx.table.column_header_cell("Monto"))), rx.table.body(rx.foreach(State.lista_contratos, lambda c: rx.table.row(rx.table.cell(c.inmueble.calle), rx.table.cell(c.inquilino.apellido), rx.table.cell("$" + c.monto.to_string()))))),
        spacing="4", width="100%"
    )

def vista_pagos():
    return rx.vstack(
        rx.heading("Registrar Cobro de Alquiler", size="4"),
        rx.text("Seleccione sobre qué contrato va a cobrar:", color="gray", size="2"),
        rx.select(State.opciones_contratos_select, placeholder="Seleccione Contrato...", on_change=State.set_pago_contrato_select),
        
        rx.flex(
            rx.input(placeholder="Periodo (Ej: Enero 2025)", value=State.pago_periodo, on_change=State.set_pago_periodo),
            rx.input(placeholder="Monto Pagado", value=State.pago_monto, on_change=State.set_pago_monto),
            rx.text("Fecha de Pago:"),
            rx.input(type="date", on_change=State.set_pago_fecha),
            spacing="3",
            direction="column"
        ),
        rx.button("Registrar Pago", on_click=State.guardar_pago, color_scheme="violet"),
        
        rx.divider(),
        rx.heading("Historial de Pagos", size="3"),
        rx.table.root(
            rx.table.header(rx.table.row(
                rx.table.column_header_cell("Fecha"), 
                rx.table.column_header_cell("Periodo"),
                rx.table.column_header_cell("Inquilino"),
                rx.table.column_header_cell("Monto")
            )),
            rx.table.body(rx.foreach(State.lista_pagos, lambda p: rx.table.row(
                rx.table.cell(p.fecha), 
                rx.table.cell(p.periodo),
                rx.table.cell(p.contrato.inquilino.apellido),
                rx.table.cell("$" + p.monto.to_string())
            ))),
        ),
        spacing="4", width="100%"
    )

def index() -> rx.Component:
    return rx.container(
        rx.heading("Sistema de Gestión Inmobiliaria", size="8", margin_bottom="1em"),
        rx.tabs.root(
            rx.tabs.list(
                rx.tabs.trigger("Inicio", value="tab0"), # <-- NUEVA
                rx.tabs.trigger("Propietarios", value="tab1"),
                rx.tabs.trigger("Inmuebles", value="tab2"),
                rx.tabs.trigger("Inquilinos", value="tab3"),
                rx.tabs.trigger("Contratos", value="tab4"),
                rx.tabs.trigger("Pagos (Caja)", value="tab5"),
            ),
            # Contenido de la nueva pestaña
            rx.tabs.content(vista_dashboard(), value="tab0", padding="2em", border="1px solid #eaeaea"),
            
            rx.tabs.content(vista_propietarios(), value="tab1", padding="2em", border="1px solid #eaeaea"),
            rx.tabs.content(vista_inmuebles(), value="tab2", padding="2em", border="1px solid #eaeaea"),
            rx.tabs.content(vista_inquilinos(), value="tab3", padding="2em", border="1px solid #eaeaea"),
            rx.tabs.content(vista_contratos(), value="tab4", padding="2em", border="1px solid #eaeaea"),
            rx.tabs.content(vista_pagos(), value="tab5", padding="2em", border="1px solid #eaeaea"),
            
            default_value="tab0", # <-- Hacemos que inicie en el Dashboard
            width="100%"
        ),
        on_mount=State.cargar_datos, 
        padding="2em", 
        max_width="1000px"
    )

app = rx.App()
app.add_page(index)