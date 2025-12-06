# Plan de Mejoras - Sistema de Gestión Inmobiliaria

Resumen ejecutivo de mejoras sugeridas para evolucionar el MVP actual hacia un sistema robusto y escalable.

## Prioridad Alta (Críticas)

### 1. Validación de Datos
**Impacto**: Alto | **Esfuerzo**: Medio

- Validar formato y unicidad de DNI
- Validar formato de email
- Validar montos (números positivos)
- Validar fechas (fecha_fin > fecha_inicio en contratos)
- Prevenir datos duplicados

**Beneficio**: Integridad de datos, prevención de errores

---

### 2. Manejo de Errores y Feedback
**Impacto**: Alto | **Esfuerzo**: Bajo

- Implementar try-catch en operaciones de base de datos
- Agregar notificaciones/toasts de éxito/error
- Mensajes claros cuando fallan operaciones
- Indicadores de carga durante operaciones

**Beneficio**: Mejor experiencia de usuario, debugging más fácil

---

### 3. CRUD Completo
**Impacto**: Alto | **Esfuerzo**: Medio

**Faltante**:
- **Update**: Editar propietarios, inmuebles, inquilinos, contratos
- **Delete**: Eliminar registros (con confirmación)

**Beneficio**: Funcionalidad completa, gestión real de datos

---

### 4. Reglas de Negocio
**Impacto**: Alto | **Esfuerzo**: Medio

- Validar que un inmueble no tenga contratos solapados
- Marcar contratos como "activos" o "vencidos" según fecha
- Verificar coherencia entre monto de contrato y pago
- Prevenir eliminación de propietarios con inmuebles activos

**Beneficio**: Lógica de negocio consistente

---

## Prioridad Media (Importantes)

### 5. Refactorización de Código
**Impacto**: Medio | **Esfuerzo**: Alto

**Acciones**:
- Dividir `State` en estados modulares por entidad
- Extraer lógica de negocio a servicios (`services/`)
- Crear componentes reutilizables (FormularioPersona)
- Separar líneas largas (78-79, 91, 203-237)
- Crear helpers para formateo de moneda

**Beneficio**: Mantenibilidad, escalabilidad, código limpio

---

### 6. Búsqueda y Filtros
**Impacto**: Medio | **Esfuerzo**: Medio

- Buscador en tablas de propietarios/inquilinos
- Filtros por propietario en inmuebles
- Filtros por estado en contratos (activos/vencidos)
- Filtros por periodo en pagos
- Ordenamiento por columnas

**Beneficio**: Usabilidad con grandes volúmenes de datos

---

### 7. Mejoras en Dashboard
**Impacto**: Medio | **Esfuerzo**: Medio

**Agregar**:
- Contratos próximos a vencer (30 días)
- Pagos pendientes del mes actual
- Gráfico de recaudación mensual/anual
- Lista de inquilinos morosos
- Inmuebles disponibles vs ocupados

**Beneficio**: Visibilidad de información crítica

---

### 8. Optimización de Performance
**Impacto**: Medio | **Esfuerzo**: Bajo-Medio

- Implementar paginación en tablas
- Lazy loading de datos
- Caché de estadísticas del dashboard
- Optimizar recálculo solo cuando cambian datos relevantes

**Beneficio**: Escalabilidad con muchos registros

---

## Prioridad Baja (Deseables)

### 9. Sistema de Autenticación
**Impacto**: Bajo (MVP) / Alto (Producción) | **Esfuerzo**: Alto

- Login de usuarios
- Roles (admin, operador, solo lectura)
- Permisos por módulo
- Auditoría de cambios

**Beneficio**: Seguridad, trazabilidad

---

### 10. Reportes y Exportación
**Impacto**: Bajo | **Esfuerzo**: Medio

- Exportar a Excel/CSV
- Reporte de pagos por periodo
- Estado de cuenta por inmueble
- Reporte de contratos vencidos

**Beneficio**: Análisis externo, contabilidad

---

### 11. Funcionalidades Avanzadas
**Impacto**: Bajo | **Esfuerzo**: Alto

- Sistema de notificaciones (contratos por vencer)
- Carga masiva de datos (importación CSV)
- Historial de cambios (auditoría)
- Gestión de gastos por inmueble
- Cálculo automático de comisiones

**Beneficio**: Automatización, profesionalización

---

### 12. Mejoras UX/UI
**Impacto**: Bajo | **Esfuerzo**: Bajo-Medio

- Confirmaciones antes de acciones importantes
- Tooltips explicativos
- Modo oscuro
- Diseño responsivo para móviles
- Atajos de teclado

**Beneficio**: Mejor experiencia de usuario

---

## Detalles Técnicos Puntuales

### Código que Requiere Refactorización

#### Problema: División de strings frágil
```python
# Líneas 87, 109, 110, 124
id_dueno = int(self.inm_propietario_select.split(" - ")[0])
```
**Solución**: Pasar IDs directamente en el value del select, no en texto visible

---

#### Problema: Múltiples operaciones en una línea
```python
# Línea 78-79
session.add(nuevo); session.commit(); session.refresh(nuevo)
self.cargar_datos(); self.form_prop_nombre = ""; ...
```
**Solución**: Separar en líneas individuales para mejor lectura

---

#### Problema: Reseteo incompleto de campos
```python
# Línea 91 - falta limpiar inm_localidad e inm_cp
```
**Solución**: Agregar todos los campos al reseteo

---

#### Problema: Componentes muy largos
```python
# Líneas 203-206, 214-218, 224-226
```
**Solución**: Extraer a componentes separados con mejor formato

---

## Estrategia de Implementación Sugerida

### Fase 1: Estabilización (2-3 semanas)
1. Validación de datos
2. Manejo de errores
3. CRUD completo
4. Reglas de negocio básicas

### Fase 2: Usabilidad (1-2 semanas)
5. Búsqueda y filtros
6. Mejoras en Dashboard
7. Mejoras UX/UI

### Fase 3: Optimización (1-2 semanas)
8. Refactorización de código
9. Optimización de performance

### Fase 4: Profesionalización (2-4 semanas)
10. Sistema de autenticación
11. Reportes y exportación
12. Funcionalidades avanzadas

---

## Métricas de Éxito

- **Cobertura de tests**: > 70%
- **Tiempo de respuesta**: < 500ms en operaciones CRUD
- **Validaciones**: 100% de campos críticos validados
- **Bugs reportados**: Reducción del 80% post-refactorización
- **Satisfacción del usuario**: Encuestas > 4/5

---

## Notas Importantes

- El código actual es **funcional y bien estructurado** para un MVP
- Las mejoras son **incrementales**, no requieren reescritura total
- Priorizar según necesidades reales de usuarios
- Mantener simplicidad: evitar over-engineering

---

**Documento creado**: Diciembre 2025
**Versión base**: 1.0.0 MVP
