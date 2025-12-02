<img src="custom_components/hakboard/icon.png?raw=true" width="200">

# HAKboard

📫 **Contacto:** hakboard.dev@gmail.com
🌐 **Idioma:** [🇺🇸 English](README.md) | [🇪🇸 Español](README.es.md)

## Tabla de Contenido

- [Introducción](#introducción)
- [Funciones](#funciones)
- [Funcionalidad](#funcionalidad)
- [¿Por qué integrar un sistema de gestión de proyectos con Home Assistant?](#por-qué-integrar-un-sistema-de-gestión-de-proyectos-con-home-assistant)
- [¿Por qué Kanboard?](#por-qué-kanboard)
- [Capturas de Pantalla](#capturas-de-pantalla)
- [¿Cómo empiezo?](#cómo-empiezo)
  - [Instalación mediante HACS (Recomendada)](#instalación-mediante-hacs-recomendada)
  - [Instalación manual](#instalación-manual)
- [Documentación](#documentación)
  - [Instalación](#instalación)
  - [Reconfiguración](#reconfiguración)
  - [Integración y Entidades](#integración-y-entidades)
  - [Configuración de Tarjetas](#configuración-de-tarjetas)
- [Roadmap](#roadmap)

---

## Introducción
HAKboard integra datos de proyectos, tareas y usuarios desde [Kanboard](https://kanboard.org/), una herramienta gratuita y de código abierto para gestión de proyectos Kanban, dentro de [Home Assistant](https://www.home-assistant.io/), una plataforma de automatización del hogar de código abierto. Almacena datos de proyectos en una colección de entidades de sensor generadas dinámicamente para facilitar su integración en automatizaciones y paneles.

**Antecedentes**: Mientras desarrollábamos HAKboard queríamos explorar cómo podría verse una integración de Home Assistant de bajo código y, con suerte, hacerla fácil para usuarios no técnicos. Esto exigió enfocarnos en:
- **Experiencia de usuario:** Debe ser fácil de instalar y configurable desde la interfaz
- **Documentación:** Los usuarios no deberían tener que leer código para entender cómo funciona una integración, y se debe incluir un esquema de datos.
- **Cumplimiento:** Implementar los métodos más recientes aprobados por HA para crear y administrar entidades, realizar llamadas a la API, construir la interfaz y generar tarjetas Lovelace nativas.
- **Velocidad:** Implementar las mejores prácticas de HA para flujos de instalación y reconfiguración, llamadas de red y administración de entidades.

## Funciones
- Configuración guiada por la UI (sin YAML ni código), instalable mediante HACS.
- Incluye tres tarjetas Lovelace preconstruidas: **Estado del Sistema**, **Usuarios** y **Proyectos**. (ver [Capturas de Pantalla](#capturas-de-pantalla)).
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
HAKboard obtiene datos de Kanboard hacia HA en un horario configurable. Crea entidades para datos de resumen (total de proyectos, total de usuarios, etc.) y una entidad para cada proyecto que proporciona datos agregados de tareas, estado, asignaciones, columnas, etc., ofreciéndote una vista panorámica de tu entorno, además de la capacidad de crear automatizaciones mediante los datos del sensor. Una versión muy próxima (ver [Roadmap](#roadmap)) introducirá la creación de entidades para cada tarea y persona, entre otras. Queríamos asegurar que el sistema de generación de entidades fuera totalmente sólido antes de abrirlo a miles de nuevas entidades de tareas, por lo que optamos por liberar esta funcionalidad de forma escalonada.

Hay 3 [tarjetas](#configuración-de-tarjetas) disponibles para el panel. Una tarjeta nativa Lovelace `HAKboard Status Card` (agregar mediante `Panel > Añadir Tarjeta`), y dos tarjetas YAML que generan dinámicamente contenido filtrando las entidades de HAKboard. **Nota** Las tarjetas YAML requieren la instalación de varios complementos de HACS. Consulta el encabezado de los archivos para más detalles.

## ¿Por qué integrar un sistema de gestión de proyectos con Home Assistant?
HAKboard permite que Kanboard se convierta en un participante activo dentro de tu hogar inteligente. Esto habilita casos de uso obvios, como activar eventos cuando se completan hitos de software o se actualizan bugs críticos. Aunque esto ya ofrece posibilidades interesantes, se vuelve realmente poderoso cuando se usa de manera creativa. Algunas ideas incluyen:
* Reemplazar apps de tareas/listas de compras que cada vez mueven más funciones básicas a planes de pago.
* Compilar boletines del hogar, actualizaciones o incluso notas de "release" de tu entorno inteligente directamente desde las Tareas, y enviar una notificación push solo a miembros suscritos o pertenecientes a un proyecto/grupo específico.
* Agregar automáticamente elementos a listas/proyectos dinámicos basados en datos del hogar. Por ejemplo, cuando el filtro o batería de un dispositivo necesita reemplazo, agregarlo automáticamente a una lista de compras y/o a un carrito automático en línea, incluyendo el modelo/accesorio correcto; crear una tarea en el proyecto "Mantenimiento del Hogar" llamada "Instalar Filtros Nuevos", asignarla al dueño del dispositivo, marcarla como Lista cuando el filtro llegue, notificar vía push y finalmente marcarla como completada cuando el sensor se actualice con nuevas lecturas.
* Compartir un panel de Home Assistant para seguimiento de tareas domésticas (donde las tareas son Tareas Kanboard) que incorpore sensores en tiempo real (como lavadora o secadora) junto con la tarea.

Aunque algunos de estos ejemplos son extensos y sobre-gestionados, sirven para ilustrar las posibilidades de un sistema de gestión de proyectos estrechamente acoplado con Home Assistant.

## ¿Por qué Kanboard?
Es pequeño, gratuito, rápido (tanto cliente como servidor), altamente personalizable, soporta branding y temas (incluyendo temas responsivos para móvil), plugins y una [imagen Docker oficial](https://hub.docker.com/r/kanboard/kanboard). La imagen Docker no requiere base de datos separada ya que incluye SQLite. Tiene configuraciones sensatas y tableros preconfigurados, por lo que está funcionando en minutos, no horas o fines de semana dolorosos.

**Notas**
* Necesitas acceso a una instalación existente de Kanboard; HAKboard no instala Kanboard por ti.
* HAKboard no está afiliado con Kanboard, solo creemos que es genial. 💖

## Capturas de Pantalla
<img src="custom_components/hakboard/img/dashboard01.png"><br>
*Vista del panel mostrando estado, usuarios y proyectos. Incluye controles para refrescar la integración o ir a la pantalla de reconfiguración directamente desde el Panel. Al hacer clic en un usuario se muestra su tarjeta de historial de entidad de HA y su historial de tareas activas. Al hacer clic en un proyecto se abre directamente en Kanboard.*

<img src="custom_components/hakboard/img/status_card_editor.png" width="900"><br>
*Editor de la tarjeta de estado con opciones de personalización. Cada elemento de la tarjeta se puede configurar.*

<img src="custom_components/hakboard/img/configuration.png" width="560"><br>
*Pantalla de configuración / reconfiguración.*

## ¿Cómo empiezo?

⚠️ **NOTAS IMPORTANTES DE INSTALACIÓN:** HAKboard está actualmente pasando por el proceso oficial de aprobación en HACS. Mientras tanto, sigue estas instrucciones si deseas instalar HAKboard (requiere un servidor Kanboard existente):
- HA > HACS > ⚙️ (arriba a la derecha) > Repositorios Personalizados > Agregar: https://github.com/aktive/hakboard como tipo Integration
- Configura tu instancia Kanboard mediante Ajustes (abajo a la izquierda) > Dispositivos y servicios > Agregar (abajo a la derecha) > Buscar HAKboard
- **NOTA:** Si HAKboard no aparece (ni como integración ni como tarjeta del panel), actualiza el navegador o reinicia HA.

Por favor lee la sección [Documentación](#documentación) a continuación para saber qué esperar después de la instalación.

### Instalación mediante HACS (Recomendada)
Las instalaciones mediante HACS ofrecen notificaciones de actualización, actualizaciones con un clic y soporte para revertir versiones.
1. Inicia sesión en HA y abre HACS
2. Busca `HAKboard` en la tienda comunitaria y selecciónalo
3. Revisa las notas y haz clic en el botón `Download` para iniciar la instalación guiada

### Instalación manual
No se recomienda la instalación manual a menos que planees gestionar manualmente las actualizaciones.
1. Descarga el contenido del repositorio
2. Extrae en tu directorio `config/custom_components/HAKboard` de HA
3. Reinicia HA
4. Navega a `Ajustes / Dispositivos y servicios / + Agregar Integración` y busca HAKboard.

## Documentación
### Instalación
Durante la instalación, debes especificar un Endpoint Kanban (tu servidor Kanboard). También debes especificar una `Instance Key` única. Este identificador ficticio se antepone a todos los IDs de entidad creados para asegurar unicidad y hacerlos legibles. Puedes ingresar cualquier nombre que desees, pero se recomienda elegir un nombre corto que puedas identificar rápidamente ya que aparecerá en todos los IDs de entidad creados por HAKboard. Además, debes especificar un filtro de proyectos para determinar qué proyectos se sincronizarán desde Kanboard hacia HA. El Project ID de Kanboard también se agrega a los IDs de entidad para unicidad.

### Reconfiguración
Para reconfigurar una integración existente, visita la pantalla `Ajustes / Dispositivos y servicios / HAKboard` y haz clic en el ícono `⚙️` de la integración. ¡O simplemente haz clic en el ícono `⚙️` directamente desde la Tarjeta de Estado HAKBoard en el panel! La reconfiguración te permite cambiar el Nombre de Instancia, URL del Endpoint, Token API, Filtro de Proyectos e Intervalo de Sondeo. No puedes cambiar la `Instance Key` ya que se usa como parte de la clave para generación única de entidades. Si necesitas cambiar la `Instance Key`, elimina la integración y vuelve a agregarla con un nuevo valor. No se perderán datos si eliminas y recreas una integración.

### Integración y Entidades
HAKboard generará automáticamente una colección de entidades de sensor en HA para almacenar datos de Kanboard. Los sensores se usan porque son un tipo de entidad bien soportado en HA, pueden recibir actualizaciones en tiempo real, almacenan historial, y son poderosos aliados del panel.

Si configuras tu instancia `Homelab 2` con una `Instance Key` de `hl2`, HAKboard usará el siguiente esquema de nombres para las entidades recién creadas:
`sensor.hakboard_{instance_key}_xxx  `
Por ejemplo: `sensor.hakboard_hl2_system_status`

Por favor consulta [docs/ENTITIES.md](docs/ENTITIES.md) para una lista detallada de entidades.

Cualquier integración que amenace con introducir entidades generadas dinámicamente potencialmente ilimitadas es aterradora. Escenarios de pesadilla incluyen creación masiva accidental de entidades con posibles sobrescrituras, duplicación de entidades, entidades zombis que mágicamente reaparecen después de eliminarlas, o entidades inestables que se comportan inconsistentemente, especialmente tras reinicios de HA. HAKboard fue escrito cuidadosamente para asegurar que todas las entidades creadas estén en sincronización estricta con sus contrapartes en Kanboard, y lo más importante, bien documentadas. Esto se destaca con algunos escenarios sobre la eliminación y modificación de entidades y proyectos:

#### Escenario 1: Entidad eliminada desde Home Assistant
Home Assistant no te permite eliminar las entidades generadas dinámicamente mediante la UI ya que son 'administradas' por la integración HAKboard. Sin embargo, en caso de eliminación de entidad por medios no soportados u otros, las entidades serán recreadas cuando la integración HAKboard afectada se recargue mediante `Ajustes › Integraciones › HAKboard › {Nombre de Instancia} › Menú ⋮ › Recargar` o cuando HA reinicie. Este es el comportamiento previsto. Si se están recreando entidades que no deseas, simplemente modifica tu(s) integración(es) para excluir los proyectos no deseados del filtro de proyectos.

#### Escenario 2: Proyecto eliminado de Kanboard
Si un proyecto se elimina de Kanboard, ya no es 'visto' por HAKboard y todas las entidades asociadas serán eliminadas automáticamente en la próxima recarga de integración/reinicio de HA. Esto fue implementado intencionalmente para mantener estado entre HA y Kanboard, sin embargo si deseas cambiar este comportamiento predeterminado nos gustaría saber de ti.

#### Escenario 3: Proyecto renombrado en Kanboard
Si un proyecto se renombra en Kanboard, el nombre amigable de la entidad del proyecto (NO el ID de entidad) en HA será renombrado la próxima vez que la integración se recargue o cuando HA reinicie. Por ejemplo, el proyecto 4 de Kanboard llamado 'Video Surveillance' ya está sincronizado mediante HAKboard, y por lo tanto la siguiente entidad de proyecto habrá sido creada automáticamente: `sensor.hakboard_hl2_project_4` con el nombre `Homelab 2 • Project 4: Video Surveillance`. Si renombras este proyecto en Kanboard a 'Cameras', la próxima vez que HA inicie o la integración se recargue, el ID de entidad permanecerá sin cambios pero el atributo `name` se actualizará a `Homelab 2 • Project 4: Cameras`.

#### Escenario 4: Entidad renombrada o eliminada en Home Assistant
Si el ID único o nombre de una entidad se editan en HA, esos cambios persistirán a menos que se renombren manualmente de vuelta a su nombre original. Para restablecer el nombre, simplemente elimina el nombre personalizado desde la pantalla de edición de entidad y revertirá al nombre predeterminado generado por HAKboard. Para restablecer el ID de entidad, debes renombrarlo manualmente de vuelta a su estado original. Las entidades eliminadas de HA se retienen en el registro de entidades de HA (`.storage/core.entity_registry`). Entonces si eliminas la integración y luego la vuelves a agregar especificando el mismo servidor Kanboard e ID de endpoint, las entidades renombradas seguirán renombradas en la nueva integración. Este es el comportamiento esperado de HA.

#### Escenario 5: Cambio en el alcance del filtro de proyectos
Reducir o aumentar el filtro de proyectos de una integración existente causará que HAKboard aplique esos cambios (y agregue/elimine entidades según sea necesario) tan pronto como se haga clic en el botón `Submit` en la pantalla de configuración. Esto fue implementado intencionalmente para mantener estado entre HA y Kanboard, sin embargo si deseas cambiar este comportamiento predeterminado nos gustaría saber de ti.

### Configuración de Tarjetas
Tres tarjetas están incluidas con HAKboard. Ver [Capturas de Pantalla](#capturas-de-pantalla) para verlas en el panel.

#### Tarjeta de Estado HAKBoard (frontend/hakboard-status-card.js)
Muestra información útil sobre tu integración HAKboard. Esta es una tarjeta Lovelace nativa que puede agregarse fácilmente a tu panel mediante la UI.
- **USO:** Desde tu panel, selecciona el botón `+ Añadir Tarjeta` y elige la tarjeta `HAKboard Status`. Tiene soporte multi-endpoint, permite al usuario configurar qué elementos se muestran, e incluye botones `🔗 Link`, `🔄️ Refresh` y `⚙️ Config` que te permiten enlazar directamente a tu instancia Kanboard (o configurar una URL personalizada), forzar una sincronización, o configurar la integración. Los botones son especialmente útiles durante el período de configuración inicial, después del cual pueden ocultarse usando las casillas de verificación.

#### Tarjeta de Usuarios (lovelace_card_users.yaml)
**NOTA:** Esta no es una tarjeta Lovelace nativa, y en su lugar se proporciona en formato `.yaml` con fines educativos ya que demuestra cómo realizar agrupación/ordenamiento por instancia Kanboard y conteos de tareas. No se requiere edición de YAML, está lista para pegarse tal cual.
Muestra una lista de todos los usuarios y sus tareas asignadas totales. Denota Admins, Usuarios y Gerentes de Proyecto usando íconos. Los elementos en esta tarjeta son entidades clicables que abrirán la vista de Entidad de HA. Esta tarjeta busca automáticamente cualquier entidad de usuario HAKboard y las agrega a la tarjeta. Por favor revisa `lovelace_card_users.yaml` para ejemplos.
- **USO:** Desde tu panel de HA, selecciona `Editar` (arriba a la derecha), `+ Añadir Tarjeta` (abajo a la derecha), elige cualquier tipo de tarjeta luego selecciona `Mostrar editor de código` (abajo a la izquierda) y pega el contenido de `lovelace_card_users.yaml`. Detectará automáticamente todas las entidades `hakboard.` de usuario relevantes y las mostrará en la tarjeta.

#### Tarjeta de Proyectos (lovelace_card_projects.yaml)
**NOTA:** Esta no es una tarjeta Lovelace nativa, y en su lugar se proporciona en formato `.yaml` con fines educativos ya que demuestra cómo realizar agrupación/ordenamiento por instancia Kanboard y conteos de tareas. No se requiere edición de YAML, está lista para pegarse tal cual.
Muestra estadísticas vitales para cada proyecto, incluyendo el número total de tareas, `#️⃣ ID de Proyecto`, `🕑 Última Actividad`, `👤 Dueño del Proyecto`, `⚠️ Tareas Vencidas` y 📊 estadísticas del número de tareas abiertas para cada columna configurada en el proyecto. Cada entrada es un enlace clicable que te llevará directamente al proyecto en Kanboard.
- **USO:** Desde tu panel de HA, selecciona `+ Añadir Tarjeta`, elige cualquier tipo de tarjeta luego selecciona `Mostrar editor de código` (abajo a la izquierda) y pega el contenido de `lovelace_card_projects.yaml`. Detectará automáticamente todas las entidades `hakboard.` de proyecto relevantes y las mostrará en la tarjeta.

Las tarjetas YAML de Usuarios y Proyectos usan varios excelentes addons de HACS desarrollados por [@thomasloven](https://github.com/thomasloven).
**Nota:** Estos addons son puramente para propósitos de visualización y no alteran la funcionalidad central de tu Home Assistant.

---

## Roadmap:
* `Q4-25` `HECHO` Implementar verificación SSL configurable para la API de Kanboard (verify_ssl actualmente desactivado para lanzamiento MVP)
* `Q1-26` Webhooks para actualizaciones en tiempo real
* `Q4-25` Entidades para cada tarea
* `Q4-25` Etiquetas de Kanboard expuestas como atributos
* `Q1-26` Crear/actualizar tareas de Kanboard desde HA/automatizaciones
* `Q1-26` Tarjetas de plantilla Lovelace adicionales para estadísticas avanzadas y gráficos
* `Q1-26` Estadísticas de reportes agregados para habilitar contexto útil como, *"¿Cuántos problemas de alta prioridad se cerraron este mes que tomaron >20% más que el promedio?"*. O mejor aún, ¡sé creativo con Home Assistant! *"¿Cuántos problemas se cerraron más rápido que el promedio mientras yo estaba en casa, conectado a mi PC de desarrollo vs mi laptop arcaica, mientras Hall and Oates sonaba en Spotify, mientras mi cafetera se rellenó más de 3 veces?"*

---

**Licencia:** *MIT – libre para usar, forkear, remezclar, encurtir, lo que sea - solo mantén el crédito.*
