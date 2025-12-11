import reflex as rx
from ..state import State


def vista_inquilinos():
    return rx.vstack(
        rx.heading("Gestión de Inquilinos", size="4"),
        rx.flex(
            rx.input(
                placeholder="Nombre",
                value=State.form_inq_nombre,
                on_change=State.set_form_inq_nombre
            ),
            rx.input(
                placeholder="Apellido",
                value=State.form_inq_apellido,
                on_change=State.set_form_inq_apellido
            ),
            rx.input(
                placeholder="DNI",
                value=State.form_inq_dni,
                on_change=State.set_form_inq_dni
            ),
            rx.input(
                placeholder="Email",
                value=State.form_inq_email,
                on_change=State.set_form_inq_email
            ),
            rx.button("Guardar", on_click=State.guardar_inquilino, color_scheme="orange"),
            spacing="3",
            direction="column"
        ),
        rx.divider(),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Inquilino"),
                    rx.table.column_header_cell("Email")
                )
            ),
            rx.table.body(
                rx.foreach(
                    State.lista_inquilinos,
                    lambda i: rx.table.row(
                        rx.table.cell(i.nombre + " " + i.apellido),
                        rx.table.cell(i.email)
                    )
                )
            )
        ),
        spacing="4",
        width="100%"
    )
