# Control Horario PWA - Práctica 2 (DISM)
## Sistema Unificado de Registro Horario y Gestión Empresarial

Proyecto correspondiente a la **Entrega 2 de DISM (Desarrollo de Interfaces para Sistemas Móviles)**.

Se ha diseñado e implementado una solución integral basada en una **Progressive Web App (PWA)** desarrollada con **Ionic Framework** y **Angular**, conectada a una arquitectura de microservicios con **Node.js, Express y MySQL** documentada bajo el estándar **OpenAPI 3.0 (Swagger UI)**.

---

## 1. Puesta en Marcha Inmediata (0 Instalaciones)

La solución se entrega completamente compilada y empaquetada con dependencias locales, garantizando su ejecución instantánea en cualquier ordenador con Windows:

1. Accede a la carpeta **`Practica_Compilada`** (ubicada en el Escritorio).
2. Haz doble clic sobre el archivo ejecutable:
   👉 **`iniciar_todo.bat`**
3. El script ejecutará automáticamente la liberación de puertos y arrancará:
   - **Servidor Backend REST API (Puerto 8080):** `http://localhost:8080/api-docs/` (Swagger UI interactivo).
   - **Servidor Web PWA (Puerto 8100):** `http://localhost:8100` (Aplicación PWA en vivo).
4. El navegador predeterminado se abrirá automáticamente en ambas direcciones.
5. Para ejecutar la PWA en **modo ventana nativa independiente** (sin barras ni controles de navegador), haz doble clic en **`Abrir_PWA.bat`**.

---

## 2. Control de Acceso y Roles de Usuario

La aplicación cuenta con una **pantalla de inicio de sesión unificada** en tema neutral gris (`#475569`):

| Rol | Usuario | Contraseña | Identidad Visual | Funcionalidades Principales |
| :--- | :--- | :--- | :--- | :--- |
| **Administrador** | `admin` | `admin123` / `adminadmin123` | **Tema Verde** (`#2dd36f`) | Gestión de Usuarios (CRUD), Catálogo de Trabajos (CRUD), Auditoría de Fichajes con filtros de fecha, eliminación y mapas interactivos Leaflet. |
| **Empleado** | `sergio` | `1234` | **Tema Azul** (`#3880ff`) | Registro de turnos en tiempo real, turnos en paralelo, cierre de jornada y consulta histórica de fichajes con cálculo de horas. |
| **Empleado** | `lucia` | `1234` | **Tema Azul** (`#3880ff`) | Registro y consulta de turnos de trabajo. |

---

## 3. Funcionalidades Detalladas del Sistema

### A. Portal del Empleado (Tema Azul)
- **Registrar Fichaje en Tiempo Real:**
  - **Tarjeta superior de "Nueva Jornada / Tarea":** Siempre disponible y activa para seleccionar el trabajo deseado e iniciar la entrada.
  - **Soporte de turnos simultáneos en paralelo:** El empleado puede tener varias tareas activas al mismo tiempo.
  - **Visualización inmediata (0 ms):** Al pulsar "Fichar Entrada", aparece de forma instantánea la tarjeta de turno en curso con las mismas métricas visuales.
  - **Finalización de turno:** Al pulsar el botón rojo **"Finalizar Fichaje"**, el turno se cierra al instante, se actualiza el historial y se muestra un toast verde de confirmación.
- **Consulta de Fichajes:**
  - Filtro por rango de fechas ("Desde" y "Hasta") con selectores de fecha nativos y adaptativos.
  - Historial detallado con fecha/hora de entrada, fecha/hora de salida y cómputo de horas trabajadas.
  - Carga inmediata optimizada con tolerancia a fallos de conexión.

### B. Panel del Administrador (Tema Verde)
- **Gestión de Usuarios (CRUD):**
  - Carga automática e inmediata de la lista completa de usuarios del sistema.
  - Formulario modal para consultar, editar y dar de alta nuevos usuarios con validación de roles (`admin` o `empleado`).
  - Botón verde **"Añadir Nuevo Usuario"** ubicado al final del listado dinámico.
  - Eliminación segura con diálogo modal de confirmación.
- **Gestión de Trabajos (CRUD):**
  - Carga instantánea del catálogo de proyectos y tareas asignables.
  - Botón verde **"Crear Nuevo Trabajo"** al pie de la lista de proyectos.
  - Modificación y borrado de tareas.
- **Auditoría Global de Fichajes:**
  - Visualización de todos los fichajes de la plantilla con distintivos de estado (`Completado` o `Abierto`).
  - Filtros avanzados por empleado y rango de fechas.
  - **Eliminación de fichajes:** Botón rojo para borrar registros obsoletos o erróneos.
  - **Visor de Mapa Interactivo:** Botón **"Ver Mapa de Fichaje"** que abre un modal con OpenStreetMap y Leaflet posicionando con chincheta las coordenadas GPS de la entrada.

---

## 4. Requisitos Técnicos de PWA (Progressive Web App)

Siguiendo la guía de la asignatura (*Procedimiento para crear una App PWA desde Ionic*):

- **Manifiesto Web (`manifest.webmanifest` / `manifest.json`):**
  - Nombre: `Control Horario` / Nombre corto: `ControlHorario`.
  - Modo de visualización: `standalone`.
  - Iconos oficiales corporativos en todas las resoluciones reglamentarias (`favicon.png`, `icon-192.png`, `icon-512.png`, `icon-of-app-icon.png`).
- **Service Worker (`sw.js` y `ngsw-worker.js`):**
  - Registro automático del Service Worker en el ciclo de vida de la aplicación.
  - Política de caché configurada para actualización inmediata en vivo y compatibilidad sin conexión.
- **Instalabilidad:**
  - Compatible con el prompt nativo de instalación de Google Chrome, Edge y navegadores móviles Android/iOS.
  - Lanzador directo `Abrir_PWA.bat` para ejecución en ventana dedicada sin marco web.

---

## 5. Arquitectura del Backend REST API

El servidor backend está construido con **Node.js, Express y MySQL** (`backend-api/server.js`):

- **Seguridad y ApiKey:** Middleware de validación mediante clave `dism-secret-key-2026`.
- **Límite duro de tolerancia a fallos (200 ms):** Wrapper con `Promise.race` en `db.js`. Si el servidor MySQL no está iniciado o sufre caídas de socket, el backend conmuta de inmediato (0 ms) a los datos locales en memoria para que la aplicación nunca se quede congelada.
- **Endpoints principales:**
  - `POST /api/v1/auth/login`: Autenticación por roles.
  - `GET / POST / PUT / DELETE /api/v1/usuarios`: Gestión completa de usuarios.
  - `GET / POST / PUT / DELETE /api/v1/trabajos`: Gestión de proyectos y tareas.
  - `GET /api/v1/fichajes`: Consulta y auditoría con filtros.
  - `POST /api/v1/fichajes`: Inicio de turno con GPS.
  - `PUT /api/v1/fichajes/cerrar/:id`: Cierre de turno y cálculo de horas.
  - `DELETE /api/v1/fichajes/:id`: Eliminación de registros de fichaje.
  - `GET /api/v1/fichajes/activos/:idUsuario`: Listado de turnos abiertos en paralelo.

---

## 6. Capturas de Pantalla Móviles (Responsive 470 x 900 px)

Para la presentación del proyecto se ha generado una colección completa de capturas de pantalla automatizadas en resolución móvil nativa de **470 x 900 píxeles**, disponibles en la carpeta:
📁 **`Capturas_Responsive_470x900/`**

### Documento PDF de Presentación
Se incluye el archivo listo para imprimir o proyectar:
📄 **`Capturas_Responsive_470x900/Presentacion_Capturas_PWA.pdf`**

### Relación de Pantallas:
1. **`01_Login_Inicio.png`**: Pantalla inicial de login con tema neutral gris.
2. **`02_Login_Error_Contrasena.png`**: Feedback inmediato ante contraseña incorrecta con toast rojo y spinner detenido.
3. **`03_Login_Exito_Toast.png`**: Notificación de bienvenida personalizada tras login correcto.
4. **`04_Panel_Admin_General.png`**: Menú principal del Administrador con tema verde.
5. **`05_Admin_Gestion_Usuarios.png`**: Listado de usuarios con roles y botón inferior "Añadir Nuevo Usuario".
6. **`06_Admin_Modal_Detalle_Usuario.png`**: Formulario modal de alta/edición de usuario.
7. **`07_Admin_Gestion_Trabajos.png`**: Catálogo de proyectos y botón inferior "Crear Nuevo Trabajo".
8. **`08_Admin_Modal_Detalle_Trabajo.png`**: Formulario modal de detalle de trabajo.
9. **`09_Admin_Gestion_Fichajes.png`**: Panel de auditoría de fichajes con filtros y botón de eliminación.
10. **`10_Admin_Modal_Mapa_Fichaje.png`**: Modal interactivo de mapa Leaflet con marcador GPS.
11. **`11_Panel_Empleado_General.png`**: Menú principal del Empleado con tema azul corporativo.
12. **`12_Empleado_Registrar_Fichaje_Inicial.png`**: Formulario de entrada con selector de tareas y botón activo.
13. **`13_Empleado_Fichajes_Activos_Paralelo.png`**: Turnos activos en paralelo con métricas visuales homologadas.
14. **`14_Empleado_Fichaje_Finalizado_Toast.png`**: Confirmación verde tras finalizar turno y borrado inmediato.
15. **`15_Empleado_Consulta_Fichajes.png`**: Historial de fichajes con selector de fechas adaptativo claro/oscuro.
16. **`16_Cerrar_Sesion_Retorno_Login.png`**: Cierre de sesión seguro y retorno limpio al inicio.
