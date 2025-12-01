<img src="custom_components/hakboard/icon.png?raw=true" width="200">

# HAKboard

📫 **Contacto:** hakboard.dev@gmail.com  
🌐 **Idioma:** [🇺🇸 English](README.md) | [🇪🇸 Español](README.es.md)

## Introducción
HAKboard integra datos de proyectos, tareas y usuarios desde [Kanboard](https://kanboard.org/), una herramienta de gestión de proyectos Kanban gratuita y de código abierto, dentro de [Home Assistant](https://www.home-assistant.io/), una plataforma de automatización del hogar de código abierto. Almacena datos de proyectos en una colección de entidades de sensor generadas dinámicamente para una fácil integración en automatizaciones y tableros. Se instala y configura exclusivamente a través de la interfaz de usuario de [Home Assistant Community Store (HACS)](https://www.hacs.xyz/) como una integración personalizada.

**Antecedentes**: El objetivo al desarrollar HAKboard fue explorar cómo podría verse una integración personalizada de Home Assistant sin necesidad de escribir código, y hacerlo accesible para usuarios no técnicos. Esto requirió enfocarse en:
- **Experiencia de usuario:** Debe ser fácil de instalar y totalmente configurable desde la interfaz.
- **Documentación:** Los usuarios no deberían tener que revisar el código para entender cómo funciona una integración, y se debe incluir un esquema de datos.
- **Cumplimiento:** Implementar los métodos más recientes y aprobados por HA para crear y gestionar entidades, realizar llamadas a la API, construir la interfaz y generar tarjetas Lovelace nativas.
- **Velocidad:** Aplicar las mejores prácticas de HA para instalación, reconfiguración, llamadas de red y gestión de entidades.


## Características
- Configuración completamente basada en la UI (sin YAML ni código), instalable mediante HACS.
- Incluye tres tarjetas Lovelace preconstruidas: **System Status**, **Users** y **Projects**. (ver [Capturas de pantalla](#screenshots)).
- Se conecta a Kanboard utilizando la API JSON-RPC oficial (compatibilidad con webhooks próximamente).
- Intervalo de sondeo ajustable (mínimo 5 segundos) para actualizaciones casi en tiempo real — úselo con responsabilidad.
- Los filtros de proyectos permiten sincronizar solo los proyectos que desea que aparezcan en HA.
- Soporta múltiples instancias concurrentes de la integración. Esto habilita [blue/green deployment](https://en.wikipedia.org/wiki/Blue%E2%80%93green_deployment).  
- Los Perfiles de Conexión permiten diferentes reglas de sincronización para el mismo servidor de Kanboard  
  *(por ejemplo, los proyectos 1,3–5,7 se actualizan cada 10s mientras que el proyecto 23 se actualiza cada 24h).*
- Creación automática de entidades con detección de colisiones y limpieza de entidades huérfanas.
- Optimizado para rendimiento de red usando [DataUpdateCoordinator](https://developers.home-assistant.io/docs/integration_fetching_data/) de Home Assistant.
- Localización incluida: 🇺🇸 English, 🇪🇸 Español.

## Funcionalidad
En esta versión inicial, se realiza una sincronización unidireccional de los datos de Kanboard hacia Home Assistant, con enlaces directos a los proyectos de Kanboard desde el panel de HA. Se crea una entidad para cada proyecto que proporciona datos agregados sobre tareas, estado de tareas, asignaciones, columnas, etc., ofreciéndote una excelente vista panorámica de tu entorno, además de la posibilidad de crear automatizaciones basadas en estos sensores.

En una versión muy próxima (ver [Hoja de ruta](#roadmap)) se añadirá la creación de entidades para cada tarea y cada persona, y posiblemente más. Queríamos garantizar que el sistema central de generación de entidades fuera totalmente sólido antes de abrirlo a potencialmente miles de nuevas entidades, por lo que consideramos prudente implementar esta funcionalidad de manera gradual.

## ¿Por qué integrar un sistema de gestión de proyectos con Home Assistant?
HAKboard permite que Kanboard sea un participante activo en su hogar inteligente. Esto desbloquea algunos casos de uso evidentes, como desencadenar eventos cuando se alcanzan hitos de software o se actualizan errores críticos. Aunque esto por sí solo abre posibilidades interesantes, se vuelve realmente poderoso cuando se aplica de manera creativa. Otras ideas incluyen:
* Reemplazar aplicaciones de tareas/listas de compras que cada vez empujan funciones básicas hacia planes de pago.
* Compilar boletines del hogar, actualizaciones o incluso notas de lanzamiento de su entorno de hogar inteligente directamente desde las Tareas, luego enviar una notificación push solo a los miembros que hayan suscrito o sean parte de un proyecto/grupo en particular.
* Agregar elementos automáticamente a listas/proyectos dinámicos basados en datos del hogar. Por ejemplo, cuando el filtro o batería de un dispositivo molesto necesita reemplazo, agregarlo automáticamente a una lista de compras y/o carrito en línea, incluyendo la información de modelo/accesorio, crear una tarea en el proyecto 'Home Maintenance' llamada 'Instalar filtros nuevos', asignarla al dueño del dispositivo o proyecto, marcarla como Lista cuando llegue el filtro, notificar al dueño por push, y finalmente marcarla como completada cuando el nuevo sensor esté instalado y en línea con lecturas actualizadas.
* Compartir un tablero de Home Assistant para seguimiento de tareas del hogar (donde las tareas son Tareas de Kanboard) que incorpore sensores del hogar en tiempo real (como lavadora o secadora) junto con la tarea.

Aunque algunos de estos ejemplos están algo extendidos, sirven para ilustrar las posibilidades de un sistema de gestión de proyectos estrechamente integrado con Home Assistant.

## Interesante, pero ¿por qué Kanboard?
Es pequeño, gratuito, rápido (tanto en cliente como servidor), altamente personalizable, soporta branding y temas (incluyendo temas responsivos móviles), plugins, tiene una comunidad activa, un [repositorio](https://github.com/kanboard/kanboard) bien mantenido y una [imagen oficial de Docker](https://hub.docker.com/r/kanboard/kanboard). La imagen Docker no requiere una base de datos por separado ya que incluye SQLite. Tiene configuraciones sensatas y tableros preconfigurados, por lo que está funcionando en minutos, no horas o fines de semana dolorosos.

**Notas**
* Necesita acceso a una instalación existente de Kanboard; HAKboard no instala Kanboard por usted.
* HAKboard no está afiliado con Kanboard, solo pensamos que es genial. 💖

## Capturas de pantalla
<img src="custom_components/hakboard/img/dashboard01.png"><br>
*Descripción general del tablero mostrando estado, usuarios y proyectos. La tarjeta de Estado incluye controles para actualizar la integración o abrir la pantalla de reconfiguración directamente desde el tablero.*  

<img src="custom_components/hakboard/img/status_card_editor.png" width="900"><br>
*Editor de la tarjeta de estado con opciones de personalización.*  

<img src="custom_components/hakboard/img/configuration.png" width="560"><br>
*Pantalla de configuración / reconfiguración.*  

## Estoy convencido, ¿cómo empiezo?
Por favor lea la sección de Documentación más abajo para saber qué esperar después de la instalación.

### Instalación vía HACS (Recomendada)
Las instalaciones con HACS ofrecen notificaciones de actualización, actualizaciones con un clic y soporte para revertir versiones.
1. Inicie sesión en HA y abra HACS
2. Busque `HAKboard` en la tienda comunitaria y selecciónelo
3. Revise las notas y haga clic en el botón `Download` para iniciar la instalación guiada

### Instalación manual
La instalación manual no es recomendada a menos que planee mantenerse al tanto de las actualizaciones.
1. Descargue el contenido del repositorio
2. Extraiga en su directorio `config/custom_components/HAKboard` de HA
3. Reinicie HA
4. Navegue a `Settings / Devices & services / + Add Integration` y busque HAKboard.

## Documentación:
### Instalación
Durante la instalación, debe especificar un Endpoint Kanban (su servidor Kanboard). En este momento también debe especificar un Endpoint ID único. Este ID ficticio se agrega al prefijo de todos los IDs de entidades creadas para asegurar unicidad y hacerlas legibles. Puede ingresar cualquier nombre, pero se recomienda elegir uno breve y fácil de identificar ya que aparecerá en todos los IDs de entidades creadas por HAKboard. Además, debe especificar un filtro de proyectos para gobernar qué proyectos se sincronizarán desde Kanboard hacia HA. El ID de Proyecto de Kanboard también se agrega a los IDs de entidades para unicidad.

### Re-configuración
Para reconfigurar una integración existente, visite `Settings / Devices & services / HAKboard` y haga clic en el ícono `⚙️` en la integración. O simplemente haga clic en el ícono `⚙️` directamente desde la tarjeta de Estado de HAKboard. La reconfiguración le permite cambiar la URL del Endpoint, el API Token, el Filtro de Proyectos y el Intervalo de Sondeo. **No** puede cambiar el Endpoint ID ya que es parte de la clave para generar entidades únicas. Si necesita cambiar el Entity ID, elimine la integración y vuelva a agregarla con un nuevo valor. No se perderán datos si elimina y recrea una integración.

### Integración y Entidades
HAKboard generará automáticamente una colección de entidades de sensor HA para almacenar datos de Kanboard. Se usan sensores porque son un tipo de entidad bien soportado en HA, pueden recibir actualizaciones en tiempo real, almacenar historial y son aliados poderosos en tableros.

Si su entorno `Homelab 2` con una clave de integración `hl2` contiene 10 proyectos y sincroniza solo los proyectos 1–4 y 8, HAKboard creará las siguientes entidades. Los nombres de entidades pueden ser modificados después de la integración sin efectos secundarios; son solo para visualización.

### Entidades de Sistema
Las entidades de sistema proporcionan estadísticas de alto nivel sobre su integración.  

**Entity ID:** *sensor.hakboard_hl2_system_status*: 10 (número de tareas abiertas en todos los proyectos)  
**Name:** *Homelab2 • System Status*
- Attribute: api_endpoint: https://kanboard.homelab2.net/jsonrpc.php
- Attribute: config_entry_id: 01KB959BNGD9PEV0GZAAZM9WTS
- Attribute: display_name: Homelab2
- Attribute: friendly_name: Homelab2 • System Status
- Attribute: icon: mdi:pulse
- Attribute: last_success_timestamp: 2025-11-29T17:49:11.182526-08:00
- Attribute: poll_interval: 5s
- Attribute: project_filter: 1-4
- Attribute: synced_project_count: 4
- Attribute: unit_of_measurement: tasks

### Entidades de Resumen
Las entidades de resumen proporcionan estadísticas de alto nivel para proyectos y usuarios.

**Entity ID:** *sensor.hakboard_hl2_summary_projects_total*: 10 (número total de proyectos en Kanboard)  
**Name:** *Homelab2 • Summary: Projects Total*

**Entity ID:** *sensor.hakboard_hl2_summary_projects_synced*: 6 (número de proyectos sincronizados después de aplicar el filtro de proyectos)  
**Name:** *Homelab2 • Summary: Projects Synced*

**Entity ID:** *sensor.hakboard_hl2_summary_users*: 4 (número total de usuarios en Kanboard)  
**Name:** *Homelab2 • Summary: Users*
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
Las entidades de proyecto proporcionan estadísticas del proyecto.

> ⚠️ **Precaución:** Se creará una entidad de proyecto por *cada* proyecto incluido en el alcance del filtro.  
> Si sincroniza **26,326** proyectos, HAKboard creará **26,326 entidades de proyecto**.

**Entity ID:** *sensor.hakboard_hl2_project_1*: 4 (número de tareas activas en este proyecto)  
**Name:** *Homelab 2 • Project 1: Shopping List*
- Attribute: id: 1 (Kanboard `project_id`)
- Attribute: name: Home Assistant (Kanboard `name`)
- Attribute: identifier: HA (Kanboard `identifier`)
- Attribute: description: The Fitswell Family's Shopping List (Kanboard `description`)
- Attribute: project_url: https://kanboard.homelab2.net/board/1 (Kanboard `url`. Permite acceder al proyecto desde el tablero)
- Attribute: owner: Richard (Derivado de Kanboard `owner_id`)
- Attribute: project_email: richard.fitswell@homelab2.net
- Attribute: last_activity: 2025-11-28T10:24:02 (Kanboard `last_modified` que se actualiza cuando cualquier tarea del proyecto ha sido modificada)
- Attribute: overdue_count: 1 (Derivado de Kanboard `date_due`, `is_active` y `is_overdue`)
- Attribute: Backlog: 12 (Cuenta de tareas asignadas a la columna "Backlog"; metadatos de columnas obtenidos mediante `getColumns`, asignación de tareas mediante el método API `project` de Kanboard. Nota: se creará un atributo por cada columna configurada en un proyecto.)
- Attribute: Open: 3 (Cuenta de tareas asignadas a la columna "Open"; metadatos de columnas obtenidos mediante `getColumns`, asignación de tareas mediante el método API `project` de Kanboard. Nota: se creará un atributo por cada columna configurada en un proyecto.)

Cualquier integración que pueda introducir un número potencialmente ilimitado de entidades generadas dinámicamente es algo delicado. Escenarios de pesadilla incluyen creación masiva no intencional de entidades con posibles sobrescrituras, duplicación de entidades, entidades zombis que reaparecen misteriosamente después de ser eliminadas o entidades inestables que se comportan de manera inconsistente, especialmente después de reinicios de HA. HAKboard fue escrito cuidadosamente para asegurar que todas las entidades creadas estén en sincronía con sus contrapartes en Kanboard y, más importante, bien documentadas. Esto se ilustra aún más con algunos escenarios sobre la eliminación y modificación de entidades y proyectos:

### Escenario 1: Entidad eliminada de Home Assistant
Home Assistant no permite borrar entidades generadas dinámicamente vía la UI ya que están "gestionadas" por la integración HAKboard. Sin embargo, en caso de eliminación por medios no soportados u otros, las entidades se recrearán cuando la integración afectada sea recargada vía `Settings › Integrations › HAKboard › {Instance Name} › ⋮ Menu › Reload` o cuando HA se reinicie. Esto es comportamiento intencional. Si se están recreando entidades que no desea, simplemente modifique sus integraciones para excluir esos proyectos del filtro de proyectos.

### Escenario 2: Proyecto eliminado de Kanboard
Si un proyecto es eliminado en Kanboard, ya no será "visto" por HAKboard y todas las entidades asociadas serán eliminadas automáticamente en la siguiente recarga de la integración / reinicio de HA. Esto se implementó para mantener consistencia entre HA y Kanboard. Si desea cambiar este comportamiento predeterminado, nos encantaría saberlo.

### Escenario 3: Proyecto renombrado en Kanboard
Si un proyecto se renombra en Kanboard, el nombre amigable de la entidad (NO el ID de la entidad) en HA será actualizado la próxima vez que la integración se recargue o cuando HA se reinicie. Por ejemplo: el proyecto 4 llamado 'Video Surveillance' ya está sincronizado vía HAKboard, por lo que la entidad `sensor.hakboard_hl2_project_4` tendrá el nombre `Homelab 2 • Project 4: Video Surveillance`. Si renombra este proyecto en Kanboard a 'Cameras', la próxima vez que HA se reinicie el ID de la entidad permanecerá igual pero el nombre se actualizará a `Homelab 2 • Project 4: Cameras`.

### Escenario 4: Entidad renombrada o eliminada en Home Assistant
Si el Unique ID o el nombre de una entidad se editan en HA, esos cambios persistirán a menos que se reviertan manualmente. Para restablecer el nombre, simplemente elimine el nombre personalizado en la pantalla de edición de la entidad y volverá al nombre predeterminado generado por HAKboard. Para restablecer el ID de la entidad, debe renombrarlo manualmente. Las entidades eliminadas en HA se mantienen en el registro interno (`.storage/core.entity_registry`). Por lo tanto, si elimina la integración y la vuelve a agregar usando el mismo servidor Kanboard y Endpoint ID, las entidades renombradas seguirán estando renombradas en la nueva integración. Esto es comportamiento esperado de HA.

### Escenario 5: Cambios en el alcance del filtro de proyectos
Reducir o aumentar el filtro de proyectos de una integración existente hará que HAKboard aplique esos cambios (y agregue/quite entidades según sea necesario) tan pronto como se presione el botón `Submit` en la pantalla de configuración. Esto se implementó para mantener consistencia entre HA y Kanboard. Si desea cambiar este comportamiento predeterminado, nos encantaría saberlo.

---

## Configuración de la tarjeta
HAKboard incluye tres tarjetas. Vea las [capturas de pantalla](#screenshots) para verlas en el panel.

### Tarjeta de Estado de HAKboard (frontend/hakboard-status-card.js)
Muestra información útil sobre tu integración de HAKboard. Esta es una tarjeta Lovelace personalizada desarrollada específicamente para HAKboard y puede añadirse fácilmente al panel mediante la interfaz de usuario.  
- **USO:** Desde tu dashboard, selecciona el botón `+ Añadir Tarjeta` y elige la tarjeta `HAKboard Status`. Tiene soporte para múltiples endpoints, permite configurar qué elementos se muestran e incluye los botones `🔄️ Actualizar` y `⚙️ Config` que permiten actualizar tus datos de Kanboard o configurar la integración directamente desde el dashboard. Esto es extremadamente útil durante el período de configuración inicial, después del cual pueden ocultarse utilizando las casillas de selección.

### Tarjeta de Usuarios (lovelace_card_users.yaml)
Muestra una lista de todos los usuarios y sus tareas asignadas. Indica Administradores, Usuarios y Gestores de Proyecto mediante iconos. Los elementos de esta tarjeta son entidades clicables que abrirán la vista de entidad de Home Assistant. Esta tarjeta detecta automáticamente cualquier entidad de usuario de HAKboard y la añade a la tarjeta. Consulta `lovelace_card_users.yaml` para ver ejemplos.  
- **USO:** Esta tarjeta está construida con YAML estándar de Lovelace, pero no necesitas editar archivos YAML (¡uf!). La forma más sencilla es pegar el código preconstruido directamente en el editor del panel. Desde tu dashboard de Home Assistant, selecciona `+ Añadir Tarjeta`, elige cualquier tipo de tarjeta, luego selecciona `Mostrar editor de código` y pega el contenido de `lovelace_card_users.yaml`. Detectará automáticamente todas las entidades `hakboard.` relevantes y las mostrará en la tarjeta.
- **NOTA:** Esta tarjeta aún no es una tarjeta Lovelace nativa. Esto fue intencional en la versión inicial para demostrar la potencia de generar dinámicamente el contenido de una tarjeta basándose en criterios flexibles. La tarjeta tiene varias dependencias listadas en la parte superior del archivo.

### Tarjeta de Proyectos (lovelace_card_projects.yaml)
Muestra estadísticas importantes de cada proyecto, incluyendo el número total de tareas, `#️⃣ ID del Proyecto`, `🕑 Última Actividad`, `👤 Propietario del Proyecto`, `⚠️ Tareas Vencidas` y 📊 estadísticas sobre el número de tareas abiertas por columna configurada en el proyecto. Cada entrada es un enlace clicable que te llevará directamente al proyecto en Kanboard.  
- **USO:** Esta tarjeta está construida con YAML estándar de Lovelace, pero no necesitas editar archivos YAML (¡uf!). La forma más sencilla es pegar el código preconstruido directamente en el editor del panel. Desde tu dashboard de Home Assistant, selecciona `+ Añadir Tarjeta`, elige cualquier tipo de tarjeta, luego selecciona `Mostrar editor de código` y pega el contenido de `lovelace_card_projects.yaml`. Detectará automáticamente todas las entidades `hakboard.` relevantes y las mostrará en la tarjeta.
- **NOTA:** Esta tarjeta aún no es una tarjeta Lovelace nativa. Esto fue intencional en la versión inicial para demostrar la potencia de generar dinámicamente el contenido de una tarjeta basándose en criterios flexibles. La tarjeta tiene varias dependencias listadas en la parte superior del archivo.

Las tarjetas YAML de Usuarios y Proyectos utilizan varios excelentes complementos de HACS desarrollados por [@thomasloven](https://github.com/thomasloven).  
**Nota:** Estos complementos son únicamente para fines visuales y no modifican la funcionalidad principal de Home Assistant.

---

## Roadmap:
* `Q1-26` Webhooks para actualizaciones en tiempo real
* `Q4-25` Entidades para cada tarea
* `Q4-25` Etiquetas de Kanboard expuestas como atributos
* `Q1-26` Crear/actualizar tareas de Kanboard desde HA/automatizaciones
* `Q1-26` Tarjetas Lovelace adicionales para estadísticas avanzadas y gráficos
* `Q1-26` Informes agregados para mostrar contexto útil como,  
  *"¿Cuántos problemas de alta prioridad se cerraron este mes que tardaron >20% más del promedio?"*.  
  O mejor aún, divertirse con Home Assistant:  
  *"¿Cuántos problemas se cerraron más rápido que el promedio mientras yo estaba en casa, conectado a mi PC de desarrollo vs mi laptop antigua, con Hall and Oates sonando en Spotify y mi cafetera se ha rellenado más de 3 veces?"*

---

**Licencia:** *MIT – libre para usar, bifurcar, modificar, encurtir, lo que sea — solo mantén el crédito.*
