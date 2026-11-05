# Práctica 2 (Entrega 2) - Sistema Unificado de Registro Horario (PWA)

Solución completa de la **Entrega 2 (Práctica 2)** de la asignatura **DISM (Desarrollo de Interfaces para Sistemas Móviles)**.

Se han unificado todas las funcionalidades en una **única aplicación Ionic Progresiva (PWA)** multiplataforma, con control de acceso por roles (Administrador y Empleado), control de turnos en menos de 12 horas, geolocalización GPS y persistencia en base de datos MySQL mediante servicios REST OpenAPI 3.0.

---

## 🚀 Puesta en Marcha Inmediata (Sin Instalaciones)

Esta carpeta está completamente compilada y preparada con todas las dependencias locales incluidas, por lo que **no es necesario ejecutar ningún comando de instalación (`npm install`)**:

1. Haz doble clic en el archivo **`iniciar_todo.bat`** (o `iniciar_practica2.bat`).
2. Automáticamente se levantarán:
   - **Backend REST API**: en el puerto `8080` (con documentación interactiva en `http://localhost:8080/api-docs/`).
   - **Servidor Web PWA**: en el puerto `8100` (`http://localhost:8100`).
3. El navegador predeterminado se abrirá automáticamente en ambas direcciones.
4. Para abrir la aplicación en modo ventana nativa PWA (sin barra de navegador), puedes hacer doble clic en **`Abrir_PWA.bat`**.

---

## 📱 Dónde está la PWA Compilada (Para Enseñar a la Profesora)

Siguiendo al pie de la letra la guía oficial de la asignatura (*Procedimiento para crear una App PWA desde Ionic*):

La PWA compilada se encuentra directamente en la carpeta:
👉 **`PWA_Compilada/`** (y en `AppRegistroHorario/www/`)

Dentro de esta carpeta se encuentran todos los artefactos exigidos:
- **`manifest.webmanifest`** y **`manifest.json`**: Manifiesto web con el nombre de la app, modo de pantalla `standalone`, color de fondo `#f1f5f9` y definición de iconos.
- **`sw.js`** y **`ngsw-worker.js`**: Service Worker registrado para el control de ciclo de vida, soporte offline y cacheo inteligente de recursos.
- **`icons/`**: Carpeta con los iconos oficiales en todas las resoluciones estándar (`72x72`, `96x96`, `128x128`, `144x144`, `152x152`, `192x192`, `384x384`, `512x512`).
- **`index.html`**: Punto de entrada con las etiquetas `<link rel="manifest">`, meta tags de compatibilidad móvil y script de registro del Service Worker.
- **Bundles JS y CSS**: Todos los módulos Angular e Ionic compilados para producción.

### Icono de Instalación PWA en el Navegador
Al abrir `http://localhost:8100` en Google Chrome o Microsoft Edge:
- En el extremo derecho de la barra de direcciones (omnibox) aparece el icono nativo de **"Instalar aplicación"** (un monitor con flecha de descarga o símbolo de suma).
- Al pulsar dicho icono, el sistema operativo instala la app y crea el acceso directo nativo en tu ordenador.
- También se incluye en la barra superior de la app el botón **"Instalar PWA"** que lanza el prompt de instalación directamente.

---

## 🔐 Control de Acceso y Funcionalidades por Rol

La pantalla de acceso cuenta con un diseño limpio, profesional y neutro en **estilo gris**:

### Credenciales Disponibles:
- **Administrador**:
  - Usuario: `admin` | Contraseña: `admin123`
  - Al iniciar sesión accede al panel de administración:
    - **Usuarios**: Consulta, inserción, actualización y borrado (CRUD).
    - **Trabajos**: Catálogo de proyectos y tareas asignables (CRUD).
    - **Fichajes**: Auditoría global de fichajes con filtros por usuario y rango de fechas, y botón para visualizar la ubicación del fichaje en un **mapa interactivo**.
- **Empleado / Trabajador**:
  - Usuario: `sergio` | Contraseña: `1234`
  - Usuario: `lucia`  | Contraseña: `1234`
  - Al iniciar sesión accede al portal del trabajador:
    - **Fichar**: Detección automática de turno en las últimas 12 horas. Si no hay turno abierto, permite seleccionar trabajo e iniciar jornada capturando coordenadas GPS y dirección física. Si hay un turno abierto (<12h), permite cerrar el fichaje calculando las horas trabajadas.
    - **Mis Fichajes**: Listado de fichajes del día y consulta histórica con filtro de fechas.
    - **Mi Perfil**: Resumen de datos y cierre de sesión seguro.

---

## 📁 Estructura de la Carpeta

```text
Practica_2/
├── iniciar_practica2.bat     # Script interactivo de arranque
├── Abrir_PWA.bat             # Abre la app directamente en ventana PWA nativa
├── servidor_estatico.js      # Servidor HTTP Node.js para servir la PWA al instante
├── README.md                 # Esta documentacion
├── backend-api/              # Servidor REST Node.js con OpenAPI y dependencias preinstaladas
│   ├── openapi.yaml
│   ├── server.js
│   └── node_modules/
├── database/                 # Script SQL con estructura y datos demo
│   └── schema.sql
└── AppRegistroHorario/       # Proyecto fuente Ionic con su bundle www/
    └── www/                  # Compilacion de produccion
```
