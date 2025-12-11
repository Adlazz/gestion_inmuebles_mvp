import reflex as rx
from ..state import State


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
