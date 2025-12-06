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
- **Lenguaje**: Python 3.x
- **Frontend**: Componentes Reflex (React bajo el capó)

## Estructura del Proyecto

```
gestion_inmuebles/
├── inamobiliaria/
│   ├── __init__.py
│   ├── inamobiliaria.py    # Lógica principal y vistas
│   └── models.py            # Modelos de base de datos
├── README.md
└── requirements.txt         # Dependencias del proyecto
```

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
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd gestion_inmuebles
```

2. Crear entorno virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install reflex sqlmodel
```

4. Inicializar la base de datos:
```bash
reflex init
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
- CRUD básico (Create + Read) para todas las entidades
- Dashboard con métricas en tiempo real
- Relaciones entre entidades (propietario-inmueble, contrato-inmueble-inquilino)
- Sistema de carga eager loading para optimizar consultas
- Interfaz de usuario limpia y funcional

### Limitaciones Conocidas
- No incluye funcionalidad de edición de registros
- No permite eliminar registros
- Sin validaciones de datos en formularios
- Sin sistema de búsqueda o filtros
- Sin autenticación de usuarios
- Sin manejo de errores visualizado al usuario

## Roadmap de Mejoras

Ver [MEJORAS.md](MEJORAS.md) para el plan detallado de mejoras sugeridas.

Próximas funcionalidades planificadas:
- Edición y eliminación de registros
- Validación de formularios
- Sistema de notificaciones
- Filtros y búsqueda en tablas
- Control de contratos vencidos
- Reportes y exportación de datos

## Contribuciones

Este es un proyecto en desarrollo activo. Las sugerencias y mejoras son bienvenidas.

## Licencia

[Especificar licencia]

## Contacto

---

**Versión**: 1.0.0 (MVP)
**Última actualización**: Diciembre 2025
