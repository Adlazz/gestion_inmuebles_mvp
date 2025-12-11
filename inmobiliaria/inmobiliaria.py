import reflex as rx
from .state import State
from .views import (
    vista_dashboard,
    vista_propietarios,
    vista_inmuebles,
    vista_inquilinos,
    vista_contratos,
    vista_pagos,
)

def index() -> rx.Component:
    return rx.container(
        rx.heading("Sistema de Gestión Inmobiliaria", size="8", margin_bottom="1em"),
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