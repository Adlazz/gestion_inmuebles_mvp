import reflex as rx
from ..state import State
from datetime import datetime


def badge_estado_contrato(fecha_inicio: rx.Var, fecha_fin: rx.Var) -> rx.Component:
    """Componente que muestra el badge de estado del contrato"""
    hoy = datetime.now().date().isoformat()

    # Determinar estado y color usando rx.cond
    return rx.cond(
        fecha_inicio > hoy,
        rx.badge("Futuro", color_scheme="blue"),
        rx.cond(
            fecha_fin < hoy,
            rx.badge("Vencido", color_scheme="red"),
            rx.badge("Activo", color_scheme="green")
        )
    )


def vista_contratos():
    return rx.vstack(
        rx.heading("Nuevo Contrato", size="4"),
        rx.flex(
            rx.select(
                State.opciones_inmuebles_select,
                placeholder="Inmueble...",
                on_change=State.set_con_inmueble_select,
                width="100%"
            ),
            rx.select(
                State.opciones_inquilinos_select,
                placeholder="Inquilino...",
                on_change=State.set_con_inquilino_select,
                width="100%"
            ),
            rx.text("Desde - Hasta:"),
            rx.flex(
                rx.input(type="date", on_change=State.set_con_fecha_inicio),
                rx.input(type="date", on_change=State.set_con_fecha_fin),
                spacing="2"
            ),
            rx.input(
                placeholder="Monto Mensual ($)",
                value=State.con_monto,
                on_change=State.set_con_monto
            ),
            rx.button("Crear Contrato", on_click=State.guardar_contrato, color_scheme="crimson"),
            spacing="3",
            direction="column",
            width="100%"
        ),
        rx.divider(),
        rx.heading("Listado de Contratos", size="3"),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Inmueble"),
                    rx.table.column_header_cell("Inquilino"),
                    rx.table.column_header_cell("Período"),
                    rx.table.column_header_cell("Monto"),
                    rx.table.column_header_cell("Estado"),
                    rx.table.column_header_cell("Acciones")
                )
            ),
            rx.table.body(
                rx.foreach(
                    State.lista_contratos,
                    lambda c: rx.table.row(
                        rx.table.cell(c.inmueble.calle),
                        rx.table.cell(c.inquilino.apellido),
                        rx.table.cell(c.fecha_inicio + " / " + c.fecha_fin),
                        rx.table.cell("$" + c.monto.to_string()),
                        rx.table.cell(
                            badge_estado_contrato(c.fecha_inicio, c.fecha_fin)
                        ),
                        rx.table.cell(
                            rx.flex(
                                rx.button("Editar", on_click=lambda: State.editar_contrato(c.id), size="1"),
                                rx.button("Eliminar", on_click=lambda: State.abrir_dialog_eliminar("contrato", c.id), size="1", color_scheme="red"),
                                spacing="2"
                            )
                        )
                    )
                )
            )
        ),
        spacing="4",
        width="100%"
    )
