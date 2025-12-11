import reflex as rx
from ..state import State


def vista_propietarios():
    return rx.vstack(
        rx.heading("Gestión de Propietarios", size="4"),
        rx.flex(
            rx.input(
                placeholder="Nombre",
                value=State.form_prop_nombre,
                on_change=State.set_form_prop_nombre
            ),
            rx.input(
                placeholder="Apellido",
                value=State.form_prop_apellido,
                on_change=State.set_form_prop_apellido
            ),
            rx.input(
                placeholder="DNI",
                value=State.form_prop_dni,
                on_change=State.set_form_prop_dni
            ),
            rx.input(
                placeholder="Email",
                value=State.form_prop_email,
                on_change=State.set_form_prop_email
            ),
            rx.button("Guardar", on_click=State.guardar_propietario),
            spacing="3",
            direction="column"
        ),
        rx.divider(),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Nombre"),
                    rx.table.column_header_cell("DNI")
                )
            ),
            rx.table.body(
                rx.foreach(
                    State.lista_propietarios,
                    lambda p: rx.table.row(
                        rx.table.cell(p.nombre + " " + p.apellido),
                        rx.table.cell(p.dni)
                    )
                )
            )
        ),
        spacing="4",
        width="100%"
    )
