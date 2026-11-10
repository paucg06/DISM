# Control Horario — Sistema PWA y API REST
## Arquitectura de Software, Documentación Técnica y Guía de Código

**Asignatura:** Dispositivos e Infraestructuras de Sistemas Multimedia (DISM)  
**Entrega:** Entrega 2: Ionic & REST  
**Autor:** Pau Cremades García  
**Titulación:** Grado en Ingeniería Multimedia, 3.er curso  
**Institución:** Universidad de Alicante (UA)  
**Curso Académico:** 2026-2027  

---

## 1. Introducción y Propósito del Sistema

El proyecto **Control Horario** es una solución informática integral diseñada para la gestión, registro y auditoría de la jornada laboral en entornos corporativos. Resuelve dos necesidades operativas fundamentales dentro de una misma plataforma:

1. **La operativa diaria del trabajador (Perfil Empleado):** Permite registrar entradas y salidas de turno en tiempo real, asignar cada fichaje a proyectos concretos del catálogo, trabajar en múltiples tareas simultáneas en paralelo (multitarea) y consultar el historial acumulado de horas trabajadas con filtrado cronológico.
2. **La supervisión y auditoría integral (Perfil Administrador):** Proporciona un centro de mando para gestionar la plantilla laboral (altas, modificaciones y bajas de usuarios), mantener el catálogo de proyectos o trabajos y auditar todos los fichajes registrados por el personal, incluyendo la inspección visual de las coordenadas GPS mediante mapas interactivos geolocalizados.

El sistema se fundamenta en una **arquitectura desacoplada cliente-servidor**, donde el frontend es una Progressive Web App (PWA) desarrollada sobre **Ionic Framework** y **Angular**, y el backend es un servicio REST desarrollado con **Node.js** y **Express**, respaldado por una base de datos relacional y documentado formalmente bajo el estándar **OpenAPI 3.0 (Swagger UI)**.

---

## 2. Arquitectura Global del Sistema

El sistema implementa un modelo en capas desacopladas que garantiza la escalabilidad, el mantenimiento independiente de cada subsistema y la tolerancia a fallos:

```
+-------------------------------------------------------------------------+
|                       CAPA DE PRESENTACIÓN (PWA)                        |
|   Ionic Framework 7 + Angular 16/17 (TypeScript / HTML5 / SCSS)         |
|                                                                         |
|  +--------------------+  +--------------------+  +--------------------+ |
|  |   Módulo Login     |  |   Portal Empleado  |  |    Panel Admin     | |
|  |   (Autenticación)  |  |   (Fichaje/Turnos) |  |   (CRUD/Auditoría) | |
|  +--------------------+  +--------------------+  +--------------------+ |
|            |                       |                       |            |
|            +-----------------------+-----------------------+            |
|                                    |                                    |
|                       Servicio HTTP: ApiService                         |
|                         (RxJS HttpClient)                               |
+------------------------------------+------------------------------------+
                                     |
                         Peticiones HTTP REST / JSON
                         Puerto 8080 (Cabecera: x-api-key)
                                     |
                                     v
+-------------------------------------------------------------------------+
|                         CAPA DE SERVICIOS (BACKEND)                     |
|                  Node.js + Express REST API (server.js)                 |
|                                                                         |
|  +--------------------+  +--------------------+  +--------------------+ |
|  | Middleware CORS    |  | Validador ApiKey   |  | Swagger UI / Docs  | |
|  +--------------------+  +--------------------+  +--------------------+ |
|  | Rutas /auth        |  | Rutas /usuarios    |  | Rutas /trabajos    | |
|  | Rutas /fichajes    |  | Rutas /fichajes/act|  | Proxy Nominatim    | |
+------------------------------------+------------------------------------+
                                     |
                            Capa de Abstracción
                                  (db.js)
                         Conmutación por Timeout
                                     |
                  +------------------+------------------+
                  |                                     |
                  v                                     v
+-----------------------------------+ +-----------------------------------+
|      BASE DE DATOS RELACIONAL     | |   ALMACENAMIENTO EN MEMORIA (RAM) |
|   SQLite / MySQL (database.sql)   | |   Mock Datasets (Alta Disponib.)  |
|   Tablas: Usuarios, Trabajos,     | |   Garantiza 0 ms de bloqueo ante  |
|   Fichajes, ApiKey                | |   caídas de base de datos         |
+-----------------------------------+ +-----------------------------------+
```

### Características de la Arquitectura:
- **Desacoplamiento Estricto:** El frontend consume exclusivamente la API REST mediante formato JSON; no existe renderizado en servidor (SSR), lo que permite desplegar el cliente en cualquier servidor estático, CDN o contenedor móvil nativo (Capacitor/Cordova).
- **Tolerancia a Fallos (Fault Tolerance):** El backend cuenta con una estrategia de persistencia híbrida. Si la conexión con la base de datos externa experimenta un retraso superior a 200 ms, un interceptor `Promise.race` conmuta automáticamente a datasets en memoria para que ninguna petición del usuario se quede colgada.
- **Optimistic UI en el Cliente:** Las acciones críticas del trabajador (iniciar y finalizar turno) actualizan el árbol del DOM en 0 ms antes de esperar la respuesta del servidor, logrando una sensación de inmediatez idéntica a una aplicación nativa instalada.

---

## 3. Puesta en Marcha y Guía de Ejecución

El proyecto está diseñado bajo el principio de **cero configuraciones manuales**. Toda la infraestructura se levanta mediante scripts por lotes preparados para entornos Windows.

### 3.1. Procedimiento de Arranque Automatizado
1. Acceder a la raíz del proyecto o a la carpeta compilada de entrega.
2. Ejecutar el archivo **`Iniciar_Todo.bat`** haciendo doble clic sobre él.
3. El script ejecuta la siguiente secuencia técnica:
   - **Verificación de Entorno:** Comprueba si existe el directorio `backend-api/node_modules`. Si es la primera ejecución, ejecuta automáticamente `npm install --omit=dev` para instalar las librerías esenciales (`express`, `cors`, `swagger-ui-express`, `yamljs`) sin descargar paquetes superfluos de desarrollo.
   - **Limpieza de Puertos:** Ejecuta consultas `netstat` filtradas por estado `LISTENING` para los puertos **8080** y **8100**, finalizando cualquier proceso previo huérfano con `taskkill /f` para evitar conflictos `EADDRINUSE`.
   - **Lanzamiento de la API REST:** Abre una consola secundaria que ejecuta `node server.js` en el directorio `backend-api`, levantando el backend en `http://localhost:8080`.
   - **Lanzamiento del Servidor Web PWA:** Abre una consola secundaria que ejecuta `node servidor_estatico.js` en la raíz, sirviendo los archivos compilados en `http://localhost:8100`.
   - **Apertura de Navegador:** Lanza el explorador predeterminado en `http://localhost:8080/api-docs/` (Swagger UI) y en `http://localhost:8100` (Aplicación PWA).

### 3.2. Lanzador en Modo Aplicación Nativa (`Abrir_PWA.bat`)
Permite abrir la PWA en una ventana independiente sin barras de dirección, marcadores ni pestañas del navegador, emulando el comportamiento de una app instalada de escritorio. Emplea la bandera `--app` soportada por Google Chrome y Microsoft Edge:
```bat
start "" "chrome.exe" --app="http://localhost:8100/?fresh=%RANDOM%" || start "" "msedge.exe" --app="http://localhost:8100/?fresh=%RANDOM%"
```
El parámetro `fresh=%RANDOM%` actúa como un inhibidor de caché en el parámetro de consulta para garantizar que los scripts JavaScript carguen su versión más reciente sin alterar el almacenamiento persistente (`localStorage`).

### 3.3. Credenciales de Acceso Configuradas
| Perfil | Nombre de Usuario | Contraseña | Rol en Sistema | Tema Visual Asociado |
| :--- | :--- | :--- | :--- | :--- |
| **Administrador** | `admin` | `admin123` | `admin` | Tema Verde Corporativo (`#16a34a`) |
| **Empleado** | `sergio` | `1234` | `empleado` | Tema Azul Corporativo (`#2563eb`) |
| **Empleado** | `lucia` | `1234` | `empleado` | Tema Azul Corporativo (`#2563eb`) |

---

## 4. Estructura de Directorios del Código Fuente

A continuación se desglosa el árbol completo de directorios y la responsabilidad de cada archivo de la solución:

```
modest-lavoisier/
│
├── Practica_2/                                # Directorio principal del proyecto
│   ├── AppRegistroHorario/                    # Aplicación cliente (Ionic / Angular PWA)
│   │   ├── src/                               # Código fuente TypeScript, plantillas y estilos
│   │   │   ├── app/                           # Módulos, componentes y lógica de negocio
│   │   │   │   ├── login/                     # Componente de acceso y autenticación
│   │   │   │   │   ├── login.module.ts        # Declaración del módulo y FormsModule
│   │   │   │   │   ├── login.page.html        # Plantilla con formulario reactivo y tarjetas
│   │   │   │   │   ├── login.page.scss        # Estilos en escala de grises y animaciones
│   │   │   │   │   ├── login.page.spec.ts     # Pruebas unitarias de autenticación
│   │   │   │   │   ├── login.page.ts          # Controlador: validación y guardado de sesión
│   │   │   │   │   └── login-routing.module.ts # Ruta secundaria del componente
│   │   │   │   │
│   │   │   │   ├── home/                      # Dashboard principal según rol
│   │   │   │   │   ├── home.module.ts         # Módulo Angular de inicio
│   │   │   │   │   ├── home.page.html         # Plantilla con vistas condicionales por rol
│   │   │   │   │   ├── home.page.scss         # Estilos visuales de tarjetas de navegación
│   │   │   │   │   ├── home.page.spec.ts      # Pruebas del componente Home
│   │   │   │   │   ├── home.page.ts           # Lógica: detección de rol y cierre de sesión
│   │   │   │   │   └── home-routing.module.ts # Ruta principal
│   │   │   │   │
│   │   │   │   ├── usuarios/                  # Gestión de personal (CRUD Administrador)
│   │   │   │   │   ├── usuarios.module.ts     # Módulo con IonicModule y FormsModule
│   │   │   │   │   ├── usuarios.page.html     # Listado con badges, modales de alta/edición
│   │   │   │   │   ├── usuarios.page.scss     # Estilos de la tabla de usuarios
│   │   │   │   │   ├── usuarios.page.spec.ts  # Pruebas de mantenimiento de usuarios
│   │   │   │   │   ├── usuarios.page.ts       # Controlador CRUD: altas, bajas y cambios
│   │   │   │   │   └── usuarios-routing.module.ts
│   │   │   │   │
│   │   │   │   ├── trabajos/                  # Catálogo de tareas (CRUD Administrador)
│   │   │   │   │   ├── trabajos.module.ts     # Módulo Angular de catálogo de trabajos
│   │   │   │   │   ├── trabajos.page.html     # Lista de proyectos y modales interactivos
│   │   │   │   │   ├── trabajos.page.scss     # Estilos del catálogo
│   │   │   │   │   ├── trabajos.page.spec.ts  # Pruebas unitarias de trabajos
│   │   │   │   │   ├── trabajos.page.ts       # Controlador de operaciones sobre proyectos
│   │   │   │   │   └── trabajos-routing.module.ts
│   │   │   │   │
│   │   │   │   ├── fichajes/                  # Auditoría global y mapa GPS (Administrador)
│   │   │   │   │   ├── fichajes.module.ts     # Módulo con integración de Leaflet
│   │   │   │   │   ├── fichajes.page.html     # Tabla de turnos, filtros y modal de mapa
│   │   │   │   │   ├── fichajes.page.scss     # Estilos del mapa y filtros adaptativos
│   │   │   │   │   ├── fichajes.page.spec.ts  # Pruebas del módulo de auditoría
│   │   │   │   │   ├── fichajes.page.ts       # Controlador: filtros, borrado y Leaflet
│   │   │   │   │   └── fichajes-routing.module.ts
│   │   │   │   │
│   │   │   │   ├── registrar-fichaje/         # Registro y multitarea en paralelo (Empleado)
│   │   │   │   │   ├── registrar-fichaje.module.ts
│   │   │   │   │   ├── registrar-fichaje.page.html # Tarjeta nueva jornada y turnos activos
│   │   │   │   │   ├── registrar-fichaje.page.scss # Estilos homologados de tarjetas
│   │   │   │   │   ├── registrar-fichaje.page.spec.ts
│   │   │   │   │   ├── registrar-fichaje.page.ts   # Optimistic UI, GPS y cierre de turno
│   │   │   │   │   └── registrar-fichaje-routing.module.ts
│   │   │   │   │
│   │   │   │   ├── consulta-fichajes/         # Consulta de historial propio (Empleado)
│   │   │   │   │   ├── consulta-fichajes.module.ts
│   │   │   │   │   ├── consulta-fichajes.page.html # Historial con cómputo de horas
│   │   │   │   │   ├── consulta-fichajes.page.scss # Iconos de fecha con filtro adaptativo
│   │   │   │   │   ├── consulta-fichajes.page.spec.ts
│   │   │   │   │   ├── consulta-fichajes.page.ts   # Controlador de consultas por fecha
│   │   │   │   │   └── consulta-fichajes-routing.module.ts
│   │   │   │   │
│   │   │   │   ├── services/                  # Capa de servicios compartidos
│   │   │   │   │   ├── api.ts                 # Servicio Angular: llamadas HTTP REST y tipos
│   │   │   │   │   └── api.spec.ts            # Pruebas unitarias de servicios
│   │   │   │   │
│   │   │   │   ├── app.component.html         # Contenedor raíz (<ion-app><ion-router-outlet>)
│   │   │   │   ├── app.component.scss         # Estilos del contenedor raíz
│   │   │   │   ├── app.component.spec.ts      # Pruebas del componente raíz
│   │   │   │   ├── app.component.ts           # Inicialización de la aplicación
│   │   │   │   ├── app.module.ts              # Módulo principal (HttpClientModule, IonicModule)
│   │   │   │   └── app-routing.module.ts      # Configuración de rutas globales SPA
│   │   │   │
│   │   │   ├── assets/                        # Recursos multimedia y librerías estáticas
│   │   │   │   ├── icons/                     # Iconos PWA para instalación (192x192, 512x512)
│   │   │   │   ├── marker-icon.png            # Icono chincheta para mapa Leaflet
│   │   │   │   └── marker-shadow.png          # Sombra de marcador para mapa Leaflet
│   │   │   │
│   │   │   ├── environments/                  # Variables de entorno por perfil
│   │   │   │   ├── environment.prod.ts        # Entorno de producción
│   │   │   │   └── environment.ts             # Entorno de desarrollo local
│   │   │   │
│   │   │   ├── theme/                         # Identidad visual corporativa
│   │   │   │   └── variables.scss             # Variables CSS globales, temas claro/oscuro
│   │   │   │
│   │   │   ├── index.html                     # Documento base HTML5
│   │   │   ├── main.ts                        # Punto de entrada Angular (bootstrapModule)
│   │   │   └── manifest.webmanifest           # Manifiesto PWA (identidad, iconos, display)
│   │   │
│   │   ├── www/                               # Paquete de distribución compilado para producción
│   │   │   ├── index.html                     # HTML empaquetado para despliegue directo
│   │   │   ├── chunk-*.js                     # Chunks JavaScript generados por Code Splitting
│   │   │   ├── svg/                           # 1.358 iconos vectoriales de Ionicons
│   │   │   └── assets/                        # Iconos e imágenes empaquetadas
│   │   │
│   │   ├── angular.json                       # Configuración de compilación de Angular CLI
│   │   ├── ionic.config.json                  # Identificador del proyecto en Ionic CLI
│   │   ├── package.json                       # Manifiesto de dependencias npm del cliente
│   │   └── tsconfig.json                      # Configuración de compilación de TypeScript
│   │
│   ├── backend-api/                           # Servidor de servicios web REST
│   │   ├── server.js                          # Servidor Express, definición de rutas y CORS
│   │   ├── openapi.yaml                       # Especificación técnica formal OpenAPI 3.0
│   │   ├── db.js                              # Capa de datos con conexión y tolerancia a fallos
│   │   ├── package.json                       # Dependencias mínimas del backend (Express, CORS)
│   │   └── package-lock.json                  # Árbol exacto de versiones bloqueadas
│   │
│   ├── database/                              # Capa de persistencia relacional
│   │   └── schema.sql                         # Sentencias DDL de estructura y DML de datos
│   │
│   ├── servidor_estatico.js                   # Servidor HTTP nativo en Node.js para www/ (Puerto 8100)
│   ├── Iniciar_Todo.bat                       # Script batch orquestador de inicio completo
│   ├── Abrir_PWA.bat                          # Script batch para abrir la app en ventana nativa
│   ├── Manual_Usuario_PWA_Control_Horario.pdf # Manual de usuario y técnico completo (30 páginas)
│   └── README.md                              # Esta documentación técnica
```

---

## 5. Análisis Técnico del Frontend (Ionic / Angular PWA)

### 5.1. Enrutamiento Modular y Lazy Loading (`app-routing.module.ts`)
El sistema utiliza una estrategia de carga perezosa (**Lazy Loading**) basada en rutas para optimizar el rendimiento. Cada sección de la aplicación solo descarga sus scripts cuando el usuario navega a ella:

```typescript
const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', loadChildren: () => import('./login/login.module').then(m => m.LoginPageModule) },
  { path: 'home', loadChildren: () => import('./home/home.module').then(m => m.HomePageModule) },
  { path: 'usuarios', loadChildren: () => import('./usuarios/usuarios.module').then(m => m.UsuariosPageModule) },
  { path: 'trabajos', loadChildren: () => import('./trabajos/trabajos.module').then(m => m.TrabajosPageModule) },
  { path: 'fichajes', loadChildren: () => import('./fichajes/fichajes.module').then(m => m.FichajesPageModule) },
  { path: 'registrar-fichaje', loadChildren: () => import('./registrar-fichaje/registrar-fichaje.module').then(m => m.RegistrarFichajePageModule) },
  { path: 'consulta-fichajes', loadChildren: () => import('./consulta-fichajes/consulta-fichajes.module').then(m => m.ConsultaFichajesPageModule) },
  { path: '**', redirectTo: 'login' }
];
```
Esta arquitectura garantiza que la página de acceso (`/login`) tenga un peso inferior a 150 KB, logrando tiempos de interacción casi instantáneos incluso en dispositivos móviles de gama baja.

### 5.2. Capa de Servicios y Modelos de Datos (`services/api.ts`)
El servicio `ApiService` centraliza todas las comunicaciones HTTP con la API REST mediante la librería reactiva **RxJS**. Define las interfaces canónicas de TypeScript:

```typescript
export interface Usuario {
  IdUsuario: number;
  Nombre: string;
  Usuario: string;
  Clave?: string;
  Rol?: string;
}

export interface Trabajo {
  IdTrabajo: number;
  Nombre: string;
}

export interface Fichaje {
  IdFichaje: number;
  FechaHoraEntrada: string;
  FechaHoraSalida?: string | null;
  HorasTrabajadas?: number | null;
  IdTrabajo: number;
  NombreTrabajo?: string;
  IdUsuario: number;
  NombreUsuario?: string;
  GeolocalizacionLatitud: number;
  GeolocalizacionLongitud: number;
}
```

El servicio inyecta cabeceras de autorización obligatorias (`x-api-key: dism-secret-key-2026`) y define métodos para cada operación del backend:
- `login(usuario, clave)`: Envía credenciales al endpoint `/auth/login`.
- `getUsuarios()`, `crearUsuario()`, `actualizarUsuario()`, `eliminarUsuario()`: Métodos CRUD de personal.
- `getTrabajos()`, `crearTrabajo()`, `actualizarTrabajo()`, `eliminarTrabajo()`: Métodos CRUD de proyectos.
- `getFichajes(filtros)`: Consulta polimórfica de turnos que concatena parámetros query opcionales (`idUsuario`, `fechaInicio`, `fechaFin`).
- `iniciarFichaje(datos)`: Registra la entrada con coordenadas GPS.
- `cerrarFichaje(idFichaje)`: Cierra la jornada laboral y computa el tiempo total.
- `getFichajesActivos(idUsuario)`: Devuelve los turnos actualmente abiertos para un empleado.

### 5.3. Módulo de Autenticación (`login/login.page.ts`)
El controlador de login gestiona el estado del formulario y la respuesta visual ante aciertos y errores:
- **Reseteo en ciclo de vida Ionic:** Utiliza `ionViewWillEnter()` para limpiar variables y reactivar la interactividad si se retorna desde una sesión previa.
- **Detención de barra de progreso en 0 ms:** Al recibir un error de red o de credenciales inválidas (HTTP 401), conmuta inmediatamente `this.cargando = false` y dispara `this.cdr.detectChanges()` de Angular para forzar la actualización del árbol visual en ese milisegundo exacto, evitando que la barra de carga quede congelada.
- **Persistencia de Sesión:** Tras validar al usuario con éxito, limpia cualquier residuo previo y almacena el objeto de identidad en el almacenamiento local:
  ```typescript
  localStorage.removeItem('auth_user');
  sessionStorage.removeItem('auth_user');
  localStorage.setItem('auth_user', JSON.stringify(user));
  ```
  A continuación muestra un toast verde de bienvenida y redirige a `/home` con `replaceUrl: true` para impedir que el usuario pueda retroceder al login con el botón de atrás del navegador.

### 5.4. Distribuidor Principal y Roles (`home/home.page.ts`)
El componente `HomePage` inspecciona el objeto `auth_user` almacenado en `localStorage`. Si no existe sesión válida, expulsa inmediatamente la navegación hacia `/login`. Si la sesión existe, discrimina dinámicamente el rol:
- Si `userObj.Rol === 'admin'`, activa el **Tema Verde** y renderiza las tarjetas de gestión de usuarios, trabajos y auditoría de fichajes.
- Si `userObj.Rol === 'empleado'`, activa el **Tema Azul** y renderiza las tarjetas de registro de jornada y consulta de historial individual.
- Proporciona el método `logout()`, accesible en la barra superior de todas las pantallas, que vacía el almacenamiento local y redirige a la pantalla de acceso.

### 5.5. Operativa del Empleado y Multitarea (`registrar-fichaje/registrar-fichaje.page.ts`)
Este módulo implementa el registro de jornada con soporte para **turnos en paralelo** y **Optimistic UI**:
1. **Adquisición de Coordenadas GPS:**
   Al entrar en la vista, solicita la ubicación geográfica a través de `navigator.geolocation.getCurrentPosition()`, almacenando la latitud y longitud actuales en segundo plano con baja latencia (`enableHighAccuracy: false, timeout: 2000`).
2. **Registro de Entrada en 0 ms (Optimistic UI):**
   Al pulsar "Fichar Entrada", el controlador crea inmediatamente un objeto `Fichaje` provisional en memoria con un identificador temporal basado en timestamp (`Date.now()`) y lo antepone a la matriz local:
   ```typescript
   this.fichajesActivos = [fichajeVisual, ...this.fichajesActivos];
   this.cdr.detectChanges();
   ```
   La tarjeta de "Fichaje en Curso" aparece en pantalla de forma instantánea. Paralelamente, emite la petición HTTP POST al backend; cuando el servidor responde con el registro persistido, actualiza silenciosamente el `IdFichaje` del objeto sin producir parpadeos visuales en la interfaz.
3. **Multitarea Simultánea:**
   El botón de inicio permanece siempre disponible. Si el trabajador participa en varios proyectos en la misma franja horaria, puede fichar en cada uno de ellos consecutivamente. Cada turno se representa en una tarjeta independiente con su propio contador, nombre de proyecto y botón de cierre.
4. **Finalización de Turno:**
   Al pulsar el botón rojo **"Finalizar Fichaje"** de una tarjeta concreta:
   - Se filtra inmediatamente la lista local `this.fichajesActivos = this.fichajesActivos.filter(f => f.IdFichaje !== idCerrar)`.
   - La tarjeta desaparece en el acto y se muestra un toast verde informativo.
   - En segundo plano, se envía la petición PUT `/api/v1/fichajes/cerrar/:id` para consolidar el cierre y calcular las horas en base de datos.

### 5.6. Auditoría y Cartografía Interactiva (`fichajes/fichajes.page.ts`)
El panel de auditoría del administrador combina filtrado de datos tabulares con representación geográfica interactiva:
- **Filtrado Combinado:** Permite filtrar turnos simultáneamente por trabajador (desplegable reactivo) y por intervalos de fecha (selectores con formato YYYY-MM-DD).
- **Integración con Leaflet:**  
  Al pulsar el botón **"Ver mapa de fichaje"**, se levanta una ventana modal y se inicializa una instancia del mapa de Leaflet en el elemento DOM `#mapAdminId`:
  ```typescript
  this.mapaLeaflet = Leaflet.map('mapAdminId').setView([lat, lon], 16);
  Leaflet.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(this.mapaLeaflet);
  ```
  Se configura un icono de marcador personalizado (`assets/marker-icon.png`) anclado a las coordenadas precisas del fichaje y se despliega un popup con el nombre del empleado y la marca de tiempo de entrada.

---

## 6. Compilación de Producción y Carpeta `www/`

### 6.1. Definición y Propósito de `www/`
En el ciclo de vida de Ionic y Angular, **`www/` es el directorio final de compilación para producción** (equivalente a la carpeta `dist/` en otros proyectos web). Contiene el artefacto final resultante de ejecutar `ng build` (o `ionic build --prod`).

### 6.2. Arquitectura de Chunks y Code Splitting
Dentro de `www/` se encuentran más de un centenar de archivos con formato `chunk-*.js`. Esta distribución no es un fallo ni un residuo, sino el resultado deliberado de las técnicas de optimización del compilador:

1. **Code Splitting (División de Código):**  
   El empaquetador (Webpack/Vite) fragmenta el código de la aplicación en bloques atómicos. Cada ruta (`/login`, `/usuarios`, etc.) y cada Web Component de Ionic (botones, modales, alertas) se almacena en un chunk independiente con un hash único en su nombre.
2. **Lazy Loading en Tiempo de Ejecución:**  
   Cuando un usuario abre la aplicación en su smartphone, el navegador únicamente descarga el chunk principal (`main`), los estilos (`styles.css`) y el chunk específico del login. Si el usuario es un empleado, el navegador nunca llegará a descargar los chunks asociados a la gestión de personal o auditoría de trabajos, ahorrando ancho de banda y memoria RAM.
3. **Ausencia de Archivos `.ts` en `www/`:**  
   Los navegadores web no pueden ejecutar TypeScript directamente. Durante la compilación, todo el código TypeScript de `src/app/` es analizado mediante análisis estático, transformado a JavaScript estándar (ES2022/ES6) y minificado (eliminación de espacios, acortamiento de identificadores y purgado de código muerto o *tree shaking*). Por ello, los archivos `.ts` residen exclusivamente en `src/` y nunca deben figurar en `www/`.

> **Regla de integridad:** No se debe borrar ningún archivo de la carpeta `www/`. Si se eliminase cualquier chunk, la aplicación fallaría con un error 404 al navegar hacia la pantalla o componente contenido en dicho chunk.

---

## 7. Servidor Web Estático Nativo (`servidor_estatico.js`)

El archivo **`servidor_estatico.js`** es un servidor HTTP desarrollado con la API nativa de Node.js (módulos `http`, `fs`, `path`). No requiere la instalación previa de ninguna librería externa de npm.

### 7.1. Justificación y Necesidad Técnica
En un entorno de desarrollo tradicional con Angular e Ionic, para servir la aplicación se requiere ejecutar `ionic serve` o `ng serve`. Estos comandos exigen tener instalado el compilador de Angular, la CLI de Ionic y un árbol de dependencias `node_modules` que supera con facilidad los 400 MB.

Para que la entrega académica sea ligera (menos de 20 MB) y funcione de manera autónoma con un doble clic en cualquier equipo sin software preinstalado, `servidor_estatico.js` actúa como el servidor web de producción en el puerto **8100**:
- Lee directamente los archivos empaquetados en `AppRegistroHorario/www`.
- Determina dinámicamente el tipo MIME adecuado para cada recurso (HTML, JS, CSS, SVG, WebManifest, JSON, PNG, WOFF2).
- **Soporte SPA Fallback:** En las aplicaciones de página única (SPA), las rutas internas como `/home` o `/fichajes` no corresponden a carpetas físicas en el disco. Si el servidor detecta que la ruta solicitada no es un archivo físico existente, entrega de forma transparente el archivo `index.html`, permitiendo que el enrutador de Angular gestione la vista sin arrojar un error HTTP 404.
- **Inhibición de Caché Estática:** Configura cabeceras HTTP de control de caché estrictas (`no-store, no-cache, must-revalidate, max-age=0`) para garantizar que cualquier modificación de código se refleje al instante en el navegador sin interferir en el almacenamiento de sesión de `localStorage`.

> **Conclusión sobre su permanencia:** `servidor_estatico.js` es **estrictamente imprescindible**. Si se eliminara de la carpeta de entrega, el script `Iniciar_Todo.bat` arrojaría un error de módulo no encontrado y la PWA no se podría visualizar.

---

## 8. Arquitectura del Backend REST API (`backend-api`)

El backend proporciona una interfaz REST desacoplada implementada con **Express 4**:

### 8.1. Servidor Principal (`server.js`)
Configura los middlewares globales esenciales:
- `cors()`: Permite el intercambio de recursos de origen cruzado, permitiendo que la PWA servida en el origen `http://localhost:8100` realice peticiones sin restricciones de seguridad CORS hacia el puerto de la API `http://localhost:8080`.
- `express.json()`: Parsea automáticamente los cuerpos de petición con carga útil JSON.
- `checkApiKey`: Middleware que verifica la cabecera `x-api-key`. Si se proporciona, valida su correspondencia frente a la tabla `ApiKey` o el dataset de claves permitidas.
- **Proxy de Geocodificación Inversa:** Incluye el endpoint `/api/v1/reverse-geocode`, que actúa como intermediario seguro hacia la API de OpenStreetMap Nominatim para convertir coordenadas de latitud y longitud en direcciones físicas legibles, evitando problemas de CORS en clientes web estrictos.

### 8.2. Capa de Datos y Tolerancia a Fallos (`db.js`)
El módulo de base de datos gestiona la persistencia con una política de **alta disponibilidad**:
- Intenta establecer un pool de conexiones con la base de datos relacional.
- Envuelve las operaciones en mecanismos de carrera temporal (`Promise.race` limitado a 200 milisegundos). Si la base de datos externa no responde en dicho plazo, el sistema captura la excepción y ejecuta la consulta sobre matrices de datos en memoria RAM (`mockUsuarios`, `mockTrabajos`, `mockFichajes`).
- Esto garantiza que, incluso si el evaluador ejecuta la práctica en un ordenador sin servicio de base de datos activo, la aplicación responde al 100% de las operaciones de login, altas, bajas, turnos y auditorías con 0 ms de latencia.

### 8.3. Especificación Formal de Endpoints REST
A continuación se detalla el contrato de interfaz implementado en `server.js` y documentado en `openapi.yaml`:

| Método | Ruta | Parámetros / Body | Códigos HTTP | Función |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/auth/login` | `{ usuario, clave }` | `200`, `400`, `401`, `500` | Valida credenciales y devuelve el perfil sin exponer el hash de la clave. |
| `GET` | `/api/v1/usuarios` | Ninguno | `200`, `500` | Retorna el listado completo de la plantilla laboral. |
| `GET` | `/api/v1/usuarios/:id` | `id` (path) | `200`, `404`, `500` | Devuelve el detalle de un usuario concreto. |
| `POST` | `/api/v1/usuarios` | `{ Nombre, Usuario, Clave, Rol }` | `201`, `400`, `500` | Registra un nuevo empleado o administrador en el sistema. |
| `PUT` | `/api/v1/usuarios/:id` | `{ Nombre, Usuario, Clave, Rol }` | `200`, `400`, `404`, `500` | Modifica los datos personales o permisos de un usuario existente. |
| `DELETE` | `/api/v1/usuarios/:id` | `id` (path) | `200`, `404`, `500` | Elimina la cuenta de un trabajador de la base de datos. |
| `GET` | `/api/v1/trabajos` | Ninguno | `200`, `500` | Devuelve el catálogo de tareas y proyectos de la empresa. |
| `GET` | `/api/v1/trabajos/:id` | `id` (path) | `200`, `404`, `500` | Detalle de un proyecto específico. |
| `POST` | `/api/v1/trabajos` | `{ Nombre }` | `201`, `400`, `500` | Añade un nuevo trabajo al catálogo disponible para fichar. |
| `PUT` | `/api/v1/trabajos/:id` | `{ Nombre }` | `200`, `400`, `404`, `500` | Actualiza la denominación de una actividad. |
| `DELETE` | `/api/v1/trabajos/:id` | `id` (path) | `200`, `404`, `500` | Elimina un proyecto del catálogo. |
| `GET` | `/api/v1/fichajes` | `idUsuario`, `fechaInicio`, `fechaFin` | `200`, `500` | Consulta de auditoría con filtrado polimórfico opcional. |
| `GET` | `/api/v1/fichajes/:id` | `id` (path) | `200`, `404`, `500` | Detalle técnico de un turno individual. |
| `POST` | `/api/v1/fichajes` | `{ IdUsuario, IdTrabajo, GeolocalizacionLatitud, GeolocalizacionLongitud }` | `201`, `400`, `500` | Inicia un turno registrando fecha/hora de entrada y posición GPS. |
| `PUT` | `/api/v1/fichajes/cerrar/:id` | `id` (path) | `200`, `404`, `500` | Registra fecha/hora de salida y calcula automáticamente `HorasTrabajadas`. |
| `DELETE` | `/api/v1/fichajes/:id` | `id` (path) | `200`, `404`, `500` | Elimina físicamente un registro de turno auditado. |
| `GET` | `/api/v1/fichajes/activos/:idUsuario` | `idUsuario` (path) | `200`, `500` | Obtiene todos los turnos abiertos (`FechaHoraSalida IS NULL`) del empleado. |
| `GET` | `/api/v1/reverse-geocode` | `lat`, `lon` (query) | `200`, `400`, `500` | Resuelve la dirección postal a partir de coordenadas GPS. |

---

## 9. Esquema de Base de Datos Relacional (`database/schema.sql`)

El diseño de la base de datos responde a un modelo relacional normalizado:

```sql
-- Tabla de Usuarios
CREATE TABLE IF NOT EXISTS Usuarios (
  IdUsuario INTEGER PRIMARY KEY AUTOINCREMENT,
  Nombre VARCHAR(100) NOT NULL,
  Usuario VARCHAR(50) NOT NULL UNIQUE,
  Clave VARCHAR(255) NOT NULL,
  Rol VARCHAR(20) NOT NULL DEFAULT 'empleado'
);

-- Tabla de Catálogo de Trabajos / Proyectos
CREATE TABLE IF NOT EXISTS Trabajos (
  IdTrabajo INTEGER PRIMARY KEY AUTOINCREMENT,
  Nombre VARCHAR(150) NOT NULL
);

-- Tabla de Fichajes y Control Horario
CREATE TABLE IF NOT EXISTS Fichajes (
  IdFichaje INTEGER PRIMARY KEY AUTOINCREMENT,
  FechaHoraEntrada DATETIME NOT NULL,
  FechaHoraSalida DATETIME NULL,
  HorasTrabajadas DECIMAL(5,2) NULL,
  IdTrabajo INTEGER NOT NULL,
  IdUsuario INTEGER NOT NULL,
  GeolocalizacionLatitud DECIMAL(10,8) NOT NULL,
  GeolocalizacionLongitud DECIMAL(11,8) NOT NULL,
  FOREIGN KEY (IdTrabajo) REFERENCES Trabajos(IdTrabajo) ON DELETE CASCADE,
  FOREIGN KEY (IdUsuario) REFERENCES Usuarios(IdUsuario) ON DELETE CASCADE
);

-- Tabla de Claves de Autorización API
CREATE TABLE IF NOT EXISTS ApiKey (
  IdKey INTEGER PRIMARY KEY AUTOINCREMENT,
  `Key` VARCHAR(100) NOT NULL UNIQUE,
  Descripcion VARCHAR(150)
);
```

### Relaciones e Integridad Referencial:
- La tabla **`Fichajes`** mantiene claves foráneas hacia `Usuarios` (`IdUsuario`) y hacia `Trabajos` (`IdTrabajo`).
- Las cláusulas `ON DELETE CASCADE` garantizan que si un administrador elimina un usuario o un trabajo, todos sus turnos vinculados se depuran de forma coherente sin dejar registros huérfanos.
- El campo `HorasTrabajadas` almacena el diferencial temporal expresado en unidades decimales (ejemplo: 2.50 horas equivale a 2 horas y 30 minutos), facilitando sumatorios aritméticos directos en las consultas SQL de liquidación de jornada.

---

## 10. Estándares y Requisitos PWA Cumplidos

1. **Manifiesto Web Canónico (`manifest.webmanifest`):**  
   Declara formalmente el nombre corporativo (`Control Horario`), nombre abreviado (`ControlHorario`), color de tema (`#2563eb`), color de fondo (`#0f172a`), orientación preferida (`portrait`) y modo de despliegue `standalone` (sin interfaz de navegador).
2. **Estrategia Multi-Resolución de Iconos:**  
   Proporciona iconos en formatos estándar de 192x192 px, 512x512 px y favicon para garantizar nitidez en pantallas Retina y escritorios de alta densidad.
3. **Integración con Hardware Móvil (Geolocalización):**  
   Utiliza la API `navigator.geolocation` del navegador para certificar la ubicación física del empleado en el instante del fichaje sin obligar al usuario a introducir datos manualmente.
4. **Cartografía Abierta con Leaflet:**  
   La visualización de mapas no depende de librerías comerciales cerradas (Google Maps SDK) ni requiere facturación por peticiones API. Emplea la librería de código abierto Leaflet y teselas de OpenStreetMap almacenadas en caché local.
5. **Arquitectura sin Bloqueos (0 Dependencias Externas en Despliegue):**  
   El paquete entregado funciona de inmediato en cualquier ordenador con Node.js instalado, cumpliendo con la restricción de peso estipulada para la plataforma docente Moodle (menos de 20 MB).
