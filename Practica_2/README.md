# Control Horario - Sistema PWA y API REST

**Asignatura:** Dispositivos e Infraestructuras de Sistemas Multimedia (DISM)  
**Entrega:** Entrega 2: Ionic & REST  
**Autor:** Pau Cremades García  
**Titulación:** Grado en Ingeniería Multimedia, 3.er curso  
**Institución:** Universidad de Alicante (UA)  
**Curso Académico:** 2026-2027  

---

## 1. Descripción General del Proyecto

Este proyecto implementa una solución integral para el **registro de jornada laboral y control horario empresarial**, combinando una arquitectura desacoplada formada por:

1. **Frontend PWA (Progressive Web App):** Desarrollado con **Ionic Framework** y **Angular**, diseñado para funcionar tanto en navegadores web de escritorio como en dispositivos móviles (Android, iOS) con capacidades de instalación como aplicación nativa independiente (modo standalone).
2. **Backend API REST:** Desarrollado con **Node.js** y **Express**, que expone una interfaz de servicios documentada formalmente bajo la especificación **OpenAPI 3.0 (Swagger UI)**.
3. **Capa de Persistencia:** Base de datos relacional con esquema estructurado para la gestión de usuarios, catálogo de proyectos/tareas y registros de jornada con geolocalización GPS.
4. **Infraestructura de Despliegue Inmediato:** Servidor HTTP nativo en Node.js que permite la ejecución directa de la aplicación compilada sin necesidad de compilar paquetes de Angular ni instalar herramientas adicionales.

---

## 2. Puesta en Marcha Rápida (Ejecución)

El proyecto está preparado para su arranque con un único comando mediante los scripts batch incluidos en la raíz:

### Procedimiento de inicio:
1. Ejecutar el archivo **`Iniciar_Todo.bat`** haciendo doble clic sobre él.
2. El script realiza las siguientes acciones automáticas:
   - Comprueba la presencia de las dependencias mínimas del backend (`backend-api/node_modules`); si no existen, ejecuta `npm install --omit=dev` de forma desatendida.
   - Libera los puertos 8080 y 8100 si hubiese procesos residuales.
   - Inicia el servidor de la API REST en el puerto 8080 (`http://localhost:8080/api-docs/`).
   - Inicia el servidor web de la PWA en el puerto 8100 (`http://localhost:8100`).
   - Abre automáticamente en el navegador web predeterminado tanto la documentación interactiva Swagger como la aplicación PWA.
3. Para ejecutar la aplicación como ventana de app independiente (sin marcos ni barras del explorador), se puede ejecutar **`Abrir_PWA.bat`**.

### Servicios y URLs activas:
- **Aplicación Web PWA:** `http://localhost:8100`
- **Documentación Swagger UI (API REST):** `http://localhost:8080/api-docs/`

### Credenciales de acceso preconfiguradas:
| Rol | Nombre de usuario | Contraseña | Tema visual | Alcance del perfil |
| :--- | :--- | :--- | :--- | :--- |
| **Administrador** | `admin` | `admin123` | Tema Verde (`#16a34a`) | Control total: gestión de personal, catálogo de trabajos, auditoría global de fichajes, mapa Leaflet y borrado. |
| **Empleado** | `sergio` | `1234` | Tema Azul (`#2563eb`) | Registro de jornada laboral en tiempo real, soporte multitarea en paralelo y consulta de historial propio. |
| **Empleado** | `lucia` | `1234` | Tema Azul (`#2563eb`) | Registro y consulta de turnos de trabajo individuales. |

---

## 3. Estructura Detallada del Proyecto

A continuación se detalla la organización de carpetas y la función de cada módulo dentro de la solución:

```
modest-lavoisier/
├── Practica_2/
│   ├── AppRegistroHorario/            # Proyecto Frontend (Ionic / Angular PWA)
│   │   ├── src/                       # Código fuente original TypeScript/SCSS/HTML
│   │   │   ├── app/                   # Módulos y componentes de la aplicación
│   │   │   │   ├── login/             # Componente de autenticación unificado
│   │   │   │   ├── home/              # Dashboard distribuidor por roles
│   │   │   │   ├── usuarios/          # Gestión de personal (CRUD Administrador)
│   │   │   │   ├── trabajos/          # Catálogo de proyectos y tareas (CRUD Administrador)
│   │   │   │   ├── fichajes/          # Auditoría global de turnos y mapa GPS (Administrador)
│   │   │   │   ├── registrar-fichaje/ # Fichaje de entrada, turnos paralelos y salida (Empleado)
│   │   │   │   ├── consulta-fichajes/ # Historial personal de jornadas y cómputo de horas
│   │   │   │   ├── services/          # Servicios Angular (HTTP, Auth, Estado)
│   │   │   │   ├── app-routing.module.ts # Definición de rutas y lazy loading
│   │   │   │   ├── app.component.ts   # Componente raíz de la aplicación
│   │   │   │   └── app.module.ts      # Módulo raíz y configuración global
│   │   │   ├── assets/                # Recursos estáticos (iconos PWA, Leaflet)
│   │   │   ├── environments/          # Configuración de entornos (dev/prod)
│   │   │   ├── theme/                 # Paleta de estilos globales y variables SCSS
│   │   │   ├── index.html             # Punto de entrada HTML de la SPA
│   │   │   ├── main.ts                # Arranque del framework Angular
│   │   │   └── manifest.webmanifest   # Manifiesto PWA para instalación móvil
│   │   ├── www/                       # Compilación optimizada para producción (distribución)
│   │   │   ├── index.html             # HTML empaquetado para despliegue
│   │   │   ├── chunk-*.js             # Módulos JS divididos por rutas (lazy loading)
│   │   │   ├── svg/                   # Conjunto de iconos vectoriales Ionicons
│   │   │   └── assets/                # Iconos corporativos PWA y dependencias visuales
│   │   ├── angular.json               # Configuración del compilador Angular CLI
│   │   ├── ionic.config.json          # Configuración del framework Ionic
│   │   ├── package.json               # Dependencias de desarrollo del frontend
│   │   └── tsconfig.json              # Configuración del compilador TypeScript
│   │
│   ├── backend-api/                   # Servidor de Servicios REST
│   │   ├── server.js                  # Servidor Express, endpoints y middlewares
│   │   ├── openapi.yaml               # Especificación OpenAPI 3.0 formal
│   │   ├── db.js                      # Capa de conexión y acceso a base de datos
│   │   ├── package.json               # Dependencias mínimas del backend
│   │   └── package-lock.json          # Bloqueo de versiones de dependencias
│   │
│   ├── database/                      # Definición de la Base de Datos
│   │   └── schema.sql                 # Sentencias DDL de creación y DML de precarga
│   │
│   ├── Iniciar_Todo.bat               # Script batch de arranque conjunto automático
│   ├── Abrir_PWA.bat                  # Script batch para ejecutar la PWA en ventana nativa
│   ├── servidor_estatico.js           # Servidor web nativo Node.js para la carpeta www/
│   ├── generar_manual_usuario.py      # Script de generación del manual en PDF (ReportLab)
│   ├── Manual_Usuario_PWA_Control_Horario.pdf # Manual de usuario y técnico completo (30 páginas)
│   └── README.md                      # Documentación técnica del proyecto
```

---

## 4. Descripción Exhaustiva de los Componentes

### 4.1. Frontend (`AppRegistroHorario`)

El cliente es una Single Page Application (SPA) construida con **Ionic 7** y **Angular 16/17**:

- **`src/app/login/`:**  
  Gestiona la autenticación inicial. Presenta una interfaz neutra en escala de grises. Realiza la petición POST a la API REST, valida las credenciales y almacena la información de sesión en el almacenamiento local del cliente (`localStorage`), redirigiendo al panel correspondiente según el rol (`admin` o `empleado`).
  
- **`src/app/home/`:**  
  Actúa como distribuidor visual. Presenta las opciones disponibles para cada perfil mediante tarjetas descriptivas con accesos directos y badges identificativos.

- **`src/app/usuarios/`:**  
  Panel exclusivo del administrador para la gestión de la plantilla laboral. Carga la lista completa de empleados desde el backend, permite modificar datos mediante una ventana modal emergente, registrar nuevos usuarios y eliminar cuentas con diálogo de confirmación.

- **`src/app/trabajos/`:**  
  Panel de mantenimiento del catálogo de tareas y proyectos de la empresa. Permite visualizar, dar de alta y editar códigos y denominaciones de los proyectos en los que pueden fichar los trabajadores.

- **`src/app/fichajes/`:**  
  Herramienta de auditoría para el administrador. Incluye filtros combinados por trabajador y rangos de fecha. Cada registro muestra el estado de la jornada (`Completado` o `Abierto`), las horas calculadas, un botón para eliminar el turno y un botón **"Ver mapa de fichaje"**, que abre una ventana modal con un mapa interactivo **Leaflet** con capa de OpenStreetMap, posicionando la chincheta GPS exacta donde se inició la jornada.

- **`src/app/registrar-fichaje/`:**  
  Pantalla operativa del empleado. Permite seleccionar el proyecto y fichar la entrada capturando la geolocalización del dispositivo mediante la API nativa de geolocalización del navegador. Soporta **multitarea en paralelo**: el trabajador puede mantener abiertos varios turnos simultáneos si trabaja en distintos proyectos a la vez. Cada turno en curso se representa en una tarjeta dedicada con botón rojo **"Finalizar Fichaje"** que cierra la jornada en la base de datos y calcula el total de horas devengadas.

- **`src/app/consulta-fichajes/`:**  
  Historial del propio empleado. Permite filtrar por fechas de inicio y fin, mostrando el listado cronológico de turnos y el cómputo total de horas acumuladas en el periodo seleccionado.

- **`src/app/services/`:**  
  Servicios singleton de Angular que centralizan la lógica transversal:
  - `auth.service.ts`: Gestión de estado de sesión, inicio, verificación de rol y cierre seguro.
  - `usuarios.service.ts`: Comunicación HTTP con las rutas de usuarios.
  - `trabajos.service.ts`: Comunicación HTTP con el catálogo de tareas.
  - `fichajes.service.ts`: Comunicación HTTP para aperturas, cierres, auditorías y cómputo de turnos.

---

### 4.2. ¿Qué es la carpeta `www/` y por qué tiene múltiples archivos `chunk-*.js`?

En el framework Ionic/Angular, **`www/` es el directorio de distribución compilado para producción** (el equivalente al directorio `dist/` en otros entornos web). Contiene el código fuente TypeScript, las plantillas HTML y las hojas de estilo SCSS tras ser transpiladas, minificadas y empaquetadas por el compilador de Angular/Webpack/Vite.

- **Archivos `chunk-*.js` (Code Splitting & Lazy Loading):**  
  En lugar de generar un único archivo JavaScript masivo que ralentizaría la carga inicial en teléfonos móviles con conexiones lentas, el compilador divide la aplicación en trozos independientes ("chunks"). Cada página (`login`, `usuarios`, `fichajes`, etc.) y cada conjunto de componentes de Ionic se compila en su propio chunk. De esta forma, el navegador descarga únicamente el código necesario para la pantalla actual, cargando el resto de módulos bajo demanda de manera asíncrona conforme el usuario navega.
- **Archivos `.ts` (TypeScript):**  
  Los archivos con extensión `.ts` corresponden al código fuente de desarrollo y se ubican en `src/app/`. En la carpeta `www/` no se incluyen archivos `.ts` porque el navegador únicamente puede interpretar código JavaScript estándar (`.js`).
- **Conservación de la carpeta `www/`:**  
  Esta carpeta **no debe ser eliminada**. Al incluir `www/` en el proyecto entregable, el evaluador puede arrancar la aplicación de inmediato con el script `Iniciar_Todo.bat` sin requerir la instalación de Angular CLI ni esperar tiempos de compilación.

---

### 4.3. ¿Para qué sirve `servidor_estatico.js`?

El archivo **`servidor_estatico.js` es un servidor web HTTP nativo de Node.js** (desarrollado sin ninguna dependencia externa, utilizando únicamente los módulos estándar `http`, `fs` y `path`).

- **Su función dentro del sistema:**  
  Es el componente encargado de servir la aplicación PWA compilada ubicada en `AppRegistroHorario/www` en el puerto **8100**.
- **Por qué no se debe borrar:**  
  No es un servidor de reserva ni una alternativa descartable. Cuando se ejecuta `Iniciar_Todo.bat`, el paso 2 ejecuta directamente `node servidor_estatico.js`. Si este archivo se eliminara, `Iniciar_Todo.bat` no podría servir la aplicación PWA y el navegador mostraría un error de conexión no disponible en el puerto 8100.
- **Características técnicas:**  
  Implementa resolución MIME automática (HTML, JS, CSS, SVG, WebManifest), cabeceras de no-caché (`no-store, no-cache`) para garantizar que las actualizaciones se reflejen inmediatamente sin alterar el `localStorage` de la sesión, y soporte completo para Single Page Applications (cualquier ruta no estática redirige a `index.html` para permitir el enrutamiento interno de Angular).

---

### 4.4. Backend REST API (`backend-api`)

El backend proporciona una API REST desacoplada que sigue las directrices del estándar OpenAPI 3.0:

- **Servidor principal (`server.js`):**  
  Escucha en el puerto 8080. Configura middlewares de análisis de cuerpo JSON, habilitación de CORS para admitir peticiones desde `http://localhost:8100` y monta la interfaz Swagger UI en la ruta `/api-docs/`.
- **Capa de persistencia híbrida (`db.js`):**  
  Gestiona la conexión con la base de datos relacional y cuenta con un mecanismo de tolerancia a fallos con límite de tiempo (`Promise.race` a 200 ms). Si la base de datos externa no responde en el tiempo estipulado, conmuta de forma transparente al almacenamiento en memoria para evitar bloqueos en la interfaz de usuario.
- **Especificación formal (`openapi.yaml`):**  
  Documento YAML completo que describe cada endpoint, parámetros requeridos, esquemas de entrada y códigos de respuesta HTTP (200, 201, 400, 401, 404, 500).

#### Endpoints implementados en la API REST:
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `POST` | `/api/v1/auth/login` | Autenticación de credenciales y retorno del perfil de usuario (`admin` / `empleado`). |
| `GET` | `/api/v1/usuarios` | Obtención del listado completo de trabajadores de la empresa. |
| `POST` | `/api/v1/usuarios` | Alta de un nuevo usuario en la plantilla. |
| `PUT` | `/api/v1/usuarios/:id` | Modificación de datos de un usuario existente. |
| `DELETE` | `/api/v1/usuarios/:id` | Baja física de un trabajador del sistema. |
| `GET` | `/api/v1/trabajos` | Consulta del catálogo de tareas y proyectos. |
| `POST` | `/api/v1/trabajos` | Creación de una nueva tarea en el catálogo. |
| `PUT` | `/api/v1/trabajos/:id` | Actualización de la denominación o código de un trabajo. |
| `DELETE` | `/api/v1/trabajos/:id` | Eliminación de un trabajo del catálogo. |
| `GET` | `/api/v1/fichajes` | Auditoría de fichajes con filtros opcionales por usuario y rango de fechas. |
| `POST` | `/api/v1/fichajes` | Registro de inicio de turno laboral con coordenadas GPS (`latitud`, `longitud`). |
| `PUT` | `/api/v1/fichajes/cerrar/:id` | Finalización de turno en curso y cálculo de horas trabajadas. |
| `DELETE` | `/api/v1/fichajes/:id` | Eliminación de un registro de fichaje del sistema. |
| `GET` | `/api/v1/fichajes/activos/:idUsuario` | Consulta de turnos abiertos simultáneos para un empleado concreto. |

---

### 4.5. Base de Datos (`database`)

El archivo **`database/schema.sql`** contiene la definición de tablas y datos iniciales:
- **`usuarios`:** Identificador, nombre de usuario, contraseña encriptada/hasheada, nombre completo y rol (`admin` o `empleado`).
- **`trabajos`:** Identificador, código de proyecto y denominación de la tarea.
- **`fichajes`:** Identificador, clave foránea de usuario (`idUsuario`), clave foránea de trabajo (`idTrabajo`), fecha y hora de entrada (`fechaInicio`), fecha y hora de salida (`fechaFin`), horas calculadas (`totalHoras`), coordenadas de geolocalización (`latitud`, `longitud`) y estado (`ABIERTO` o `COMPLETADO`).

---

## 5. Requisitos Cumplidos de Progressive Web App (PWA)

1. **Instalabilidad:** Cuenta con `manifest.webmanifest` debidamente vinculado en el encabezado HTML, definiendo colores temáticos, modo de visualización `standalone` y catálogo de iconos en resoluciones reglamentarias (192x192, 512x512 y favicon).
2. **Service Worker:** Registrado automáticamente en el ciclo de vida del frontend, permitiendo la gestión eficiente del almacenamiento y la disponibilidad de recursos.
3. **Diseño Responsive:** La interfaz ha sido diseñada para adaptarse fluidamente a pantallas de smartphone (probada a 470x900 px), tablets y monitores de escritorio.
4. **Geolocalización en Tiempo Real:** Integración nativa con la API Geolocation del navegador para capturar la posición exacta del trabajador al iniciar el turno.
5. **Cartografía Interactiva sin Claves:** Integración de Leaflet con teselas abiertas de OpenStreetMap, permitiendo visualizar mapas interactivos con marcadores GPS sin necesidad de suscripciones ni claves de API propietarias de terceros.

---

## 6. Documentación Adicional Incluida

- **Manual de Usuario y Guía Técnica:**  
  Documento completo en PDF de 30 páginas ubicado en la raíz del proyecto:  
  **`Manual_Usuario_PWA_Control_Horario.pdf`**  
  Incluye la presentación de la aplicación, primeros pasos, guía de perfiles y permisos, ficha técnica pantalla a pantalla de las 19 vistas del sistema, guías rápidas por tarea, preguntas frecuentes, resolución de problemas y glosario.
- **Script generador del manual:**  
  `generar_manual_usuario.py`, desarrollado con Python y ReportLab para la compilación automatizada del documento oficial.
