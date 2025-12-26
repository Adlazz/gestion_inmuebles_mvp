"""
Script para cargar datos ficticios en la base de datos.
Genera: 20 propietarios, 45 inmuebles (40 alquilados, 5 sin alquilar),
contratos en diferentes estados, y pagos con variaciones.
"""
import reflex as rx
from datetime import datetime, timedelta
import random
from inmobiliaria.models import Propietario, Inmueble, Inquilino, Contrato, Pago


# Datos ficticios
NOMBRES = ["Juan", "María", "Carlos", "Ana", "Luis", "Laura", "Pedro", "Sofía",
           "Miguel", "Valentina", "Diego", "Camila", "Fernando", "Lucía", "Jorge",
           "Martina", "Roberto", "Florencia", "Gabriel", "Victoria", "Andrés",
           "Catalina", "Ricardo", "Isabella", "Mauricio", "Emma", "Daniel", "Olivia"]

APELLIDOS = ["González", "Rodríguez", "Fernández", "López", "Martínez", "García",
             "Pérez", "Sánchez", "Romero", "Silva", "Torres", "Álvarez", "Castro",
             "Moreno", "Vargas", "Ramos", "Díaz", "Ruiz", "Gómez", "Herrera"]

CALLES = ["San Martín", "Belgrano", "Mitre", "Rivadavia", "Sarmiento", "Córdoba",
          "Corrientes", "Santa Fe", "Entre Ríos", "Independencia", "Libertad",
          "25 de Mayo", "9 de Julio", "Alem", "Maipú", "Tucumán", "Moreno",
          "Alsina", "Lavalle", "Florida", "Pellegrini", "Pueyrredón", "Callao"]

BARRIOS = ["Centro", "Villa María", "Alberdi", "General Paz", "Güemes", "Nueva Córdoba",
           "Cerro de las Rosas", "Alta Córdoba", "San Martín", "Providencia"]

LOCALIDADES = ["Córdoba", "Villa Carlos Paz", "Río Cuarto", "San Francisco", "Villa María"]


def generar_dni():
    """Genera un DNI ficticio único"""
    return str(random.randint(20000000, 45000000))


def generar_email(nombre, apellido):
    """Genera un email ficticio"""
    dominios = ["gmail.com", "hotmail.com", "yahoo.com", "outlook.com"]
    return f"{nombre.lower()}.{apellido.lower()}@{random.choice(dominios)}"


def generar_fecha(dias_atras_min, dias_atras_max):
    """Genera una fecha aleatoria en el rango especificado"""
    dias_atras = random.randint(dias_atras_min, dias_atras_max)
    fecha = datetime.now() - timedelta(days=dias_atras)
    return fecha.strftime("%Y-%m-%d")


def generar_propietarios(session):
    """Genera 20 propietarios"""
    print("Generando propietarios...")
    propietarios = []
    dnis_usados = set()

    for i in range(20):
        dni = generar_dni()
        while dni in dnis_usados:
            dni = generar_dni()
        dnis_usados.add(dni)

        nombre = random.choice(NOMBRES)
        apellido = random.choice(APELLIDOS)
        email = generar_email(nombre, apellido)

        prop = Propietario(
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            email=email
        )
        session.add(prop)
        propietarios.append(prop)

    session.commit()
    print(f"[OK] {len(propietarios)} propietarios creados")
    return propietarios


def generar_inquilinos(session, cantidad=45):
    """Genera inquilinos (uno por cada inmueble que estará alquilado)"""
    print("Generando inquilinos...")
    inquilinos = []
    dnis_usados = set()

    for i in range(cantidad):
        dni = generar_dni()
        while dni in dnis_usados:
            dni = generar_dni()
        dnis_usados.add(dni)

        nombre = random.choice(NOMBRES)
        apellido = random.choice(APELLIDOS)
        email = generar_email(nombre, apellido)

        inq = Inquilino(
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            email=email
        )
        session.add(inq)
        inquilinos.append(inq)

    session.commit()
    print(f"[OK] {len(inquilinos)} inquilinos creados")
    return inquilinos


def generar_inmuebles(session, propietarios):
    """Genera 45 inmuebles distribuidos entre los propietarios"""
    print("Generando inmuebles...")
    inmuebles = []

    # Algunos propietarios tendrán más de un inmueble
    # Distribuir 45 inmuebles entre 20 propietarios
    # 10 propietarios con 3 inmuebles = 30
    # 10 propietarios con 1-2 inmuebles = 15
    # Total = 45

    propietario_idx = 0
    for i in range(45):
        # Primeros 10 propietarios: 3 inmuebles cada uno (30 inmuebles)
        if i < 30:
            propietario = propietarios[i // 3]
        # Siguientes 10 propietarios: 1-2 inmuebles cada uno (15 inmuebles)
        else:
            if i < 35:
                propietario = propietarios[10 + (i - 30)]  # 5 propietarios con 1
            else:
                propietario = propietarios[15 + ((i - 35) // 2)]  # 5 propietarios con 2

        calle = random.choice(CALLES)
        altura = str(random.randint(100, 9999))
        barrio = random.choice(BARRIOS)
        localidad = random.choice(LOCALIDADES)
        cp = str(random.randint(5000, 5999))

        inm = Inmueble(
            calle=calle,
            altura=altura,
            barrio=barrio,
            localidad=localidad,
            cp=cp,
            propietario_id=propietario.id
        )
        session.add(inm)
        inmuebles.append(inm)

    session.commit()
    print(f"[OK] {len(inmuebles)} inmuebles creados")
    return inmuebles


def generar_contratos(session, inmuebles, inquilinos):
    """Genera contratos en diferentes estados (activos, vencidos, próximos a vencer)"""
    print("Generando contratos...")
    contratos = []

    # Dejar 5 inmuebles sin contrato
    inmuebles_con_contrato = inmuebles[:40]

    for i, inmueble in enumerate(inmuebles_con_contrato):
        inquilino = inquilinos[i]

        # Diferentes escenarios de contratos
        tipo_contrato = random.choice([
            "vencido",      # 30%
            "vencido",
            "vencido",
            "activo",       # 40%
            "activo",
            "activo",
            "activo",
            "proximo_vencer",  # 20%
            "proximo_vencer",
            "futuro"        # 10%
        ])

        if tipo_contrato == "vencido":
            # Contratos vencidos (terminaron entre 1 y 180 días atrás)
            dias_desde_inicio = random.randint(400, 800)
            duracion = random.randint(365, 730)  # 1-2 años
            fecha_inicio = datetime.now() - timedelta(days=dias_desde_inicio)
            fecha_fin = fecha_inicio + timedelta(days=duracion)

        elif tipo_contrato == "activo":
            # Contratos activos (comenzaron hace tiempo y terminan en el futuro)
            dias_desde_inicio = random.randint(90, 500)
            duracion = random.randint(365, 730)
            fecha_inicio = datetime.now() - timedelta(days=dias_desde_inicio)
            fecha_fin = fecha_inicio + timedelta(days=duracion)

        elif tipo_contrato == "proximo_vencer":
            # Contratos próximos a vencer (terminan en 1-60 días)
            dias_desde_inicio = random.randint(300, 700)
            dias_hasta_fin = random.randint(1, 60)
            fecha_inicio = datetime.now() - timedelta(days=dias_desde_inicio)
            fecha_fin = datetime.now() + timedelta(days=dias_hasta_fin)

        else:  # futuro
            # Contratos futuros (comienzan en 1-90 días)
            dias_hasta_inicio = random.randint(1, 90)
            duracion = random.randint(365, 730)
            fecha_inicio = datetime.now() + timedelta(days=dias_hasta_inicio)
            fecha_fin = fecha_inicio + timedelta(days=duracion)

        # Montos variables (entre $50,000 y $300,000)
        monto = random.randint(50, 300) * 1000

        contrato = Contrato(
            inmueble_id=inmueble.id,
            inquilino_id=inquilino.id,
            fecha_inicio=fecha_inicio.strftime("%Y-%m-%d"),
            fecha_fin=fecha_fin.strftime("%Y-%m-%d"),
            monto=float(monto)
        )
        session.add(contrato)
        contratos.append(contrato)

    session.commit()
    print(f"[OK] {len(contratos)} contratos creados")
    return contratos


def generar_pagos(session, contratos):
    """Genera pagos para los contratos con variaciones de monto"""
    print("Generando pagos...")
    pagos_count = 0

    for contrato in contratos:
        # Calcular cuántos meses han pasado desde el inicio del contrato
        fecha_inicio = datetime.strptime(contrato.fecha_inicio, "%Y-%m-%d")
        fecha_fin = datetime.strptime(contrato.fecha_fin, "%Y-%m-%d")
        hoy = datetime.now()

        # Solo generar pagos para contratos que ya comenzaron
        if fecha_inicio > hoy:
            continue

        # Calcular meses de contrato
        fecha_pago = fecha_inicio
        meses_transcurridos = 0

        while fecha_pago < min(fecha_fin, hoy):
            # Determinar si se realizó el pago este mes (90% de probabilidad)
            if random.random() < 0.9:
                # Variación en el monto del pago
                variacion_tipo = random.choice([
                    "exacto",        # 60%
                    "exacto",
                    "exacto",
                    "exacto",
                    "exacto",
                    "exacto",
                    "a_favor",       # 20%
                    "a_favor",
                    "en_contra",     # 20%
                    "en_contra"
                ])

                if variacion_tipo == "exacto":
                    monto_pago = contrato.monto
                elif variacion_tipo == "a_favor":
                    # Pago mayor (con ajuste por inflación o similar)
                    monto_pago = contrato.monto * random.uniform(1.05, 1.15)
                else:  # en_contra
                    # Pago menor (descuento o pago parcial)
                    monto_pago = contrato.monto * random.uniform(0.85, 0.95)

                # Generar período (ej: "2024-01", "2024-02")
                periodo = fecha_pago.strftime("%Y-%m")

                # Fecha de pago: entre el día 1 y 15 del mes
                dia_pago = random.randint(1, 15)
                fecha_pago_real = fecha_pago.replace(day=min(dia_pago, 28))

                pago = Pago(
                    contrato_id=contrato.id,
                    periodo=periodo,
                    fecha=fecha_pago_real.strftime("%Y-%m-%d"),
                    monto=round(monto_pago, 2)
                )
                session.add(pago)
                pagos_count += 1

            # Avanzar un mes
            meses_transcurridos += 1
            if fecha_pago.month == 12:
                fecha_pago = fecha_pago.replace(year=fecha_pago.year + 1, month=1, day=1)
            else:
                # Cambiar a día 1 para evitar problemas con meses de diferentes longitudes
                fecha_pago = fecha_pago.replace(month=fecha_pago.month + 1, day=1)

    session.commit()
    print(f"[OK] {pagos_count} pagos creados")


def limpiar_base_datos(session):
    """Elimina todos los datos existentes"""
    print("Limpiando base de datos...")

    # Eliminar en orden inverso de dependencias
    from sqlmodel import select, delete

    session.exec(delete(Pago))
    session.exec(delete(Contrato))
    session.exec(delete(Inmueble))
    session.exec(delete(Inquilino))
    session.exec(delete(Propietario))

    session.commit()
    print("[OK] Base de datos limpiada")


def main():
    """Función principal que ejecuta la carga de datos"""
    print("=" * 60)
    print("CARGA MASIVA DE DATOS FICTICIOS")
    print("=" * 60)

    with rx.session() as session:
        # Limpiar datos existentes
        limpiar_base_datos(session)

        # Generar datos
        propietarios = generar_propietarios(session)
        inquilinos = generar_inquilinos(session, cantidad=45)
        inmuebles = generar_inmuebles(session, propietarios)
        contratos = generar_contratos(session, inmuebles, inquilinos)
        generar_pagos(session, contratos)

    print("=" * 60)
    print("[OK] CARGA COMPLETADA EXITOSAMENTE")
    print("=" * 60)
    print("\nResumen:")
    print("  - 20 propietarios (algunos con multiples inmuebles)")
    print("  - 45 inmuebles (40 alquilados, 5 disponibles)")
    print("  - 45 inquilinos")
    print("  - 40 contratos (vencidos, activos, proximos a vencer, futuros)")
    print("  - Multiples pagos con variaciones de monto")
    print("\nEjecuta la app para ver los datos!")


if __name__ == "__main__":
    main()
