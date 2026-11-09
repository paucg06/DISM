# Control Horario PWA - Práctica 2 (DISM)
## Sistema Unificado de Registro Horario y Gestión Empresarial

Proyecto correspondiente a la **Entrega 2 de DISM (Desarrollo de Interfaces para Sistemas Móviles)**.

Se ha diseñado e implementado una solución integral basada en una **Progressive Web App (PWA)** desarrollada con **Ionic Framework** y **Angular**, conectada a una arquitectura de backend REST con **Node.js, Express y MySQL / SQLite** documentada bajo el estándar **OpenAPI 3.0 (Swagger UI)**.

---

## 1. Puesta en Marcha Inmediata (0 Instalaciones)

La solución se entrega completamente compilada y empaquetada con sus dependencias en la carpeta de distribución del Escritorio:

1. Accede a la carpeta **`Practica_Compilada`** (ubicada en el Escritorio).
2. Haz doble clic sobre el script de inicio:
   - **`iniciar_todo.bat`**
3. El script liberará automáticamente los puertos en caso de conflicto y levantará los servicios:
   - **Servidor Backend REST API (Puerto 8080):** `http://localhost:8080/api-docs/` (Documentación Swagger UI interactiva).
   - **Servidor Web PWA (Puerto 8100):** `http://localhost:8100` (Aplicación PWA unificada).
4. El navegador predeterminado se abrirá automáticamente en ambas direcciones.
5. Para ejecutar la aplicación en **modo ventana nativa independiente** (sin barras de navegación del explorador), haz doble clic en **`Abrir_PWA.bat`**.

---

## 2. Control de Acceso y Roles de Usuario

La aplicación cuenta con una **pantalla de autenticación unificada** con identidad visual neutral en escala de grises (`#475569`):

| Rol | Usuario | Contraseña | Identidad Visual | Funcionalidades Principales |
| :--- | :--- | :--- | :--- | :--- |
| **Administrador** | `admin` | `admin123` / `adminadmin123` | **Tema Verde** (`#2dd36f`) | Gestión de Usuarios (CRUD), Catálogo de Trabajos (CRUD), Auditoría de Fichajes con filtros de fecha adaptativos, borrado de turnos y visor de mapas interactivos Leaflet con chincheta GPS. |
| **Empleado** | `sergio` | `1234` | **Tema Azul** (`#3880ff`) | Registro de turnos en tiempo real, soporte de turnos simultáneos en paralelo, cierre instantáneo de jornada y consulta de historial con cómputo de horas. |
| **Empleado** | `lucia` | `1234` | **Tema Azul** (`#3880ff`) | Registro y consulta de turnos de trabajo individuales. |

---

## 3. Funcionalidades Detalladas del Sistema

### A. Portal del Empleado (Tema Azul)
- **Registro de Jornada y Turnos en Paralelo:**
  - **Tarjeta superior "Nueva Jornada / Tarea":** Permite seleccionar el proyecto asignado y pulsar "Fichar Entrada". El botón permanece siempre activo para permitir iniciar múltiples tareas consecutivas.
  - **Tarjetas dinámicas de "Fichaje en Curso":** Al pulsar el botón de entrada, se genera de inmediato (0 ms) un recuadro debajo que homologa exactamente las métricas, bordes y estilos de la tarjeta superior.
  - **Multitarea en paralelo:** El empleado puede tener abiertos dos o más turnos simultáneamente para proyectos diferentes, mostrando el contador dinámico de fichajes activos.
  - **Finalización de turno:** Al presionar el botón rojo **"Finalizar Fichaje"** en cualquiera de las tareas en curso, dicho recuadro desaparece instantáneamente y se presenta un aviso toast verde de confirmación.
- **Consulta de Fichajes:**
  - Filtro por rango de fechas ("Fecha Inicio" y "Fecha Fin") con iconos de calendario adaptativos (`filter: invert(0)` en tema claro y `filter: invert(1)` en tema oscuro).
  - Cálculo automático del total de horas trabajadas y visualización cronológica detallada.

### B. Panel del Administrador (Tema Verde)
- **Gestión de Usuarios (CRUD):**
  - Carga inmediata y completa de la lista de usuarios al entrar a la sección.
  - Ventana modal interactiva para consultar y editar usuarios existentes.
  - Botón verde **"Añadir Nuevo Usuario"** al pie del listado para dar de alta nuevos empleados o administradores.
  - Borrado directo con diálogo de confirmación.
- **Gestión de Trabajos (CRUD):**
  - Catálogo de tareas y proyectos disponible de forma instantánea.
  - Ventana modal para visualizar y actualizar denominaciones y códigos.
  - Botón verde **"Crear Nuevo Trabajo"** ubicado al final de la lista.
- **Auditoría Global de Fichajes y Mapa Leaflet:**
  - Filtros avanzados por empleado y rango de fechas.
  - Visualización del estado del turno (`Completado` o `Abierto (<12h)`).
  - **Botón "Ver Mapa de Fichaje":** Abre una ventana modal emergente con un mapa interactivo de OpenStreetMap renderizado mediante la librería **Leaflet**, posicionando con precisión la chincheta GPS del empleado en el momento del fichaje.
  - **Eliminación de fichajes:** Botón rojo para eliminar registros directamente desde la interfaz de auditoría.

---

## 4. Requisitos Técnicos de PWA (Progressive Web App)

- **Manifiesto Web (`manifest.webmanifest` / `manifest.json`):**
  - Nombre: `Control Horario` / Nombre corto: `ControlHorario`.
  - Modo de visualización: `standalone`.
  - Iconos corporativos actualizados en todas las resoluciones reglamentarias (`assets/icons/favicon.png`, `icon-192.png`, `icon-512.png`, `icon-of-app-icon.png`).
- **Service Worker (`sw.js` y `ngsw-worker.js`):**
  - Registro automático del Service Worker en el ciclo de vida de la aplicación.
  - Política de caché configurada sin conflicto con el almacenamiento local de sesión.
- **Instalabilidad:**
  - Compatible con el prompt de instalación nativo de Google Chrome y Microsoft Edge.
  - Lanzador de acceso directo `Abrir_PWA.bat` para ejecución en ventana de aplicación dedicada.

---

## 5. Catálogo Oficial de Capturas Responsive (470 x 900 px)

Todas las pantallas, modales emergentes y estados del sistema han sido capturados a resolución móvil (470 x 900 px con factor de escala 2x) y se encuentran organizados en la subcarpeta **`Capturas_Responsive_470x900`**:

| N.º | Archivo de Captura | Estado / Pantalla Demostrada |
| :---: | :--- | :--- |
| **01** | `01_Login_Inicio.png` | Pantalla de inicio de sesión limpia en escala de grises. |
| **02** | `02_Login_Error_Contrasena.png` | Aviso toast rojo ante clave errónea y detención inmediata de la barra de carga. |
| **03** | `03_Login_Exito_Toast.png` | Toast de bienvenida personalizado tras introducir credenciales correctas. |
| **04** | `04_Panel_Admin_General.png` | Hub de gestión del Administrador con identidad visual verde. |
| **05** | `05_Admin_Gestion_Usuarios.png` | Listado completo de usuarios y botón inferior "Añadir Nuevo Usuario". |
| **06** | `06_Admin_Modal_Detalle_Usuario.png` | Ventana modal emergente para inspeccionar y editar los datos del usuario. |
| **07** | `07_Admin_Modal_Nuevo_Usuario.png` | Ventana modal emergente para dar de alta un nuevo usuario. |
| **08** | `08_Admin_Gestion_Trabajos.png` | Catálogo de proyectos cargado por defecto y botón inferior "Crear Nuevo Trabajo". |
| **09** | `09_Admin_Modal_Detalle_Trabajo.png` | Ventana modal emergente con el detalle de la tarea seleccionada. |
| **10** | `10_Admin_Modal_Nuevo_Trabajo.png` | Ventana modal emergente para crear una nueva actividad o proyecto. |
| **11** | `11_Admin_Gestion_Fichajes.png` | Auditoría de fichajes con filtros de fecha adaptativos y botón rojo de borrado. |
| **12** | `12_Admin_Modal_Mapa_Fichaje.png` | Ventana modal emergente con el mapa interactivo Leaflet y chincheta GPS. |
| **13** | `13_Panel_Empleado_General.png` | Portal principal del Empleado con identidad corporativa azul. |
| **14** | `14_Empleado_Registrar_Fichaje_Inicial.png` | Pantalla de registro de fichaje con tarjeta superior de Nueva Jornada. |
| **15** | `15_Empleado_Fichaje_Activo_Unico.png` | Recuadro inferior de turno en curso con métricas homologadas y botón finalizar rojo. |
| **16** | `16_Empleado_Fichajes_Activos_Paralelo.png` | Demostración de múltiples turnos activos simultáneos en paralelo. |
| **17** | `17_Empleado_Fichaje_Finalizado_Toast.png` | Cierre de turno: borrado instantáneo del recuadro y confirmación toast verde. |
| **18** | `18_Empleado_Consulta_Fichajes.png` | Historial individual de jornadas con cálculo de horas y selectores de fecha. |
| **19** | `19_Cerrar_Sesion_Retorno_Login.png` | Cierre seguro de sesión desde la barra superior y retorno limpio al login. |

📄 **Presentación PDF Oficial:**  
Dentro del mismo directorio se incluye el documento compilado en formato A4 **`Presentacion_Capturas_PWA.pdf`**, que agrupa las 19 capturas con ficha descriptiva técnica para su exposición o entrega académica.

---

## 6. Arquitectura del Backend REST API

- **Servidor Express:** `backend-api/server.js` (Puerto 8080).
- **Especificación OpenAPI 3.0:** Archivo `backend-api/openapi.yaml` accesible vía navegador en `/api-docs/`.
- **Persistencia Híbrida y Alta Disponibilidad:** Capa de datos con límite de tolerancia a fallos (`Promise.race` a 200 ms) que conmuta sin interrupciones a la persistencia local en memoria para garantizar que la aplicación nunca se bloquee ante desconexiones de base de datos.
- **Rutas Principales:**
  - `POST /api/v1/auth/login`: Autenticación por roles (`admin` / `empleado`).
  - `GET / POST / PUT / DELETE /api/v1/usuarios`: Mantenimiento de personal.
  - `GET / POST / PUT / DELETE /api/v1/trabajos`: Mantenimiento de proyectos.
  - `GET /api/v1/fichajes`: Auditoría y filtrado por usuario o fechas.
  - `POST /api/v1/fichajes`: Registro de entrada con coordenadas GPS.
  - `PUT /api/v1/fichajes/cerrar/:id`: Finalización de jornada laboral y cómputo de horas.
  - `DELETE /api/v1/fichajes/:id`: Eliminación física de registros.
  - `GET /api/v1/fichajes/activos/:idUsuario`: Consulta de fichajes abiertos en curso.
