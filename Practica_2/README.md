# Práctica 2 (Entrega 2) - Sistema Integral de Registro Horario Unificado (PWA)

Este directorio contiene la solución completa de la **Entrega 2 (Práctica 2)** de la asignatura **DISM (Desarrollo de Interfaces para Sistemas Móviles)**.

Se han unificado todas las funcionalidades en una **única aplicación Ionic Progresiva (PWA)** con soporte multiplataforma, control de acceso basado en roles con **tematización dinámica por colores**, control de turnos en menos de 12 horas, geolocalización GPS y persistencia en base de datos MySQL mediante servicios REST OpenAPI 3.0.

---

## 🎨 Tematización Dinámica según Rol de Usuario

La aplicación unificada detecta automáticamente el perfil del usuario autenticado y transforma su aspecto visual y navegación:

| Perfil | Color Corporativo | Pestañas Disponibles (Tabs) | Funcionalidades Principales |
| :--- | :--- | :--- | :--- |
| **Administrador** | **TEMA AZUL** (`#2563eb`) | `Usuarios`, `Trabajos`, `Fichajes`, `Panel` | CRUD de usuarios y trabajos, auditoría de fichajes de toda la plantilla y visualización en **mapa interactivo Leaflet**. |
| **Empleado** | **TEMA VERDE** (`#16a34a`) | `Fichar`, `Mis Fichajes`, `Mi Perfil` | **Fichaje de entrada con GPS** (Capacitor + HTML5) y geocodificación inversa (**Nominatim**). Detección de turno abierto (<12h) para **fichaje de salida**. Histórico con filtros por fecha. |

---

## 📱 Características de la Progressive Web App (PWA)

Siguiendo el procedimiento oficial de Ionic y Angular PWA:
1. **Manifiesto Web (`manifest.webmanifest`)**:
   - Nombre de la aplicación, colores temáticos (`theme_color: #2563eb`), iconos adaptativos (192x192 y 512x512) y modo de visualización `standalone` (sin barra de navegador).
2. **Service Worker (`sw.js`)**:
   - Cacheo del shell de la aplicación (HTML, CSS, JS, assets) para garantizar carga instantánea y funcionamiento offline.
3. **Instalación como App Nativa**:
   - El navegador muestra el botón de instalación en la barra de direcciones.
   - La propia aplicación incorpora un botón interactivo **"Instalar PWA"** en la barra superior.

---

## 📁 Estructura del Proyecto

```text
Practica_2/
├── backend-api/              # Servidor REST Node.js / Express
│   ├── openapi.yaml          # Especificacion formal OpenAPI 3.0
│   ├── server.js             # Endpoints CRUD, logica de negocio, CORS y API-Key
│   ├── db.js                 # Pool de conexiones MySQL y datos de fallback
│   ├── package.json          # Dependencias del backend
│   └── node_modules/         # Librerias preinstaladas para arranque inmediato
├── database/                 # Scripts SQL
│   └── schema.sql            # Tablas (Usuarios, Trabajos, Fichajes, ApiKey) y datos demo
├── AppRegistroHorario/       # Aplicacion Unificada Ionic / Angular PWA
│   ├── src/                  # Codigo fuente (login, tabs, usuarios, trabajos, fichajes)
│   ├── www/                  # Bundle compilado de produccion con Service Worker y Manifest
│   ├── manifest.webmanifest  # Manifiesto PWA
│   └── sw.js                 # Service Worker PWA
├── servidor_estatico.js      # Servidor HTTP nativo Node.js para servir la PWA al instante
├── iniciar_practica2.bat      # Lanzador en 1 clic
└── README.md                 # Esta documentacion tecnica
```

---

## 🚀 Inicio Rápido (1 Solo Clic)

Ejecuta el archivo:
```cmd
iniciar_practica2.bat
```
Selecciona la opción **`[1] ARRANCAR TODO`**:
- Inicia el Backend en el puerto `8080`.
- Inicia la aplicación web PWA en el puerto `8100`.
- Abre automáticamente en el navegador:
  - **Swagger UI**: [http://localhost:8080/api-docs/](http://localhost:8080/api-docs/)
  - **App PWA**: [http://localhost:8100](http://localhost:8100)

---

## 🔑 Credenciales de Acceso para Demostración

| Usuario | Contraseña | Rol Asignado | Color de la Interfaz |
| :--- | :--- | :--- | :--- |
| `admin` | `admin123` | Administrador | **AZUL** |
| `sergio` | `1234` | Empleado | **VERDE** |
| `estela` | `1234` | Empleado | **VERDE** |
| `juan.perez` | `user123` | Empleado | **VERDE** |

*La pantalla de login incluye botones de acceso rápido para probar ambos roles con un solo clic.*

---

## ⚙️ Cumplimiento de la Rúbrica y Aspectos Optativos

- **CRUD de Usuarios y Trabajos**: Implementado en las pestañas de administración.
- **Detección de Turno previo (< 12 horas)**: Si existe un fichaje sin salida en menos de 12 horas, la pantalla de fichaje muestra los detalles y permite cerrar la salida.
- **Geolocalización GPS y Georreferenciación Inversa**: Captura coordenadas y resuelve la dirección postal física con OpenStreetMap Nominatim.
- **Mapa Leaflet**: Visualización de puntos geográficos de fichaje en la auditoría del administrador.
- **Seguridad**: Cabecera `x-api-key: dism-secret-key-2026` y validación de credenciales en base de datos.
- **PWA**: Manifiesto web, Service Worker e instalabilidad en escritorio y móvil.
