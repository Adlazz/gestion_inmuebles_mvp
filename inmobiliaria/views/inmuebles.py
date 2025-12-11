import reflex as rx
from ..state import State


def vista_inmuebles():
    return rx.vstack(
        rx.heading("Gestión de Inmuebles", size="4"),
        rx.select(
            State.opciones_propietarios,
            placeholder="Seleccione Dueño...",
            on_change=State.set_inm_propietario_select
        ),
        rx.flex(
            rx.input(
                placeholder="Calle",
                value=State.inm_calle,
                on_change=State.set_inm_calle
            ),
            rx.input(
                placeholder="Altura",
                value=State.inm_altura,
                on_change=State.set_inm_altura
            ),
            rx.input(
                placeholder="Barrio",
                value=State.inm_barrio,
                on_change=State.set_inm_barrio
            ),
            rx.input(
                placeholder="Localidad",
                value=State.inm_localidad,
                on_change=State.set_inm_localidad
            ),
            rx.input(
                placeholder="CP",
                value=State.inm_cp,
                on_change=State.set_inm_cp
            ),
            spacing="3",
            wrap="wrap"
        ),
        rx.button("Guardar", on_click=State.guardar_inmueble, color_scheme="green"),
        rx.divider(),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Dirección"),
                    rx.table.column_header_cell("Dueño")
                )
            ),
            rx.table.body(
                rx.foreach(
                    State.lista_inmuebles,
                    lambda i: rx.table.row(
                        rx.table.cell(i.calle + " " + i.altura),
                        rx.table.cell(i.propietario.nombre + " " + i.propietario.apellido)
                    )
                )
            )
        ),
        spacing="4",
        width="100%"
    )
