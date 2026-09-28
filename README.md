# 📱 DISM - Desarrollo de Interfaces para Sistemas Móviles
> **Universidad de Alicante** | Curso Académico 2025-2026  
> Memoria Técnica y Documentación Exhaustiva de Prácticas y Ejercicios Guiados (`DISM0` - `DISM10` + `Anexos`).

---

# 📑 Índice General
1. [Ejercicio 0: Instalación de Software y Proyecto Base (`DISM0`)](#-ejercicio-0-instalación-de-software-y-verificación-del-entorno-dism0)
2. [Ejercicio 1: Componentes Visuales y Plantilla Tabs (`DISM1`)](#-ejercicio-1-desarrollo-de-aplicación-tabs-y-componentes-visuales-dism1)
3. [Ejercicio 2: Navegación y Menú Lateral (`DISM2`)](#-ejercicio-2-desarrollo-de-aplicación-side-menú-lateral-dism2)
4. [Ejercicio 3: Servicios y Consumo de API Externa (`DISM3`)](#-ejercicio-3-servicios-y-consumo-de-api-rest-externa-dism3)
5. [Ejercicio 4: Creación de Mock Backend Fake REST (`DISM4`)](#-ejercicio-4-creación-de-un-backend-fake-rest-api-dism4)
6. [Ejercicio 5: Consumo y CRUD Completo Fake REST API (`DISM5`)](#-ejercicio-5-consumo-de-fake-rest-api-y-operaciones-crud-dism5)
7. [Ejercicio 6: Geolocalización y Geocodificación Inversa (`DISM6`)](#-ejercicio-6-geolocalización-y-georreferenciación-inversa-dism6)
8. [Ejercicio 7: Mapas Interactivos con Leaflet (`DISM7`)](#-ejercicio-7-mapas-interactivos-con-leaflet-dism7)
9. [Ejercicio 8: Diseño de API REST con OpenAPI 3.0 (`DISM8`)](#-ejercicio-8-diseño-de-api-rest-con-openapi-300-dism8)
10. [Ejercicio 9: Generación de Stub Node.js/Express con Swagger (`DISM9`)](#-ejercicio-9-generación-de-stub-express-con-openapi-generator-dism9)
11. [Ejercicio 10: API REST con Acceso a Base de Datos MySQL (`DISM10`)](#-ejercicio-10-generación-de-api-rest-con-acceso-a-base-de-datos-mysql-dism10)
12. [Anexo: Servicios Web REST con Node.js & Express (`Anexos/`)](#-anexo-servicios-web-rest-con-nodejs-express-y-mysql-anexos)

---

## 🛠️ Ejercicio 0: Instalación de Software y Verificación del Entorno (`DISM0`)

### 🎯 Descripción y Objetivos
Verificación e instalación del entorno completo de desarrollo híbrido multiplataforma (Node.js LTS, npm, Ionic CLI y Angular Standalone). Se genera el proyecto base `tabs` para comprobar el ciclo de compilación y servidor de desarrollo local.

### 💻 Comandos Clave
```bash
# Instalación del CLI de Ionic globalmente
npm install -g @ionic/cli

# Creación del proyecto base (Angular + Standalone + Tabs)
ionic start DISM0 tabs --type=angular

# Ejecución del servidor local de desarrollo
cd DISM0
ionic serve
```

### 📂 Estructura del Workspace (`DISM0/`)
```text
DISM0/
├── angular.json
├── capacitor.config.ts
├── ionic.config.json
├── package.json
├── tsconfig.json
└── src/
    ├── index.html
    ├── main.ts
    ├── global.scss
    ├── app/
    │   ├── app.component.ts
    │   ├── app.routes.ts
    │   ├── tabs/
    │   ├── tab1/
    │   ├── tab2/
    │   └── tab3/
    ├── assets/
    └── theme/
        └── variables.scss
```

### 📝 Archivos y Localización Exacta
- `DISM0/src/main.ts`: Punto de entrada que inicializa la aplicación Angular Standalone.
- `DISM0/ionic.config.json`: Configuración del proyecto Ionic.

---

## 🎨 Ejercicio 1: Desarrollo de Aplicación TABS y Componentes Visuales (`DISM1`)

### 🎯 Descripción y Objetivos
Construcción de una interfaz multipestaña personalizada con 4 pestañas navegables (`Inicio`, `Listas`, `Tarjeta/Foto`, `Formulario/Toggles`). Integración de componentes visuales nativos de Ionic: botones con variantes (`ion-button`), listas estáticas y dinámicas iteradas mediante la directiva `@for` (`ion-list`, `ion-item`), tarjetas enriquecidas (`ion-card`, `ion-card-header`, `ion-card-content`) y conmutadores booleanos (`ion-toggle`).

### 💻 Comandos Clave
```bash
ionic start DISM1 tabs --type=angular
cd DISM1
ionic generate page formulario
ionic serve
```

### 📂 Estructura del Workspace (`DISM1/`)
```text
DISM1/
└── src/
    └── app/
        ├── app.routes.ts
        ├── tabs/
        │   ├── tabs.page.html        # Barra inferior de 4 tabs (ion-tab-bar)
        │   ├── tabs.page.ts          # Registro de iconos en el injector
        │   └── tabs.routes.ts        # Enrutamiento hijo de cada tab
        ├── tab1/
        │   ├── tab1.page.html        # Catálogo de botones ion-button
        │   └── tab1.page.ts
        ├── tab2/
        │   ├── tab2.page.html        # Listas estáticas y dinámicas (@for)
        │   └── tab2.page.ts          # Array de datos ['Sandía', 'Naranja'...]
        ├── tab3/
        │   ├── tab3.page.html        # Tarjeta ion-card con imagen y texto
        │   └── tab3.page.ts
        └── formulario/
            ├── formulario.page.html  # Conmutadores ion-toggle
            └── formulario.page.ts
```

### 📝 Archivos y Localización Exacta
- `DISM1/src/app/tabs/tabs.page.html`: Estructura del `ion-tab-bar` con enlaces a `tab1`, `tab2`, `tab3` y `formulario`.
- `DISM1/src/app/tabs/tabs.page.ts`: Inyección de iconos (`triangle`, `ellipse`, `square`, `add`) mediante `addIcons()`.
- `DISM1/src/app/tab1/tab1.page.html`: Demostración de botones `fill` (`clear`, `outline`, `solid`), `expand` (`block`, `full`), `size`, `color` e iconos.
- `DISM1/src/app/tab2/tab2.page.html`: Renderizado de lista estática y lista dinámica con `@for (item of lista; track $index)`.
- `DISM1/src/app/tab3/tab3.page.html`: Maquetación de `ion-card` con cabecera, imagen y cuerpo.
- `DISM1/src/app/formulario/formulario.page.html`: Conmutadores `ion-toggle` con estados `checked`, `disabled` y paleta de colores.

---

## 📑 Ejercicio 2: Desarrollo de Aplicación Side (Menú Lateral) (`DISM2`)

### 🎯 Descripción y Objetivos
Diseño e implementación del patrón de navegación lateral responsive mediante `ion-split-pane` y `ion-menu`. Creación de navegación multipágina entre la vista principal (`Home`) y la página de créditos (`Credits`), integrando botones de apertura de menú (`ion-menu-button`) y navegación dual (declarativa con `[routerLink]` y programática mediante el servicio `Router.navigate`).

### 💻 Comandos Clave
```bash
ionic start DISM2 blank --type=angular
cd DISM2
ionic generate page credits
ionic serve
```

### 📂 Estructura del Workspace (`DISM2/`)
```text
DISM2/
└── src/
    └── app/
        ├── app.component.html        # Menú lateral responsive (ion-split-pane)
        ├── app.component.ts          # Registro de iconos e imports de Ionic
        ├── app.routes.ts             # Rutas hacia 'home' y 'credits'
        ├── home/
        │   ├── home.page.html        # Botones de navegación hacia créditos
        │   └── home.page.ts          # Función mostrarPagina() con Router
        └── credits/
            ├── credits.page.html     # Botones de retorno hacia home
            └── credits.page.ts       # Navegación inversa
```

### 📝 Archivos y Localización Exacta
- `DISM2/src/app/app.component.html`: Menú lateral `ion-menu` envuelto en `ion-split-pane` con `contentId="main-content"`.
- `DISM2/src/app/home/home.page.html`: Botones con `[routerLink]="['/credits']"` y `(click)="mostrarPagina()"`.
- `DISM2/src/app/home/home.page.ts`: Inyección de `Router` y ejecución de `this.router.navigate(['/credits'])`.
- `DISM2/src/app/credits/credits.page.html`: Botones simétricos para regresar a la página de inicio.

---

## 🌐 Ejercicio 3: Servicios y Consumo de API REST Externa (`DISM3`)

### 🎯 Descripción y Objetivos
Arquitectura de separación de responsabilidades mediante la creación de un servicio Angular (`HttpService`). Configuración de `HttpClient` en `main.ts` con `provideHttpClient()`, consumo asíncrono de la API pública `https://randomuser.me/api/?results=25` y renderizado reactivo con `ion-avatar`, `ion-img` y bloques `@for` / `@empty`.

### 💻 Comandos Clave
```bash
ionic start DISM3 blank --type=angular
cd DISM3
ionic generate service services/http
ionic serve
```

### 📂 Estructura del Workspace (`DISM3/`)
```text
DISM3/
└── src/
    ├── main.ts                       # Inyección de provideHttpClient()
    └── app/
        ├── services/
        │   └── http.ts               # Servicio HTTP con método loadUsers()
        └── home/
            ├── home.page.html        # ion-list con @for y avatares
            └── home.page.ts          # Invocación asíncrona con firstValueFrom
```

### 📝 Archivos y Localización Exacta
- `DISM3/src/main.ts`: Inclusión de `provideHttpClient()` en el array de `providers` del bootstrap.
- `DISM3/src/app/services/http.ts`: Método `loadUsers()` que ejecuta `this.http.get('https://randomuser.me/api/?results=25')`.
- `DISM3/src/app/home/home.page.ts`: Consumo con `await firstValueFrom(this.http.loadUsers())` mapeando el array `usuarios`.
- `DISM3/src/app/home/home.page.html`: Vista que muestra avatar (`usuario.picture.medium`), nombre y email.

---

## 🗄️ Ejercicio 4: Creación de un Backend Fake REST API (`DISM4`)

### 🎯 Descripción y Objetivos
Despliegue de un servidor backend simulado (Mock API REST) mediante `json-server` para desarrollo y pruebas en local, exponiendo el recurso `/usuarios` en el puerto `3000` con soporte completo de operaciones CRUD (`GET`, `POST`, `PUT`, `DELETE`).

### 💻 Comandos Clave
```bash
# Instalación global o ejecución directa con npx
npm install -g json-server

# Arranque del servidor mock en el puerto 3000
cd DISM4
npx json-server db.json --port 3000
```

### 📂 Estructura del Workspace (`DISM4/`)
```text
DISM4/
└── db.json                           # Base de datos JSON con colección 'usuarios'
```

### 📝 Archivos y Localización Exacta
- `DISM4/db.json`: Archivo JSON estructurado con la colección de usuarios (`id`, `nombre`, `email`, `edad`).
  ```json
  {
    "usuarios": [
      { "id": "1", "nombre": "Sergio", "email": "sergio@ua.es", "edad": "20" },
      { "id": "2", "nombre": "Estela", "email": "estela@ua.es", "edad": "19" },
      { "id": "3", "nombre": "Susana", "email": "susana@ua.es", "edad": "27" },
      { "id": "4", "nombre": "Hugo", "email": "hugo@ua.es", "edad": "21" }
    ]
  }
  ```

---

## 🔄 Ejercicio 5: Consumo de Fake REST API y Operaciones CRUD (`DISM5`)

### 🎯 Descripción y Objetivos
Desarrollo de una aplicación cliente completa en Ionic/Angular para gestionar el ciclo de vida completo de los datos (CRUD) contra el servidor `json-server`. Creación del modelo fuertemente tipado `Usuario`, servicio de consumo `ApiService` con manejo centralizado de cabeceras HTTP y errores con `pipe(retry(2), catchError())`, y vistas independientes para Listar/Eliminar (`Home`), Editar (`Editar`) y Crear (`Nuevo`) con enlace bidireccional de formularios mediante `[(ngModel)]`.

### 💻 Comandos Clave
```bash
ionic start DISM5 blank --type=angular
cd DISM5
ionic generate page editar
ionic generate page nuevo
ionic generate class models/usuario
ionic generate service services/api
ionic serve
```

### 📂 Estructura del Workspace (`DISM5/`)
```text
DISM5/
└── src/
    ├── main.ts                       # provideHttpClient() registrado
    └── app/
        ├── models/
        │   └── usuario.ts            # Clase modelo Usuario
        ├── services/
        │   └── api.ts                # ApiService: getList, createItem, updateItem, deleteItem
        ├── home/
        │   ├── home.page.html        # Listado, botones editar/borrar y botón Nuevo
        │   └── home.page.ts          # ionViewWillEnter, getAllUsuarios, deleteUsuario, editUsuario
        ├── editar/
        │   ├── editar.page.html      # Formulario ngModel con botón Actualizar y Cancelar
        │   └── editar.page.ts        # Recepción de state y llamada PUT
        └── nuevo/
            ├── nuevo.page.html       # Formulario ngModel con botón Añadir y Cancelar
            └── nuevo.page.ts         # Llamada POST y navegación de retorno
```

### 📝 Archivos y Localización Exacta
- `DISM5/src/app/models/usuario.ts`: Definición de la entidad `Usuario` con campos `id`, `nombre`, `email`, `edad`.
- `DISM5/src/app/services/api.ts`: Métodos `getList()`, `getItem(id)`, `createItem(item)`, `updateItem(item)` y `deleteItem(id)` con `HttpHeaders({ 'Content-Type': 'application/json' })`.
- `DISM5/src/app/home/home.page.ts`: Recarga en `ionViewWillEnter()` y eliminación con reactivación de lista.
- `DISM5/src/app/editar/editar.page.ts`: Lectura del objeto pasado mediante `history.state.item` y llamada a `updateItem()`.
- `DISM5/src/app/nuevo/nuevo.page.ts`: Inicialización de datos y llamada a `createItem()` volviendo a `/home`.

---

## 📍 Ejercicio 6: Geolocalización y Georreferenciación Inversa (`DISM6`)

### 🎯 Descripción y Objetivos
Integración del plugin nativo `@capacitor/geolocation` para consultar el hardware GPS del dispositivo y obtener la latitud y longitud en tiempo real. Comunicación con el servicio web público **Nominatim de OpenStreetMap** para traducir las coordenadas en una dirección postal legible para humanos (*Reverse Geocoding*).

### 💻 Comandos Clave
```bash
ionic start DISM6 blank --type=angular
cd DISM6
npm install @capacitor/geolocation
ionic serve
```

### 📂 Estructura del Workspace (`DISM6/`)
```text
DISM6/
└── src/
    ├── main.ts                       # provideHttpClient() para peticiones a Nominatim
    └── app/
        └── home/
            ├── home.page.html        # Botón locate y visualización con ion-badge
            └── home.page.ts          # Geolocation.getCurrentPosition() y consulta HTTP
```

### 📝 Archivos y Localización Exacta
- `DISM6/src/main.ts`: Inyección de `provideHttpClient()`.
- `DISM6/src/app/home/home.page.ts`: Función asíncrona `locate()` que obtiene las coordenadas y realiza la consulta a `https://nominatim.openstreetmap.org/reverse?format=json&lat=...&lon=...`.
- `DISM6/src/app/home/home.page.html`: Botón de activación y lista con `ion-badge` para mostrar latitud, longitud y dirección completa.

---

## 🗺️ Ejercicio 7: Mapas Interactivos con Leaflet (`DISM7`)

### 🎯 Descripción y Objetivos
Integración del framework cartográfico **Leaflet** en Ionic/Angular Standalone. Carga de mapa con capas de mosaicos (tiles) de **OpenStreetMap**, configuración de dimensiones responsivas del contenedor, corrección de rutas de iconos en `angular.json` y posicionamiento de marcadores interactivos con ventanas emergentes (*popups*) en Alicante y Barcelona.

### 💻 Comandos Clave
```bash
ionic start DISM7 blank --type=angular
cd DISM7
npm install leaflet --save
npm i --save-dev @types/leaflet
ionic serve
```

### 📂 Estructura del Workspace (`DISM7/`)
```text
DISM7/
├── angular.json                      # Copia de imágenes de leaflet a assets/
└── src/
    ├── global.scss                   # @import "leaflet/dist/leaflet.css";
    └── app/
        └── home/
            ├── home.page.scss        # #mapId { width: 100%; height: 100%; }
            ├── home.page.html        # <div id="mapId"></div>
            └── home.page.ts          # Leaflet.map, tileLayer, marcadores y popups
```

### 📝 Archivos y Localización Exacta
- `DISM7/angular.json`: Inclusión del glob para copiar `node_modules/leaflet/dist/images/` a `./assets/`.
- `DISM7/src/global.scss`: Importación de la hoja de estilos global de Leaflet `@import "leaflet/dist/leaflet.css";`.
- `DISM7/src/app/home/home.page.scss`: Definición obligatoria de dimensiones para `#mapId` al 100%.
- `DISM7/src/app/home/home.page.ts`: Inicialización en el hook del ciclo de vida `ionViewDidEnter()`, fijando vista en `[38.38735, -0.51238]` con marcadores en Alicante y Barcelona.

---

## 📑 Ejercicio 8: Diseño de API REST con OpenAPI 3.0.0 (`DISM8`)

### 🎯 Descripción y Objetivos
Aplicación de la metodología **Design-First (API-First)**. Diseño formal de un contrato de API REST en formato YAML cumpliendo el estándar **OpenAPI 3.0.0** para el servicio `/holamundo`. Definición de metadatos, parámetros de query string obligatorios y esquemas de respuesta HTTP 200 y 400. Visualización y pruebas interactivas en VS Code mediante **OpenAPI Editor** y **Swagger UI**.

### 📂 Estructura del Workspace (`DISM8/`)
```text
DISM8/
└── HolaMundo.yaml                    # Especificación OpenAPI 3.0.0
```

### 📝 Archivos y Localización Exacta
- `DISM8/HolaMundo.yaml` (y en raíz `HolaMundo.yaml`): Especificación del endpoint `GET /holamundo` con parámetro `nombreEntradaHolaMundo` y respuestas 200 (`{ nombre, contador }`) y 400 (`{ message }`).

---

## ⚡ Ejercicio 9: Generación de Stub Express con OpenAPI Generator (`DISM9`)

### 🎯 Descripción y Objetivos
Generación automática de un servidor backend en **Node.js con Express** a partir del contrato `HolaMundo.yaml` usando `@openapitools/openapi-generator-cli`. Modificación de la capa de servicios para devolver `"Hola Mundo DISM 2025-2026"` y `contador: 999`, levantando el servidor en el puerto 8080 y validando la documentación interactiva en `http://localhost:8080/api-docs`.

### 💻 Comandos Clave
```bash
# Instalación del generador
npm i -g @openapitools/openapi-generator-cli

# Generación del servidor stub en DISM9
openapi-generator-cli generate -i ./HolaMundo.yaml -g nodejs-express-server -o ./DISM9

# Instalación y arranque del servidor
cd DISM9
npm install
npm start
```

### 📂 Estructura del Workspace (`DISM9/`)
```text
DISM9/
├── config.js                         # Configuración de puertos y rutas base
├── expressServer.js                  # Servidor Express, CORS, validación y Swagger UI
├── index.js                          # Punto de entrada HTTP (puerto 8080)
├── logger.js                         # Logger Winston
├── package.json                      # Dependencias del servidor
├── api/
│   └── openapi.yaml                  # Copia de la especificación OpenAPI
├── controllers/
│   └── HolaMundoServicioController.js # Controlador que recibe la petición
└── services/
    └── HolaMundoServicioService.js    # Lógica de negocio (retorna mensaje y contador)
```

### 📝 Archivos y Localización Exacta
- `DISM9/services/HolaMundoServicioService.js`: Modificación de `holamundoGET` para resolver `{ contador: 999, nombre: 'Hola Mundo DISM 2025-2026' }`.
- `DISM9/api/openapi.yaml`: Configuración de `http://localhost:8080` en la sección `servers`.
- `DISM9/expressServer.js`: Montaje de Swagger UI en la ruta `/api-docs`.

---

## 🗄️ Ejercicio 10: Generación de API REST con Acceso a Base de Datos MySQL (`DISM10`)

### 🎯 Descripción y Objetivos
Construcción de una API REST completa con persistencia en **Base de Datos MySQL (BD `dism`, tabla `usuarios`)** a partir de una especificación OpenAPI CRUD. Creación del script SQL de base de datos, generación del stub Express con OpenAPI Generator, integración del driver `mysql2` e implementación de todas las consultas SQL (`SELECT`, `INSERT`, `UPDATE`, `DELETE`) en la capa de servicios.

### 💻 Comandos Clave
```bash
# 1. Generación del proyecto a partir de UsuariosApi.yaml
openapi-generator-cli generate -i ./DISM10/UsuariosApi.yaml -g nodejs-express-server -o ./DISM10

# 2. Instalación de dependencias (incluye express, swagger-ui, mysql2)
cd DISM10
npm install

# 3. Arranque del servidor
npm start
```

### 📂 Estructura del Workspace (`DISM10/`)
```text
DISM10/
├── database.sql                      # Script de creación de BD y tabla usuarios
├── UsuariosApi.yaml                  # Contrato OpenAPI 3.0 CRUD completo
├── config.js
├── expressServer.js                  # Swagger UI en /api-docs y middlewares
├── index.js                          # Arranque en puerto 8080
├── package.json                      # Incluye mysql2, cors, swagger-ui-express
├── api/
│   └── openapi.yaml
├── controllers/
│   └── UsuariosController.js
└── services/
    └── UsuariosService.js            # Consultas MySQL (SELECT, INSERT, UPDATE, DELETE)
```

### 📝 Archivos y Localización Exacta
- `DISM10/database.sql`: Script DDL/DML para crear la base de datos `dism`, tabla `usuarios` e insertar registros de prueba.
- `DISM10/UsuariosApi.yaml`: Especificación formal de las 5 operaciones CRUD (`/usuarios` GET/POST, `/usuarios/{id}` GET/PUT/DELETE).
- `DISM10/services/UsuariosService.js`: Conexión mediante `mysql.createPool` ejecutando queries SQL con soporte y fallback local resiliente.

---

## 📚 Anexo: Servicios Web REST con Node.js, Express y MySQL (`Anexos/`)

### 🎯 Descripción y Objetivos
Scripts de apoyo incluidos en el material docente para asimilar los fundamentos de desarrollo backend con Express puro y conexión directa a base de datos relacional MySQL.

### 📂 Estructura del Workspace (`Anexos/`)
```text
Anexos/
├── Ejercicio1.js                     # Servidor Express con parámetros JSON en URL (/HolaMundo/:nombre)
├── Ejercicio2.js                     # API REST CRUD manual sobre colección /items con body-parser
└── Ejercicio3.js                     # Conexión directa a MySQL con mysql2 y consulta a tabla usuarios
```

### 📝 Archivos y Localización Exacta
- `Anexos/Ejercicio1.js`: Escucha en puerto 8080 y parsea `JSON.parse(req.params.nombre)` devolviendo `!Hola, Mundo <nombre> !`.
- `Anexos/Ejercicio2.js`: Rutas `GET /items`, `GET /items?filter=ABC`, `GET /items/:id`, `POST /items`, `PUT /items`, `DELETE /items/:id`.
- `Anexos/Ejercicio3.js`: Conexión directa con `mysql2.createConnection` y endpoint `GET /usuarios`.

---

## 🚀 Script de Subida a GitHub
En el Escritorio del equipo se encuentra disponible el script automatizado:
`C:\Users\paucr\Desktop\push_github.bat`
Permite añadir todos los cambios, solicitar mensaje de commit y realizar `git push origin main` con un solo clic.
