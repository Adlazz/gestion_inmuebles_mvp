import reflex as rx
from typing import List
from sqlmodel import select, func
from sqlalchemy.exc import IntegrityError
from .models import Propietario, Inmueble, Inquilino, Contrato, Pago
from .services import (
    ValidacionesService,
    PropietarioService,
    InmuebleService,
    InquilinoService,
    ContratoService,
    PagoService
)


class State(rx.State):
    # Configuración para desactivar setters automáticos
    state_auto_setters = False

    # --- VARIABLES PROPIETARIO ---
    form_prop_nombre: str = ""
    form_prop_apellido: str = ""
    form_prop_dni: str = ""
    form_prop_email: str = ""
    lista_propietarios: List[Propietario] = []

    # --- VARIABLES INMUEBLE ---
    inm_calle: str = ""
    inm_altura: str = ""
    inm_barrio: str = ""
    inm_localidad: str = ""
    inm_cp: str = ""
    inm_propietario_select: str = ""
    lista_inmuebles: List[Inmueble] = []

    # --- VARIABLES INQUILINO ---
    form_inq_nombre: str = ""
    form_inq_apellido: str = ""
    form_inq_dni: str = ""
    form_inq_email: str = ""
    lista_inquilinos: List[Inquilino] = []

    # --- VARIABLES CONTRATO ---
    con_inmueble_select: str = ""
    con_inquilino_select: str = ""
    con_fecha_inicio: str = ""
    con_fecha_fin: str = ""
    con_monto: str = ""
    lista_contratos: List[Contrato] = []

    # --- VARIABLES PAGO ---
    pago_contrato_select: str = ""
    pago_periodo: str = ""
    pago_fecha: str = ""
    pago_monto: str = ""
    lista_pagos: List[Pago] = []

    # --- VARIABLES DEL DASHBOARD ---
    stat_propietarios: int = 0
    stat_inmuebles: int = 0
    stat_contratos_activos: int = 0
    stat_total_pagos: float = 0.0

    # --- VARIABLES PARA EDICIÓN ---
    editando_propietario_id: int | None = None
    editando_inmueble_id: int | None = None
    editando_inquilino_id: int | None = None
    editando_contrato_id: int | None = None
    editando_pago_id: int | None = None

    # --- VARIABLES PARA MENSAJES Y CONFIRMACIONES ---
    mensaje_error: str = ""
    mensaje_exito: str = ""
    mostrar_dialog_eliminar: bool = False
    tipo_entidad_eliminar: str = ""
    id_entidad_eliminar: int = 0
    cargando: bool = False

    # --- SETTERS EXPLÍCITOS ---
    def set_form_prop_nombre(self, value: str):
        self.form_prop_nombre = value

    def set_form_prop_apellido(self, value: str):
        self.form_prop_apellido = value

    def set_form_prop_dni(self, value: str):
        self.form_prop_dni = value

    def set_form_prop_email(self, value: str):
        self.form_prop_email = value

    def set_inm_propietario_select(self, value: str):
        self.inm_propietario_select = value

    def set_inm_calle(self, value: str):
        self.inm_calle = value

    def set_inm_altura(self, value: str):
        self.inm_altura = value

    def set_inm_barrio(self, value: str):
        self.inm_barrio = value

    def set_inm_localidad(self, value: str):
        self.inm_localidad = value

    def set_inm_cp(self, value: str):
        self.inm_cp = value

    def set_form_inq_nombre(self, value: str):
        self.form_inq_nombre = value

    def set_form_inq_apellido(self, value: str):
        self.form_inq_apellido = value

    def set_form_inq_dni(self, value: str):
        self.form_inq_dni = value

    def set_form_inq_email(self, value: str):
        self.form_inq_email = value

    def set_con_inmueble_select(self, value: str):
        self.con_inmueble_select = value

    def set_con_inquilino_select(self, value: str):
        self.con_inquilino_select = value

    def set_con_fecha_inicio(self, value: str):
        self.con_fecha_inicio = value

    def set_con_fecha_fin(self, value: str):
        self.con_fecha_fin = value

    def set_con_monto(self, value: str):
        self.con_monto = value

    def set_pago_contrato_select(self, value: str):
        self.pago_contrato_select = value

    def set_pago_periodo(self, value: str):
        self.pago_periodo = value

    def set_pago_monto(self, value: str):
        self.pago_monto = value

    def set_pago_fecha(self, value: str):
        self.pago_fecha = value

    # --- CONTROL DE DIÁLOGOS Y MENSAJES ---
    def cerrar_mensaje_error(self):
        self.mensaje_error = ""

    def cerrar_mensaje_exito(self):
        self.mensaje_exito = ""

    def mostrar_error(self, mensaje: str):
        """Muestra un mensaje de error"""
        self.mensaje_error = mensaje
        self.mensaje_exito = ""

    def mostrar_exito(self, mensaje: str):
        """Muestra un mensaje de éxito"""
        self.mensaje_exito = mensaje
        self.mensaje_error = ""

    def abrir_dialog_eliminar(self, tipo: str, id_entidad: int):
        self.tipo_entidad_eliminar = tipo
        self.id_entidad_eliminar = id_entidad
        self.mostrar_dialog_eliminar = True

    def cerrar_dialog_eliminar(self):
        self.mostrar_dialog_eliminar = False
        self.tipo_entidad_eliminar = ""
        self.id_entidad_eliminar = 0

    # --- CARGA GENERAL ---
    def cargar_datos(self):
        """Carga todos los datos desde la base de datos usando services"""
        try:
            self.cargando = True
            with rx.session() as session:
                # Cargas de listas usando services
                self.lista_propietarios = PropietarioService.obtener_todos(session)
                self.lista_inmuebles = InmuebleService.obtener_todos(session)
                self.lista_inquilinos = InquilinoService.obtener_todos(session)
                self.lista_contratos = ContratoService.obtener_todos(session)
                self.lista_pagos = PagoService.obtener_todos(session)

                # Cálculos para el dashboard
                self.stat_propietarios = session.exec(select(func.count(Propietario.id))).one()
                self.stat_inmuebles = session.exec(select(func.count(Inmueble.id))).one()
                self.stat_contratos_activos = session.exec(select(func.count(Contrato.id))).one()
                self.stat_total_pagos = PagoService.calcular_total_pagos(session)
        except Exception as e:
            self.mostrar_error(f"Error al cargar datos: {str(e)}")
        finally:
            self.cargando = False

    # --- PROPIETARIOS ---
    def guardar_propietario(self):
        """Crea o actualiza un propietario"""
        try:
            self.cargando = True

            # Validaciones
            valido, error = ValidacionesService.validar_campos_obligatorios(
                nombre=self.form_prop_nombre,
                apellido=self.form_prop_apellido
            )
            if not valido:
                self.mostrar_error(error)
                return

            valido, error = ValidacionesService.validar_dni(self.form_prop_dni)
            if not valido:
                self.mostrar_error(error)
                return

            valido, error = ValidacionesService.validar_email(self.form_prop_email)
            if not valido:
                self.mostrar_error(error)
                return

            with rx.session() as session:
                # Verificar duplicados
                id_actual = self.editando_propietario_id
                dni_existe = PropietarioService.buscar_por_dni(session, self.form_prop_dni, id_actual)
                if dni_existe:
                    self.mostrar_error(f"El DNI {self.form_prop_dni} ya está registrado")
                    return

                email_existe = PropietarioService.buscar_por_email(session, self.form_prop_email, id_actual)
                if email_existe:
                    self.mostrar_error(f"El email {self.form_prop_email} ya está registrado")
                    return

                # Guardar usando service
                es_edicion = self.editando_propietario_id is not None
                if es_edicion:
                    PropietarioService.actualizar(
                        session,
                        self.editando_propietario_id,
                        self.form_prop_nombre,
                        self.form_prop_apellido,
                        self.form_prop_dni,
                        self.form_prop_email
                    )
                    self.editando_propietario_id = None
                    self.mostrar_exito("Propietario actualizado exitosamente")
                else:
                    PropietarioService.crear(
                        session,
                        self.form_prop_nombre,
                        self.form_prop_apellido,
                        self.form_prop_dni,
                        self.form_prop_email
                    )
                    self.mostrar_exito("Propietario creado exitosamente")

            self.cargar_datos()
            self._limpiar_form_propietario()
        except Exception as e:
            self.mostrar_error(f"Error al guardar propietario: {str(e)}")
        finally:
            self.cargando = False

    def editar_propietario(self, prop_id: int):
        """Carga datos del propietario en el formulario para edición"""
        try:
            with rx.session() as session:
                prop = PropietarioService.obtener_por_id(session, prop_id)
                if prop:
                    self.form_prop_nombre = prop.nombre
                    self.form_prop_apellido = prop.apellido
                    self.form_prop_dni = prop.dni
                    self.form_prop_email = prop.email
                    self.editando_propietario_id = prop_id
                else:
                    self.mostrar_error("Propietario no encontrado")
        except Exception as e:
            self.mostrar_error(f"Error al cargar propietario: {str(e)}")

    def eliminar_propietario(self, prop_id: int):
        """Elimina un propietario verificando constraints"""
        try:
            self.cargando = True
            with rx.session() as session:
                # Verificar si tiene inmuebles asociados
                tiene_inmuebles, cantidad = PropietarioService.tiene_inmuebles(session, prop_id)
                if tiene_inmuebles:
                    self.mostrar_error(f"No se puede eliminar el propietario porque tiene {cantidad} inmueble(s) asociado(s)")
                    return

                PropietarioService.eliminar(session, prop_id)
                self.mostrar_exito("Propietario eliminado exitosamente")

            self.cargar_datos()
            self.cerrar_dialog_eliminar()
        except IntegrityError:
            self.mostrar_error("Error al eliminar el propietario debido a restricciones de base de datos")
        except Exception as e:
            self.mostrar_error(f"Error al eliminar propietario: {str(e)}")
        finally:
            self.cargando = False

    def _limpiar_form_propietario(self):
        """Limpia el formulario de propietario"""
        self.form_prop_nombre = ""
        self.form_prop_apellido = ""
        self.form_prop_dni = ""
        self.form_prop_email = ""

    @rx.var
    def opciones_propietarios(self) -> List[str]:
        return [f"{p.id} - {p.nombre} {p.apellido}" for p in self.lista_propietarios]

    # --- INMUEBLES ---
    def guardar_inmueble(self):
        """Crea o actualiza un inmueble"""
        try:
            self.cargando = True

            # Validaciones
            valido, error = ValidacionesService.validar_campos_obligatorios(
                calle=self.inm_calle,
                altura=self.inm_altura
            )
            if not valido:
                self.mostrar_error(error)
                return

            if not self.inm_propietario_select:
                self.mostrar_error("Debe seleccionar un propietario")
                return

            id_dueno = int(self.inm_propietario_select.split(" - ")[0])
            with rx.session() as session:
                es_edicion = self.editando_inmueble_id is not None
                if es_edicion:
                    InmuebleService.actualizar(
                        session,
                        self.editando_inmueble_id,
                        self.inm_calle,
                        self.inm_altura,
                        self.inm_barrio,
                        self.inm_localidad,
                        self.inm_cp,
                        id_dueno
                    )
                    self.editando_inmueble_id = None
                    self.mostrar_exito("Inmueble actualizado exitosamente")
                else:
                    InmuebleService.crear(
                        session,
                        self.inm_calle,
                        self.inm_altura,
                        self.inm_barrio,
                        self.inm_localidad,
                        self.inm_cp,
                        id_dueno
                    )
                    self.mostrar_exito("Inmueble creado exitosamente")

            self.cargar_datos()
            self._limpiar_form_inmueble()
        except Exception as e:
            self.mostrar_error(f"Error al guardar inmueble: {str(e)}")
        finally:
            self.cargando = False

    def editar_inmueble(self, inm_id: int):
        """Carga datos del inmueble en el formulario para edición"""
        try:
            with rx.session() as session:
                inm = InmuebleService.obtener_por_id(session, inm_id)
                if inm:
                    self.inm_calle = inm.calle
                    self.inm_altura = inm.altura
                    self.inm_barrio = inm.barrio
                    self.inm_localidad = inm.localidad
                    self.inm_cp = inm.cp
                    self.inm_propietario_select = f"{inm.propietario_id} - {inm.propietario.nombre} {inm.propietario.apellido}"
                    self.editando_inmueble_id = inm_id
                else:
                    self.mostrar_error("Inmueble no encontrado")
        except Exception as e:
            self.mostrar_error(f"Error al cargar inmueble: {str(e)}")

    def eliminar_inmueble(self, inm_id: int):
        """Elimina un inmueble verificando constraints"""
        try:
            self.cargando = True
            with rx.session() as session:
                tiene_contratos, cantidad = InmuebleService.tiene_contratos(session, inm_id)
                if tiene_contratos:
                    self.mostrar_error(f"No se puede eliminar el inmueble porque tiene {cantidad} contrato(s) asociado(s)")
                    return

                InmuebleService.eliminar(session, inm_id)
                self.mostrar_exito("Inmueble eliminado exitosamente")

            self.cargar_datos()
            self.cerrar_dialog_eliminar()
        except IntegrityError:
            self.mostrar_error("Error al eliminar el inmueble debido a restricciones de base de datos")
        except Exception as e:
            self.mostrar_error(f"Error al eliminar inmueble: {str(e)}")
        finally:
            self.cargando = False

    def _limpiar_form_inmueble(self):
        """Limpia el formulario de inmueble"""
        self.inm_calle = ""
        self.inm_altura = ""
        self.inm_barrio = ""
        self.inm_localidad = ""
        self.inm_cp = ""

    # --- INQUILINOS ---
    def guardar_inquilino(self):
        """Crea o actualiza un inquilino"""
        try:
            self.cargando = True

            valido, error = ValidacionesService.validar_campos_obligatorios(
                nombre=self.form_inq_nombre, apellido=self.form_inq_apellido
            )
            if not valido:
                self.mostrar_error(error)
                return

            valido, error = ValidacionesService.validar_dni(self.form_inq_dni)
            if not valido:
                self.mostrar_error(error)
                return

            valido, error = ValidacionesService.validar_email(self.form_inq_email)
            if not valido:
                self.mostrar_error(error)
                return

            with rx.session() as session:
                id_actual = self.editando_inquilino_id
                if InquilinoService.buscar_por_dni(session, self.form_inq_dni, id_actual):
                    self.mostrar_error(f"El DNI {self.form_inq_dni} ya está registrado")
                    return
                if InquilinoService.buscar_por_email(session, self.form_inq_email, id_actual):
                    self.mostrar_error(f"El email {self.form_inq_email} ya está registrado")
                    return

                es_edicion = self.editando_inquilino_id is not None
                if es_edicion:
                    InquilinoService.actualizar(
                        session, self.editando_inquilino_id,
                        self.form_inq_nombre, self.form_inq_apellido,
                        self.form_inq_dni, self.form_inq_email
                    )
                    self.editando_inquilino_id = None
                    self.mostrar_exito("Inquilino actualizado exitosamente")
                else:
                    InquilinoService.crear(
                        session, self.form_inq_nombre, self.form_inq_apellido,
                        self.form_inq_dni, self.form_inq_email
                    )
                    self.mostrar_exito("Inquilino creado exitosamente")

            self.cargar_datos()
            self._limpiar_form_inquilino()
        except Exception as e:
            self.mostrar_error(f"Error al guardar inquilino: {str(e)}")
        finally:
            self.cargando = False

    def editar_inquilino(self, inq_id: int):
        """Carga datos del inquilino en el formulario para edición"""
        try:
            with rx.session() as session:
                inq = InquilinoService.obtener_por_id(session, inq_id)
                if inq:
                    self.form_inq_nombre = inq.nombre
                    self.form_inq_apellido = inq.apellido
                    self.form_inq_dni = inq.dni
                    self.form_inq_email = inq.email
                    self.editando_inquilino_id = inq_id
                else:
                    self.mostrar_error("Inquilino no encontrado")
        except Exception as e:
            self.mostrar_error(f"Error al cargar inquilino: {str(e)}")

    def eliminar_inquilino(self, inq_id: int):
        """Elimina un inquilino verificando constraints"""
        try:
            self.cargando = True
            with rx.session() as session:
                tiene_contratos, cantidad = InquilinoService.tiene_contratos(session, inq_id)
                if tiene_contratos:
                    self.mostrar_error(f"No se puede eliminar el inquilino porque tiene {cantidad} contrato(s) asociado(s)")
                    return

                InquilinoService.eliminar(session, inq_id)
                self.mostrar_exito("Inquilino eliminado exitosamente")

            self.cargar_datos()
            self.cerrar_dialog_eliminar()
        except IntegrityError:
            self.mostrar_error("Error al eliminar el inquilino debido a restricciones de base de datos")
        except Exception as e:
            self.mostrar_error(f"Error al eliminar inquilino: {str(e)}")
        finally:
            self.cargando = False

    def _limpiar_form_inquilino(self):
        """Limpia el formulario de inquilino"""
        self.form_inq_nombre = ""
        self.form_inq_apellido = ""
        self.form_inq_dni = ""
        self.form_inq_email = ""

    @rx.var
    def opciones_inmuebles_select(self) -> List[str]:
        return [f"{i.id} - {i.calle} {i.altura} ({i.barrio})" for i in self.lista_inmuebles]

    @rx.var
    def opciones_inquilinos_select(self) -> List[str]:
        return [f"{i.id} - {i.nombre} {i.apellido}" for i in self.lista_inquilinos]

    # --- CONTRATOS ---
    def guardar_contrato(self):
        """Crea o actualiza un contrato"""
        try:
            self.cargando = True

            if not self.con_inmueble_select or not self.con_inquilino_select:
                self.mostrar_error("Debe seleccionar un inmueble y un inquilino")
                return

            valido, error = ValidacionesService.validar_monto(self.con_monto)
            if not valido:
                self.mostrar_error(error)
                return

            valido, error = ValidacionesService.validar_fechas_contrato(self.con_fecha_inicio, self.con_fecha_fin)
            if not valido:
                self.mostrar_error(error)
                return

            id_inm = int(self.con_inmueble_select.split(" - ")[0])
            id_inq = int(self.con_inquilino_select.split(" - ")[0])

            with rx.session() as session:
                # Verificar si el inmueble ya tiene un contrato activo en ese período
                tiene_contrato, contrato_existente = ContratoService.inmueble_tiene_contrato_activo(
                    session,
                    id_inm,
                    self.con_fecha_inicio,
                    self.con_fecha_fin,
                    self.editando_contrato_id
                )

                if tiene_contrato:
                    self.mostrar_error(
                        f"El inmueble ya tiene un contrato activo del {contrato_existente.fecha_inicio} "
                        f"al {contrato_existente.fecha_fin}. No se pueden crear contratos con fechas solapadas."
                    )
                    return

                es_edicion = self.editando_contrato_id is not None
                if es_edicion:
                    ContratoService.actualizar(
                        session, self.editando_contrato_id, id_inm, id_inq,
                        self.con_fecha_inicio, self.con_fecha_fin, float(self.con_monto)
                    )
                    self.editando_contrato_id = None
                    self.mostrar_exito("Contrato actualizado exitosamente")
                else:
                    ContratoService.crear(
                        session, id_inm, id_inq,
                        self.con_fecha_inicio, self.con_fecha_fin, float(self.con_monto)
                    )
                    self.mostrar_exito("Contrato creado exitosamente")

            self.cargar_datos()
            self._limpiar_form_contrato()
        except Exception as e:
            self.mostrar_error(f"Error al guardar contrato: {str(e)}")
        finally:
            self.cargando = False

    def editar_contrato(self, con_id: int):
        """Carga datos del contrato en el formulario para edición"""
        try:
            with rx.session() as session:
                con = ContratoService.obtener_por_id(session, con_id)
                if con:
                    self.con_inmueble_select = f"{con.inmueble_id} - {con.inmueble.calle} {con.inmueble.altura} ({con.inmueble.barrio})"
                    self.con_inquilino_select = f"{con.inquilino_id} - {con.inquilino.nombre} {con.inquilino.apellido}"
                    self.con_fecha_inicio = con.fecha_inicio
                    self.con_fecha_fin = con.fecha_fin
                    self.con_monto = str(con.monto)
                    self.editando_contrato_id = con_id
                else:
                    self.mostrar_error("Contrato no encontrado")
        except Exception as e:
            self.mostrar_error(f"Error al cargar contrato: {str(e)}")

    def eliminar_contrato(self, con_id: int):
        """Elimina un contrato verificando constraints"""
        try:
            self.cargando = True
            with rx.session() as session:
                tiene_pagos, cantidad = ContratoService.tiene_pagos(session, con_id)
                if tiene_pagos:
                    self.mostrar_error(f"No se puede eliminar el contrato porque tiene {cantidad} pago(s) registrado(s)")
                    return

                ContratoService.eliminar(session, con_id)
                self.mostrar_exito("Contrato eliminado exitosamente")

            self.cargar_datos()
            self.cerrar_dialog_eliminar()
        except IntegrityError:
            self.mostrar_error("Error al eliminar el contrato debido a restricciones de base de datos")
        except Exception as e:
            self.mostrar_error(f"Error al eliminar contrato: {str(e)}")
        finally:
            self.cargando = False

    def _limpiar_form_contrato(self):
        """Limpia el formulario de contrato"""
        self.con_fecha_inicio = ""
        self.con_fecha_fin = ""
        self.con_monto = ""

    @rx.var
    def opciones_contratos_select(self) -> List[str]:
        """Muestra una lista legible de contratos para cobrar"""
        return [f"{c.id} - {c.inmueble.calle} (Inq: {c.inquilino.apellido})" for c in self.lista_contratos]

    # --- PAGOS ---
    def guardar_pago(self):
        """Crea o actualiza un pago"""
        try:
            self.cargando = True

            valido, error = ValidacionesService.validar_campos_obligatorios(
                contrato=self.pago_contrato_select,
                periodo=self.pago_periodo,
                fecha=self.pago_fecha
            )
            if not valido:
                self.mostrar_error(error)
                return

            valido, error = ValidacionesService.validar_monto(self.pago_monto)
            if not valido:
                self.mostrar_error(error)
                return

            id_con = int(self.pago_contrato_select.split(" - ")[0])

            with rx.session() as session:
                es_edicion = self.editando_pago_id is not None
                if es_edicion:
                    PagoService.actualizar(
                        session, self.editando_pago_id, id_con,
                        self.pago_periodo, self.pago_fecha, float(self.pago_monto)
                    )
                    self.editando_pago_id = None
                    self.mostrar_exito("Pago actualizado exitosamente")
                else:
                    PagoService.crear(
                        session, id_con,
                        self.pago_periodo, self.pago_fecha, float(self.pago_monto)
                    )
                    self.mostrar_exito("Pago registrado exitosamente")

            self.cargar_datos()
            self._limpiar_form_pago()
        except Exception as e:
            self.mostrar_error(f"Error al guardar pago: {str(e)}")
        finally:
            self.cargando = False

    def editar_pago(self, pago_id: int):
        """Carga datos del pago en el formulario para edición"""
        try:
            with rx.session() as session:
                pago = PagoService.obtener_por_id(session, pago_id)
                if pago:
                    self.pago_contrato_select = f"{pago.contrato_id} - {pago.contrato.inmueble.calle} (Inq: {pago.contrato.inquilino.apellido})"
                    self.pago_periodo = pago.periodo
                    self.pago_fecha = pago.fecha
                    self.pago_monto = str(pago.monto)
                    self.editando_pago_id = pago_id
                else:
                    self.mostrar_error("Pago no encontrado")
        except Exception as e:
            self.mostrar_error(f"Error al cargar pago: {str(e)}")

    def eliminar_pago(self, pago_id: int):
        """Elimina un pago"""
        try:
            self.cargando = True
            with rx.session() as session:
                PagoService.eliminar(session, pago_id)
                self.mostrar_exito("Pago eliminado exitosamente")

            self.cargar_datos()
            self.cerrar_dialog_eliminar()
        except IntegrityError:
            self.mostrar_error("Error al eliminar el pago debido a restricciones de base de datos")
        except Exception as e:
            self.mostrar_error(f"Error al eliminar pago: {str(e)}")
        finally:
            self.cargando = False

    def _limpiar_form_pago(self):
        """Limpia el formulario de pago"""
        self.pago_periodo = ""
        self.pago_fecha = ""
        self.pago_monto = ""

    def confirmar_eliminacion(self):
        """Ejecuta la eliminación según el tipo de entidad"""
        if self.tipo_entidad_eliminar == "propietario":
            self.eliminar_propietario(self.id_entidad_eliminar)
        elif self.tipo_entidad_eliminar == "inmueble":
            self.eliminar_inmueble(self.id_entidad_eliminar)
        elif self.tipo_entidad_eliminar == "inquilino":
            self.eliminar_inquilino(self.id_entidad_eliminar)
        elif self.tipo_entidad_eliminar == "contrato":
            self.eliminar_contrato(self.id_entidad_eliminar)
        elif self.tipo_entidad_eliminar == "pago":
            self.eliminar_pago(self.id_entidad_eliminar)
