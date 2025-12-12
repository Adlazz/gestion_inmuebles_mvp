# Sistema de Gestión Inmobiliaria

Sistema web para la administración integral de propiedades inmobiliarias, desarrollado con Reflex y Python.

## Descripción

Aplicación MVP (Minimum Viable Product) diseñada para inmobiliarias y administradores de propiedades que permite gestionar propietarios, inmuebles, inquilinos, contratos de alquiler y el registro de pagos desde una interfaz web intuitiva.

## Características Principales

### Dashboard Interactivo
- Visualización de métricas clave en tiempo real
- Contador de inmuebles gestionados
- Contratos activos
- Caja total histórica de pagos
- Total de propietarios registrados

### Módulos Funcionales

#### 1. Gestión de Propietarios
- Registro de propietarios con datos personales (nombre, apellido, DNI, email)
- Listado completo de propietarios
- Vista en tabla organizada

#### 2. Gestión de Inmuebles
- Alta de propiedades con información detallada:
  - Dirección completa (calle, altura, barrio, localidad, código postal)
  - Vinculación con propietario
- Listado de inmuebles con información del dueño

#### 3. Gestión de Inquilinos
- Registro de inquilinos con datos de contacto
- Base de datos centralizada de arrendatarios
- Historial completo en tabla

#### 4. Gestión de Contratos
- Creación de contratos de alquiler
- Vinculación inmueble-inquilino
- Registro de fechas de inicio y fin
- Establecimiento de monto mensual
- Visualización de contratos activos

#### 5. Sistema de Pagos (Caja)
- Registro de cobros de alquiler
- Seguimiento por periodo (mensual)
- Historial completo de transacciones
- Asociación de pagos a contratos específicos

## Tecnologías Utilizadas

- **Framework**: [Reflex](https://reflex.dev/) - Framework Python para aplicaciones web full-stack
- **Base de Datos**: SQLModel (ORM sobre SQLAlchemy)
- **Lenguaje**: Python 3.11+
- **Frontend**: Componentes Reflex (React bajo el capó)

## Estructura del Proyecto

```
gestion_inmuebles_mvp/
├── inmobiliaria/
│   ├── __init__.py
│   ├── inmobiliaria.py          # Punto de entrada y routing
│   ├── state.py                 # Gestión de estado y eventos UI
│   ├── models/                  # Modelos de base de datos
│   │   ├── __init__.py
│   │   ├── propietario.py
│   │   ├── inmueble.py
│   │   ├── inquilino.py
│   │   ├── contrato.py
│   │   └── pago.py
│   ├── services/                # Capa de lógica de negocio
│   │   ├── __init__.py
│   │   ├── validaciones_service.py
│   │   ├── propietario_service.py
│   │   ├── inmueble_service.py
│   │   ├── inquilino_service.py
│   │   ├── contrato_service.py
│   │   └── pago_service.py
│   └── views/                   # Componentes de interfaz
│       ├── __init__.py
│       ├── dashboard.py         # Vista principal con métricas
│       ├── propietarios.py      # Vista gestión propietarios
│       ├── inmuebles.py         # Vista gestión inmuebles
│       ├── inquilinos.py        # Vista gestión inquilinos
│       ├── contratos.py         # Vista gestión contratos
│       └── pagos.py             # Vista registro de pagos
├── .gitignore
├── README.md
├── MEJORAS.md
├── rxconfig.py                  # Configuración de Reflex
└── requirements.txt
```

### Arquitectura

El proyecto sigue una **arquitectura en capas** con clara separación de responsabilidades:

- **`inmobiliaria.py`**: Punto de entrada, definición de rutas y componentes globales (diálogos, mensajes)
- **`state.py`**: Gestión de estado UI y coordinación entre vistas y services
- **`models/`**: Modelos de datos SQLModel con relaciones definidas
- **`services/`**: Capa de lógica de negocio y operaciones de base de datos
  - Validaciones centralizadas
  - Operaciones CRUD por entidad
  - Verificación de constraints y relaciones
- **`views/`**: Componentes de UI reutilizables y aislados por funcionalidad

## Modelos de Datos

### Propietario
- ID (autoincremental)
- Nombre
- Apellido
- DNI
- Email

### Inmueble
- ID
- Calle
- Altura
- Barrio
- Localidad
- Código Postal
- Propietario (relación)

### Inquilino
- ID
- Nombre
- Apellido
- DNI
- Email

### Contrato
- ID
- Inmueble (relación)
- Inquilino (relación)
- Fecha inicio
- Fecha fin
- Monto mensual

### Pago
- ID
- Contrato (relación)
- Periodo
- Fecha de pago
- Monto

## Instalación

### Prerrequisitos
- Python 3.11 o superior (requerido para Reflex)
- pip (gestor de paquetes de Python)

### Pasos

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd gestion_inmuebles_mvp
```

2. Crear entorno virtual (recomendado):
```bash
python -m venv venv
source venv/Scripts/activate  # En Git Bash (Windows)
# o en Linux/Mac: source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Inicializar y migrar la base de datos:
```bash
reflex db init
reflex db migrate
```

## Uso

### Ejecutar la aplicación

```bash
reflex run
```

La aplicación estará disponible en `http://localhost:3000`

### Flujo de Trabajo Típico

1. **Registrar Propietarios**: Ir a la pestaña "Propietarios" y agregar los dueños de inmuebles
2. **Agregar Inmuebles**: En "Inmuebles", registrar las propiedades y asignarles propietario
3. **Registrar Inquilinos**: Dar de alta los potenciales arrendatarios
4. **Crear Contratos**: Vincular un inmueble con un inquilino estableciendo fechas y monto
5. **Registrar Pagos**: En "Pagos (Caja)", registrar cada cobro de alquiler mensual

## Características del Dashboard

El dashboard muestra en tiempo real:
- **Tarjeta Inmuebles**: Total de propiedades gestionadas
- **Tarjeta Contratos Activos**: Número de alquileres vigentes
- **Tarjeta Caja Total**: Suma histórica de todos los pagos registrados
- **Tarjeta Propietarios**: Total de dueños en el sistema

## Interfaz de Usuario

- **Diseño por pestañas**: Navegación clara entre módulos
- **Formularios intuitivos**: Campos organizados con placeholders descriptivos
- **Tablas responsivas**: Visualización limpia de datos
- **Selectores inteligentes**: Dropdowns con información contextual

## Estado Actual (MVP)

### Funcionalidades Implementadas ✓

#### CRUD Completo
- ✅ **Crear** registros en todas las entidades
- ✅ **Leer** y visualizar datos en tablas organizadas
- ✅ **Editar** registros existentes con carga de datos en formularios
- ✅ **Eliminar** con diálogo de confirmación y verificación de constraints

#### Validaciones
- ✅ Validación de formato DNI (7-8 dígitos)
- ✅ Validación de formato email (patrón estándar)
- ✅ Validación de montos (números positivos)
- ✅ Validación de fechas (fecha_fin > fecha_inicio en contratos)
- ✅ Prevención de DNI y email duplicados
- ✅ Validación de campos obligatorios

#### Gestión de Constraints
- ✅ Verificación de relaciones antes de eliminar
- ✅ Mensajes descriptivos de error
- ✅ Protección de integridad referencial:
  - Propietario con inmuebles
  - Inmueble con contratos
  - Inquilino con contratos
  - Contrato con pagos

#### Arquitectura
- ✅ **Arquitectura en capas** (Models, Services, State, Views)
- ✅ **Services layer** con lógica de negocio separada
- ✅ Validaciones centralizadas en `ValidacionesService`
- ✅ CRUD services por cada entidad
- ✅ State enfocado solo en UI
- ✅ Setters explícitos para Reflex 0.9.0+

#### Interfaz de Usuario
- ✅ Dashboard con métricas en tiempo real
- ✅ Formularios con validación en línea
- ✅ Tablas con botones de editar/eliminar
- ✅ Diálogos de confirmación para eliminaciones
- ✅ Mensajes de error contextuales
- ✅ Eager loading para optimizar consultas

### Limitaciones Conocidas
- Sin sistema de búsqueda o filtros en tablas
- Sin autenticación de usuarios
- Sin paginación en listados extensos
- Sin exportación de datos
- Sin reportes generados

### Mejoras Técnicas Implementadas
- ✅ Arquitectura modular completa (models, services, state, views)
- ✅ Separación de responsabilidades (Services Pattern)
- ✅ Validaciones robustas y reutilizables
- ✅ Manejo de errores y constraints
- ✅ Código mantenible y escalable
- ✅ Compatibilidad con Python 3.11+ y Reflex 0.9.0+

## Roadmap de Mejoras

Ver [MEJORAS.md](MEJORAS.md) para el plan detallado de mejoras sugeridas.

Próximas funcionalidades planificadas:
- Sistema de búsqueda y filtros en tablas
- Autenticación y roles de usuario
- Reportes y exportación de datos (PDF, Excel)
- Control de contratos vencidos con notificaciones
- Paginación y ordenamiento en tablas
- Gráficos y estadísticas avanzadas

## Contribuciones

Este es un proyecto en desarrollo activo. Las sugerencias y mejoras son bienvenidas.

## Licencia

[Especificar licencia]

## Contacto

---

**Versión**: 2.0.0 (CRUD Completo + Services Architecture)
**Última actualización**: Diciembre 2025
