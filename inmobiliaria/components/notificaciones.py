import reflex as rx


def mostrar_notificaciones() -> rx.Component:
    """Componente que muestra notificaciones de éxito y error"""
    from ..state import State

    return rx.vstack(
        # Notificación de error
        rx.cond(
            State.mensaje_error != "",
            rx.callout.root(
                rx.flex(
                    rx.callout.icon(rx.icon("triangle-alert")),
                    rx.callout.text(State.mensaje_error),
                    rx.icon("x", on_click=State.cerrar_mensaje_error, cursor="pointer"),
                    spacing="2",
                    align="center",
                    width="100%"
                ),
                color_scheme="red",
                role="alert",
            )
        ),
        # Notificación de éxito
        rx.cond(
            State.mensaje_exito != "",
            rx.callout.root(
                rx.flex(
                    rx.callout.icon(rx.icon("circle-check")),
                    rx.callout.text(State.mensaje_exito),
                    rx.icon("x", on_click=State.cerrar_mensaje_exito, cursor="pointer"),
                    spacing="2",
                    align="center",
                    width="100%"
                ),
                color_scheme="green",
                role="status",
            )
        ),
        spacing="2",
        width="100%",
        margin_bottom="1em"
    )
