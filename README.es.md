<img src="custom_components/hakboard/icon.png?raw=true" width="200">

# HAKboard

📫 **Contacto:** hakboard.dev@gmail.com  
🌐 **Idioma:** [🇺🇸 English](README.md) | [🇪🇸 Español](README.es.md)

## Introducción
HAKboard integra datos de proyectos, tareas y usuarios desde [Kanboard](https://kanboard.org/), una herramienta gratuita y de código abierto para tableros Kanban, dentro de [Home Assistant](https://www.home-assistant.io/), una plataforma de automatización del hogar de código abierto. Almacena datos de proyectos en una colección de entidades de sensor generadas dinámicamente para facilitar su integración en automatizaciones y paneles.

**Antecedentes:** Mientras desarrollábamos HAKboard queríamos explorar cómo podría verse una integración de Home Assistant de bajo código y, con suerte, hacerla fácil para usuarios no técnicos. Esto exigió enfocarnos en:
- **Experiencia de usuario:** Debe ser fácil de instalar y configurable desde la interfaz.
- **Documentación:** Los usuarios no deberían tener que leer código para entender cómo funciona una integración, y se debe incluir un esquema de datos.
- **Cumplimiento:** Implementar los métodos aprobados por HA más recientes para crear y administrar entidades, realizar llamadas a la API, construir la interfaz y generar tarjetas Lovelace nativas.
- **Velocidad:** Implementar las mejores prácticas de HA para flujos de instalación y reconfiguración, llamadas de red y administración de entidades.

## Funciones
- Configuración guiada por la UI (sin YAML ni código), instalable mediante HACS.
- Incluye tres tarjetas Lovelace preconstruidas: **Estado del Sistema**, **Usuarios** y **Proyectos**. (ver [Capturas de pantalla](#screenshots)).
- Se conecta a Kanboard utilizando la API oficial JSON-RPC (webhooks planificados).
- Intervalo de sondeo ajustable (mínimo 5 segundos) para actualizaciones casi en tiempo real — úsalo con responsabilidad.
- Filtros de proyectos que te permiten sincronizar solo los proyectos deseados en HA.
- Soporte para múltiples instancias simultáneas de la integración. Esto habilita [blue/green deployment](https://en.wikipedia.org/wiki/Blue%E2%80%93green_deployment).  
- Perfiles de Conexión permiten distintas reglas de sincronización para el mismo servidor Kanboard  
  *(por ejemplo, proyectos 1,3–5,7 refrescan cada 10s mientras que el proyecto 23 refresca cada 24h).*
- Creación automática de entidades con detección de colisiones y limpieza de huérfanos.
- Optimizado para rendimiento de red utilizando el [DataUpdateCoordinator](https://developers.home-assistant.io/docs/integration_fetching_data/) de Home Assistant.
- Localización incluida: 🇺🇸 Inglés, 🇪🇸 Español.

## Funcionalidad
Los datos se sincronizan desde Kanboard hacia HA. Se creará una entidad para cada proyecto que proporcione datos agregados de tareas, estado, asignaciones, columnas, etc., ofreciéndote una vista panorámica de tu entorno, además de la capacidad de crear automatizaciones basadas en estos sensores. Una versión muy próxima (ver [Roadmap](#roadmap)) introducirá la creación de entidades para cada tarea y persona, entre otras. Queríamos asegurar que el sistema de generación de entidades fuera totalmente sólido antes de abrirlo a miles de nuevas entidades de tareas, por lo que optamos por liberar esta funcionalidad de forma escalonada.

Hay 3 [tarjetas](#card-configuration) disponibles para el panel. Una tarjeta nativa Lovelace `HAKboard Status Card` (agregar mediante `Panel \ Añadir Tarjeta`), y dos tarjetas YAML que generan dinámicamente contenido filtrando las entidades de HAKboard.  
**Nota:** Las tarjetas YAML requieren la instalación de varios complementos de HACS. Consulta el encabezado de los archivos para más detalles.

## ¿Por qué integrar un sistema de gestión de proyectos con Home Assistant?
HAKboard permite que Kanboard se convierta en un participante activo dentro de tu hogar inteligente. Esto habilita casos de uso obvios, como activar eventos cuando se completan hitos de software o se actualizan bugs críticos. Aunque esto ya ofrece posibilidades interesantes, se vuelve realmente poderoso cuando se usa de manera creativa. Algunas ideas incluyen:
* Reemplazar apps de tareas/listas de compras que cada vez mueven más funciones básicas a planes de pago.
* Compilar boletines del hogar, actualizaciones o incluso notas de “release” de tu entorno inteligente directamente desde las Tareas, y enviar una notificación push solo a miembros suscritos o pertenecientes a un proyecto/grupo específico.
* Agregar automáticamente elementos a listas/proyectos dinámicos basados en datos del hogar. Por ejemplo, cuando el filtro o batería de un dispositivo necesita reemplazo, agregarlo automáticamente a una lista de compras y/o a un carrito automático en línea, incluyendo el modelo/accesorio correcto; crear una tarea en el proyecto “Mantenimiento del Hogar” llamada “Instalar Filtros Nuevos”, asignarla al dueño del dispositivo, marcarla como Lista cuando el filtro llegue, notificar vía push y finalmente marcarla como completada cuando el sensor se actualice con nuevas lecturas.
* Compartir un panel de Home Assistant para seguimiento de tareas domésticas (donde las tareas son Tareas Kanboard) que incorpore sensores en tiempo real (como lavadora o secadora) junto con la tarea.

Aunque algunos ejemplos son extendidos, ilustran las posibilidades de un sistema de gestión de proyectos estrechamente acoplado con Home Assistant.

## Interesante, ¿pero por qué Kanboard?
Es pequeño, gratuito, rápido (cliente y servidor), muy personalizable, soporta temas y branding (incluyendo temas responsivos móviles), plugins y una [imagen Docker oficial](https://hub.docker.com/r/kanboard/kanboard). La imagen Docker no requiere base de datos separada ya que utiliza SQLite. Tiene configuraciones sensatas y tableros preconfigurados, por lo que está funcionando en minutos, no horas o fines de semana dolorosos.

**Notas**
* Necesitas acceso a una instalación existente de Kanboard; HAKboard no instala Kanboard por ti.
* HAKboard no está afiliado con Kanboard, solo creemos que es genial. 💖

## Capturas de pantalla
<img src="custom_components/hakboard/img/dashboard01.png"><br>
*Vista del panel mostrando estado, usuarios y proyectos. Incluye controles para refrescar la integración o abrir la pantalla de reconfiguración directamente desde el panel. Al hacer clic en un usuario se muestra su historial de tareas. Al hacer clic en un proyecto se abre directamente en Kanboard.*  

<img src="custom_components/hakboard/img/status_card_editor.png" width="900"><br>
*Editor de la tarjeta de estado con opciones de personalización. Cada elemento de la tarjeta se puede configurar.*  

<img src="custom_components/hakboard/img/configuration.png" width="560"><br>
*Pantalla de configuración / reconfiguración.*  

## ¡Estoy convencido! ¿Cómo empiezo?

⚠️ **NOTAS IMPORTANTES DE INSTALACIÓN:** HAKboard está actualmente pasando por el proceso oficial de aprobación en HACS. Mientras tanto, sigue estas instrucciones si deseas instalar HAKboard (requiere un servidor Kanboard existente):
- HA > HACS > ⚙️ (arriba a la derecha) > Repositorios Personalizados > Agregar: https://github.com/aktive/hakboard como tipo Integration
- Configura tu instancia Kanboard mediante Ajustes (abajo a la izquierda) > Dispositivos y servicios > Agregar (abajo a la derecha) > Buscar HAKboard
- **NOTA:** Si HAKboard no aparece (ni como integración ni como tarjeta), actualiza el navegador o reinicia HA.

Lee la sección [Documentación](#documentation) para saber qué esperar tras la instalación.

### Instalación mediante HACS (Recomendada)
Las instalaciones mediante HACS ofrecen notificaciones de actualización, actualizaciones con un clic y soporte para revertir versiones.
1. Inicia sesión en HA y abre HACS
2. Busca `HAKboard` en la tienda comunitaria y selecciónalo
3. Revisa las notas y haz clic en `Download` para iniciar la instalación guiada

### Instalación manual
No se recomienda la instalación manual a menos que planees gestionar manualmente las actualizaciones.
1. Descarga el contenido del repositorio
2. Extrae en tu carpeta `config/custom_components/HAKboard`
3. Reinicia HA
4. Navega a `Ajustes / Dispositivos y servicios / + Agregar Integración` y busca HAKboard.

## Documentación:
### Instalación
Durante la instalación debes especificar un Endpoint Kanban (tu servidor Kanboard). También debes especificar una `Instance Key` única. Este identificador ficticio se antepone a todas las entidades creadas para asegurar unicidad y legibilidad. Puedes ingresar cualquier nombre, pero se recomienda elegir uno corto y fácil de reconocer ya que aparecerá en todas las entidades creadas. Además, debes especificar un filtro de proyectos que determinará qué proyectos se sincronizarán desde Kanboard hacia HA. El Project ID de Kanboard también se agrega a las entidades para mantener unicidad.

### Reconfiguración
Para reconfigurar una integración existente, ve a `Ajustes / Dispositivos y servicios / HAKboard` y haz clic en el ícono `⚙️` de la integración. O simplemente haz clic en el ícono `⚙️` directamente desde la tarjeta de estado HAKBoard en el panel. La reconfiguración te permite cambiar el Nombre de la Instancia, URL del Endpoint, Token API, Filtro de Proyectos y el Intervalo de Sondeo. No puedes cambiar la `Instance Key` ya que forma parte de las claves únicas de entidad. Si necesitas cambiarla, elimina la integración y vuelve a agregarla con un nuevo valor. No se perderán datos al hacerlo.

### Integración y Entidades
HAKboard generará automáticamente una colección de entidades de sensor en HA para almacenar los datos de Kanboard. Los sensores son ideales porque son ampliamente soportados por HA, reciben actualizaciones en tiempo real, almacenan historial y funcionan muy bien en paneles.

Si configuras tu instancia `Homelab 2` con una `Instance Key` de `hl2`, HAKboard usará el siguiente esquema de nombres para las entidades creadas:
`sensor.hakboard_{instance_key}_xxx`  
Por ejemplo: `sensor.hakboard_hl2_system_status`

### Entidades del Sistema
Las entidades del sistema muestran estadísticas de alto nivel sobre tu integración.

**Entity ID:** *sensor.hakboard_hl2_system_status*: 10 (número de tareas abiertas en todos los proyectos)  
- Attribute: api_endpoint: https://kanboard.homelab2.net/jsonrpc.php
- Attribute: config_entry_id: 01KB959BNGD9PEV0GZAAZM9WTS
- Attribute: display_name: Homelab 2
- Attribute: friendly_name: Homelab 2 • System Status
- Attribute: icon: mdi:pulse
- Attribute: last_success_timestamp: 2025-11-29T17:49:11.182526-08:00
- Attribute: poll_interval: 5s
- Attribute: project_filter: 1-4
- Attribute: synced_project_count: 4
- Attribute: unit_of_measurement: tasks

### Entidades de Resumen
Muestran estadísticas globales de proyectos y usuarios.

**Entity ID:** *sensor.hakboard_hl2_summary_projects_total*: 10 (número total de proyectos en Kanboard)  
- Attribute: name: *Homelab 2 • Summary: Projects Total*

**Entity ID:** *sensor.hakboard_hl2_summary_projects_synced*: 6 (proyectos sincronizados tras aplicar el filtro)  
- Attribute: name: *Homelab 2 • Summary: Projects Synced*

**Entity ID:** *sensor.hakboard_hl2_summary_users*: 4 (número total de usuarios en Kanboard)  
- Attribute: name: *Homelab 2 • Summary: Users*
- Attribute: active_count: 4
- Attribute: admin_count: 2
- Attribute: user_list:
  - name: Admin  
    role: app-admin  
    open_tasks: 18
  - name: Chad  
    role: app-manager  
    open_tasks: 1
  - name: Dean  
    role: app-admin  
    open_tasks: 6
  - name: Megan  
    role: app-user  
    open_tasks: 4

### Entidades de Proyecto
Estas entidades proporcionan estadísticas detalladas del proyecto.

> ⚠️ **Precaución:** Se creará una entidad por *cada* proyecto incluido en el filtro.  
> Si sincronizas **26,326** proyectos, HAKboard creará **26,326 entidades**.

**Entity ID:** *sensor.hakboard_hl2_project_1*: 4 (tareas activas en este proyecto)  
- Attribute: name: Shopping List
- Attribute: id: 1 (Kanboard `project_id`.)
- Attribute: friendly_name: Homelab 2 • Project 1: Shopping List (Kanboard `name`.)
- Attribute: identifier: HA (Kanboard `identifier`.)
- Attribute: description: The Fitswell Family's Shopping List (Kanboard `description`.)
- Attribute: project_url: https://kanboard.homelab2.net/board/1 (URL que permite abrir el proyecto desde el panel.)
- Attribute: owner: Richard (Derivado de `owner_id`.)
- Attribute: project_email: richard.fitswell@homelab2.net
- Attribute: last_activity: 2025-11-28T10:24:02 (última modificación en cualquier tarea del proyecto.)
- Attribute: overdue_count: 1 (tareas vencidas.)
- Attribute: Backlog: 12 (Tareas asignadas a la columna “Backlog”.)
- Attribute: Open: 3 (Tareas asignadas a la columna “Open”.)

---

Cualquier integración que pueda generar un número ilimitado de entidades dinámicas puede ser aterradora. Escenarios de pesadilla incluyen creación masiva accidental de entidades, duplicados, entidades zombis que reaparecen tras eliminarlas, o entidades inestables tras reinicios de HA. HAKboard fue diseñado cuidadosamente para asegurar que todas las entidades estén sincronizadas con Kanboard y, sobre todo, para documentarlo correctamente. Algunos escenarios:

### Escenario 1: Entidad eliminada desde Home Assistant
HA no permite eliminar entidades gestionadas por integraciones vía la UI. Si una entidad se elimina por métodos no soportados, será recreada al recargar la integración o reiniciar HA. Si esto ocurre con entidades no deseadas, ajusta el filtro de proyectos.

### Escenario 2: Proyecto eliminado en Kanboard
Si un proyecto desaparece de Kanboard, todas las entidades asociadas serán eliminadas automáticamente al recargar la integración o reiniciar HA.

### Escenario 3: Proyecto renombrado en Kanboard
Renombrar un proyecto en Kanboard actualizará el nombre amigable de la entidad en HA (no el ID) tras recargar la integración o reiniciar HA.

### Escenario 4: Entidad renombrada o eliminada en HA
Los cambios manuales a los nombres o IDs de entidad persistirán. Para restaurar valores originales, edita o restablece manualmente. HA conserva entidades eliminadas en `.storage/core.entity_registry`.

### Escenario 5: Cambio en el filtro de proyectos
Cambiar el filtro agrega o elimina entidades inmediatamente al presionar `Submit`, manteniendo sincronización estricta entre HA y Kanboard.

## Configuración de Tarjetas
Tres tarjetas vienen incluidas en HAKboard. Ver [Capturas de pantalla](#screenshots).

### Tarjeta de Estado HAKBoard (frontend/hakboard-status-card.js)
Muestra información útil sobre tu integración HAKboard. Es una tarjeta Lovelace nativa desarrollada específicamente para HAKboard.
- **USO:** Desde tu panel, selecciona `+ Añadir Tarjeta` y elige `HAKboard Status`. Soporta múltiples endpoints, permite configurar elementos visibles e incluye botones para `🔄️ Refrescar` y `⚙️ Configurar`.

### Tarjeta de Usuarios (lovelace_card_users.yaml)
Muestra una lista de usuarios y sus tareas asignadas. Cada ítem es clicable y abre la vista de entidad en HA.
- **USO:** Copia el YAML directamente en el editor de código de cualquier tarjeta.
- **NOTA:** No es aún una tarjeta Lovelace nativa. Tiene dependencias listadas en el encabezado.

### Tarjeta de Proyectos (lovelace_card_projects.yaml)
Muestra estadísticas clave de cada proyecto.
- **USO:** Igual que la tarjeta de Usuarios.
- **NOTA:** También depende de complementos HACS.

---

## Roadmap:
* `Q4-25` Implementar verificación SSL configurable para la API de Kanboard  
* `Q1-26` Webhooks para actualizaciones en tiempo real  
* `Q4-25` Entidades por tarea  
* `Q4-25` Etiquetas de Kanboard como atributos  
* `Q1-26` Crear/actualizar tareas desde HA  
* `Q1-26` Tarjetas Lovelace avanzadas para estadísticas y gráficas  
* `Q1-26` Informes agregados como: *“¿Cuántos problemas de alta prioridad se cerraron este mes que tardaron >20% más de lo promedio?”*  
  O incluso:  
  *“¿Cuántos problemas se resolvieron más rápido de lo normal mientras yo estaba en casa, usando mi PC de desarrollo vs mi laptop vieja, escuchando Hall & Oates, y con mi cafetera rellenada más de 3 veces?”*

---

**Licencia:** *MIT – úsalo libremente, fórcalo, modifícalo, encurtido opcional — solo mantén atribución.*
