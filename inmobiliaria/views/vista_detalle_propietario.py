import reflex as rx
from ..state import State


def seccion_estadisticas() -> rx.Component:
    """Sección de estadísticas del propietario"""
    return rx.cond(
        State.estadisticas_propietario,
        rx.box(
            rx.heading("Estadísticas", size="4", margin_bottom="0.5em"),
            rx.grid(
                # Tarjeta: Total de inmuebles
                rx.card(
                    rx.vstack(
                        rx.text("Total Inmuebles", size="2", color="gray"),
                        rx.text(
                            State.estadisticas_propietario.get("total_inmuebles", 0),
                            size="6",
                            weight="bold"
                        ),
                        spacing="1",
                        align="start"
                    )
                ),
                # Tarjeta: Alquilados
                rx.card(
                    rx.vstack(
                        rx.text("Alquilados", size="2", color="gray"),
                        rx.text(
                            State.estadisticas_propietario.get("inmuebles_alquilados", 0),
                            size="6",
                            weight="bold",
                            color="green"
                        ),
                        spacing="1",
                        align="start"
                    )
                ),
                # Tarjeta: Disponibles
                rx.card(
                    rx.vstack(
                        rx.text("Disponibles", size="2", color="gray"),
                        rx.text(
                            State.estadisticas_propietario.get("inmuebles_disponibles", 0),
                            size="6",
                            weight="bold",
                            color="orange"
                        ),
                        spacing="1",
                        align="start"
                    )
                ),
                # Tarjeta: Ingresos totales
                rx.card(
                    rx.vstack(
                        rx.text("Ingresos Totales", size="2", color="gray"),
                        rx.text(
                            f"${State.estadisticas_propietario.get('ingresos_totales', 0):.2f}",
                            size="6",
                            weight="bold",
                            color="blue"
                        ),
                        spacing="1",
                        align="start"
                    )
                ),
                # Tarjeta: Ingresos del mes
                rx.card(
                    rx.vstack(
                        rx.text("Ingresos este Mes", size="2", color="gray"),
                        rx.text(
                            f"${State.estadisticas_propietario.get('ingresos_mes_actual', 0):.2f}",
                            size="6",
                            weight="bold",
                            color="green"
                        ),
                        spacing="1",
                        align="start"
                    )
                ),
                # Tarjeta: Promedio mensual
                rx.card(
                    rx.vstack(
                        rx.text("Promedio Mensual", size="2", color="gray"),
                        rx.text(
                            f"${State.estadisticas_propietario.get('promedio_mensual', 0):.2f}",
                            size="6",
                            weight="bold",
                            color="purple"
                        ),
                        spacing="1",
                        align="start"
                    )
                ),
                columns="3",
                spacing="3",
                width="100%"
            ),
            margin_bottom="1em"
        )
    )


def seccion_inmuebles() -> rx.Component:
    """Sección de inmuebles del propietario"""
    return rx.box(
        rx.heading("Inmuebles", size="4", margin_bottom="0.5em"),
        rx.cond(
            State.detalle_prop_inmuebles,
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Dirección"),
                        rx.table.column_header_cell("Barrio"),
                        rx.table.column_header_cell("Localidad")
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        State.detalle_prop_inmuebles,
                        lambda inm: rx.table.row(
                            rx.table.cell(f"{inm['calle']} {inm['altura']}"),
                            rx.table.cell(inm["barrio"]),
                            rx.table.cell(inm["localidad"])
                        )
                    )
                ),
                width="100%"
            ),
            rx.text("No hay inmuebles registrados", color="gray")
        ),
        margin_bottom="1em"
    )


def seccion_pagos() -> rx.Component:
    """Sección de historial de pagos"""
    return rx.box(
        rx.heading("Historial de Pagos (últimos 20)", size="4", margin_bottom="0.5em"),
        rx.cond(
            State.detalle_prop_pagos,
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Fecha"),
                        rx.table.column_header_cell("Período"),
                        rx.table.column_header_cell("Inmueble"),
                        rx.table.column_header_cell("Inquilino"),
                        rx.table.column_header_cell("Monto")
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        State.detalle_prop_pagos,
                        lambda pago: rx.table.row(
                            rx.table.cell(pago["fecha"]),
                            rx.table.cell(pago["periodo"]),
                            rx.table.cell(pago["inmueble_direccion"]),
                            rx.table.cell(pago["inquilino_nombre"]),
                            rx.table.cell(f"${pago['monto']:.2f}", weight="bold", color="green")
                        )
                    )
                ),
                width="100%"
            ),
            rx.text("No hay pagos registrados", color="gray")
        )
    )


def vista_detalle_propietario() -> rx.Component:
    """Diálogo completo de detalle de propietario"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(
                    State.detalle_prop_nombre,
                    f"Detalle de {State.detalle_prop_nombre} {State.detalle_prop_apellido}",
                    "Detalle del Propietario"
                )
            ),
            rx.dialog.description(
                rx.cond(
                    State.detalle_prop_nombre,
                    rx.vstack(
                        rx.text(f"DNI: {State.detalle_prop_dni}"),
                        rx.text(f"Email: {State.detalle_prop_email}"),
                        spacing="1",
                        align="start"
                    ),
                    ""
                ),
                margin_bottom="1em"
            ),
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger("Estadísticas", value="stats"),
                    rx.tabs.trigger("Inmuebles", value="inmuebles"),
                    rx.tabs.trigger("Pagos", value="pagos")
                ),
                rx.tabs.content(
                    seccion_estadisticas(),
                    value="stats",
                    padding_top="1em"
                ),
                rx.tabs.content(
                    seccion_inmuebles(),
                    value="inmuebles",
                    padding_top="1em"
                ),
                rx.tabs.content(
                    seccion_pagos(),
                    value="pagos",
                    padding_top="1em"
                ),
                default_value="stats"
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button("Cerrar", variant="soft", color_scheme="gray")
                ),
                spacing="3",
                justify="end",
                margin_top="1em"
            ),
            max_width="900px",
            max_height="80vh",
            style={"overflow": "auto"}
        ),
        open=State.mostrar_detalle_propietario,
        on_open_change=State.cerrar_detalle_propietario
    )
