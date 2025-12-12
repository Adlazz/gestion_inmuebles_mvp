import reflex as rx
from ..state import State


def vista_pagos():
    return rx.vstack(
        rx.heading("Registrar Cobro de Alquiler", size="4"),
        rx.text("Seleccione sobre qué contrato va a cobrar:", color="gray", size="2"),
        rx.select(
            State.opciones_contratos_select,
            placeholder="Seleccione Contrato...",
            on_change=State.set_pago_contrato_select
        ),

        rx.flex(
            rx.input(
                placeholder="Periodo (Ej: Enero 2025)",
                value=State.pago_periodo,
                on_change=State.set_pago_periodo
            ),
            rx.input(
                placeholder="Monto Pagado",
                value=State.pago_monto,
                on_change=State.set_pago_monto
            ),
            rx.text("Fecha de Pago:"),
            rx.input(type="date", on_change=State.set_pago_fecha),
            spacing="3",
            direction="column"
        ),
        rx.button("Registrar Pago", on_click=State.guardar_pago, color_scheme="violet"),

        rx.divider(),
        rx.heading("Historial de Pagos", size="3"),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Fecha"),
                    rx.table.column_header_cell("Periodo"),
                    rx.table.column_header_cell("Inquilino"),
                    rx.table.column_header_cell("Monto"),
                    rx.table.column_header_cell("Acciones")
                )
            ),
            rx.table.body(
                rx.foreach(
                    State.lista_pagos,
                    lambda p: rx.table.row(
                        rx.table.cell(p.fecha),
                        rx.table.cell(p.periodo),
                        rx.table.cell(p.contrato.inquilino.apellido),
                        rx.table.cell("$" + p.monto.to_string()),
                        rx.table.cell(
                            rx.flex(
                                rx.button("Editar", on_click=lambda: State.editar_pago(p.id), size="1"),
                                rx.button("Eliminar", on_click=lambda: State.abrir_dialog_eliminar("pago", p.id), size="1", color_scheme="red"),
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
