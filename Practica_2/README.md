# Práctica 2 (Entrega 2) - Sistema Integral de Registro Horario

Este directorio contiene la solución completa para la **Entrega 2 (Práctica 2)** de la asignatura **DISM (Desarrollo de Interfaces para Sistemas Móviles)**.

El sistema comprende una arquitectura cliente-servidor desacoplada para el control horario y gestión de partes de trabajo, compuesta por:
1. **Base de Datos Relacional (`MySQL`)**: Persistencia de usuarios, trabajos y registros de fichajes con geolocalización.
2. **Servicios REST Backend (`Node.js + Express`)**: Diseñados formalmente con **OpenAPI 3.0 / Swagger**, documentados interactivamente con **Swagger UI** y securizados con API-Key y control CORS.
3. **App Administrador (`AppAdmin` - Ionic / Angular)**: Panel de control para altas, bajas, modificaciones y consultas (CRUD) de usuarios y trabajos, así como auditoría de fichajes sobre mapa interactivo Leaflet.
4. **App Empleados (`AppUsuarios` - Ionic / Angular)**: Aplicación móvil para los trabajadores con registro de fichaje (entrada/salida), detección automática de turnos en curso (<12h), geoposicionamiento GPS con Capacitor y consulta de histórico con filtros por fecha.

---

## 📁 Estructura del Proyecto

```text
Practica_2/
├── backend-api/                  # Servidor REST Node.js / Express
│   ├── openapi.yaml              # Especificación OpenAPI 3.0 del sistema completo
│   ├── server.js                 # Servidor Express, endpoints y lógica de negocio
│   ├── db.js                     # Pool de conexiones MySQL con promesas
│   ├── package.json              # Configuración y dependencias del backend
│   └── node_modules.tar.gz       # Dependencias empaquetadas para ejecución offline
├── database/                     # Scripts SQL
│   └── schema.sql                # DDL de tablas (usuarios, trabajos, fichajes) y datos demo
├── AppAdmin/                     # Aplicación Ionic/Angular para Administradores (puerto 8100)
│   ├── src/                      # Código fuente (usuarios, trabajos, fichajes con mapas)
│   ├── package.json              # Configuración de dependencias
│   └── node_modules.tar.gz       # Dependencias empaquetadas offline para AppAdmin
├── AppUsuarios/                  # Aplicación Ionic/Angular para Empleados (puerto 8101)
│   ├── src/                      # Código fuente (fichajes, geolocalización Capacitor, historial)
│   ├── package.json              # Configuración de dependencias
│   └── node_modules.tar.gz       # Dependencias empaquetadas offline para AppUsuarios
├── iniciar_practica2.bat          # Lanzador interactivo con soporte offline instantáneo
└── README.md                     # Este documento explicativo
```

---

## 🚀 Inicio Rápido (Lanzador Automatizado)

Para arrancar cualquier parte del sistema sin complicaciones, ejecuta el script interactivo:

```cmd
iniciar_practica2.bat
```

### Menú de opciones disponible:
- **[1] Arrancar Backend REST API**: Inicia el servidor Node.js en `http://localhost:8080` y abre automáticamente Swagger UI.
- **[2] Arrancar AppAdmin**: Inicia la aplicación de administración en `http://localhost:8100`.
- **[3] Arrancar AppUsuarios**: Inicia la aplicación del empleado en `http://localhost:8101`.
- **[4] Abrir Swagger UI**: Abre directamente la documentación interactiva en el navegador.
- **[5] Descomprimir librerías offline**: Si estás en un aula o entorno sin internet o con restricciones en `npm`, este comando extrae de inmediato los paquetes `.tar.gz` locales en segundos.
- **[6] Instalar / Actualizar dependencias con npm**: Para instalaciones online tradicionales.

---

## 🛠️ Requisitos e Instalación Manual

### 1. Base de Datos MySQL
1. Arranca tu servidor MySQL local (XAMPP, WAMP o servicio MySQL).
2. Importa el archivo SQL:
   ```cmd
   mysql -u root -p < database/schema.sql
   ```
   *Se creará la base de datos `DISM` con las tablas `usuarios`, `trabajos` y `fichajes`, además de datos de prueba precargados.*

### 2. Backend REST API
```cmd
cd backend-api
node server.js
```
El servidor escucha en el puerto `8080`. Documentación y pruebas:
- **Swagger UI**: [http://localhost:8080/api-docs](http://localhost:8080/api-docs)

### 3. AppAdmin (Administración)
```cmd
cd AppAdmin
ionic serve --port 8100
```
- Acceso: [http://localhost:8100](http://localhost:8100)
- Credenciales demo: Administrador (`admin` / `admin123`)

### 4. AppUsuarios (Empleados)
```cmd
cd AppUsuarios
ionic serve --port 8101
```
- Acceso: [http://localhost:8101](http://localhost:8101)
- Credenciales demo: Empleados (`juan.perez` / `user123`, `maria.lopez` / `user123`)

---

## 📱 Funcionalidades Implementadas

### A. AppUsuarios (Entrega 2)
1. **Fichaje de Entrada**:
   - Selección del trabajo asignado mediante selector dinámico conectado a la BD.
   - Captura de coordenadas GPS exactas (latitud y longitud) con `@capacitor/geolocation`.
   - Geocodificación inversa automática mediante OpenStreetMap Nominatim para registrar la dirección física del fichaje.
2. **Detección Automática de Turno Abierto (< 12 horas)**:
   - Al entrar en la pantalla de fichaje, la app consulta si el usuario tiene un fichaje de entrada sin hora de salida en un intervalo menor a 12 horas.
   - Si existe, bloquea un nuevo inicio y muestra los datos del turno en curso (trabajo, hora de entrada, ubicación), ofreciendo el botón para **Cerrar Fichaje (Salida)**.
3. **Consulta de Fichajes**:
   - Listado cronológico de fichajes del empleado autenticado.
   - Filtro reactivo por rango de fechas (Fecha Inicio - Fecha Fin).
   - Indicador de estado (fichaje abierto vs. cerrado con duración total calculada).

### B. AppAdmin (Entrega 1 + Gestión Global)
1. **CRUD Completo de Usuarios**: Listado, inserción, edición y eliminación de trabajadores y administradores.
2. **CRUD Completo de Trabajos**: Gestión de obras, proyectos y tareas asignables.
3. **Auditoría de Fichajes**:
   - Filtros por usuario y rango de fechas.
   - Visualización de marcadores de posición sobre mapa Leaflet.
   - Detalle de horas trabajadas y geolocalizaciones de entrada y salida.

---

## 🔐 Seguridad y Aspectos Optativos
- **API Key**: Validación mediante cabecera `x-api-key: dism-secret-key-2026`.
- **CORS Configurado**: Permite peticiones cruzadas seguras desde Ionic en los puertos 8100 y 8101.
- **Validaciones OpenAPI**: Control estricto de esquemas y tipos de datos en todas las operaciones.
