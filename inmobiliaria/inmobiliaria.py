import reflex as rx
from .state import State
from .views import (
    vista_dashboard,
    vista_propietarios,
    vista_inmuebles,
    vista_inquilinos,
    vista_contratos,
    vista_pagos,
    vista_detalle_propietario,
)
from .components import mostrar_notificaciones

def dialog_confirmar_eliminacion() -> rx.Component:
    """Diálogo de confirmación para eliminar registros"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Confirmar eliminación"),
            rx.dialog.description(
                "¿Está seguro de que desea eliminar este registro? Esta acción no se puede deshacer."
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button("Cancelar", variant="soft", color_scheme="gray")
                ),
                rx.dialog.close(
                    rx.button(
                        "Eliminar",
                        on_click=State.confirmar_eliminacion,
                        color_scheme="red"
                    )
                ),
                spacing="3",
                justify="end"
            )
        ),
        open=State.mostrar_dialog_eliminar,
        on_open_change=State.cerrar_dialog_eliminar
    )

def indicador_carga() -> rx.Component:
    """Indicador de carga global"""
    return rx.cond(
        State.cargando,
        rx.box(
            rx.flex(
                rx.spinner(size="3"),
                rx.text("Cargando...", size="2"),
                spacing="3",
                align="center"
            ),
            position="fixed",
            top="20px",
            right="20px",
            background="white",
            padding="1em",
            border_radius="8px",
            box_shadow="0 4px 6px rgba(0, 0, 0, 0.1)",
            z_index="1000"
        )
    )

def index() -> rx.Component:
    return rx.container(
        rx.heading("Sistema de Gestión Inmobiliaria", size="8", margin_bottom="1em"),
        mostrar_notificaciones(),
        indicador_carga(),
        dialog_confirmar_eliminacion(),
        vista_detalle_propietario(),
        rx.tabs.root(
            rx.tabs.list(
                rx.tabs.trigger("Inicio", value="tab0"),
                rx.tabs.trigger("Propietarios", value="tab1"),
                rx.tabs.trigger("Inmuebles", value="tab2"),
                rx.tabs.trigger("Inquilinos", value="tab3"),
                rx.tabs.trigger("Contratos", value="tab4"),
                rx.tabs.trigger("Pagos (Caja)", value="tab5"),
            ),
            rx.tabs.content(vista_dashboard(), value="tab0", padding="2em", border="1px solid #eaeaea"),
            rx.tabs.content(vista_propietarios(), value="tab1", padding="2em", border="1px solid #eaeaea"),
            rx.tabs.content(vista_inmuebles(), value="tab2", padding="2em", border="1px solid #eaeaea"),
            rx.tabs.content(vista_inquilinos(), value="tab3", padding="2em", border="1px solid #eaeaea"),
            rx.tabs.content(vista_contratos(), value="tab4", padding="2em", border="1px solid #eaeaea"),
            rx.tabs.content(vista_pagos(), value="tab5", padding="2em", border="1px solid #eaeaea"),
            default_value="tab0",
            width="100%"
        ),
        on_mount=State.cargar_datos,
        padding="2em",
        max_width="1000px"
    )

app = rx.App()
app.add_page(index)