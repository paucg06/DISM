# 📱 DISM - Desarrollo de Interfaces para Sistemas Móviles
> Repositorio de prácticas y ejercicios guiados de la asignatura **Desarrollo de Interfaces para Sistemas Móviles (DISM)**. Universidad de Alicante.

Este repositorio contiene la implementación completa, probada y documentada de los 11 ejercicios (`DISM0` a `DISM10`) y los anexos de servicios REST con Ionic, Angular Standalone, Leaflet, Capacitor, Node.js Express, OpenAPI 3.0 y MySQL.

---

## 📂 Estructura del Repositorio

| Directorio | Ejercicio | Tecnología Principal | Descripción |
| :--- | :--- | :--- | :--- |
| [`DISM0/`](./DISM0) | **Ej. 0: Verificación Entorno** | Ionic CLI + Angular | Proyecto base `tabs` para validar Node.js, npm e Ionic CLI. |
| [`DISM1/`](./DISM1) | **Ej. 1: Componentes UI Tabs** | Ionic Components | `ion-button`, `ion-list` con `@for`, `ion-card` y `ion-toggle`. |
| [`DISM2/`](./DISM2) | **Ej. 2: Menú Lateral (Side)** | `ion-split-pane`, `ion-menu` | Navegación multipágina con menú hamburguesa y botones programáticos. |
| [`DISM3/`](./DISM3) | **Ej. 3: Consumo API Externa** | Angular `HttpClient` | Consumo de la API pública `randomuser.me` con `@for` y `@empty`. |
| [`DISM4/`](./DISM4) | **Ej. 4: Mock Backend Fake REST** | `json-server` | Servidor backend mock local con `db.json` en puerto 3000. |
| [`DISM5/`](./DISM5) | **Ej. 5: CRUD Completo Fake API** | Ionic + Angular + HTTP | Aplicación CRUD completa (`GET`, `POST`, `PUT`, `DELETE`) de Usuarios. |
| [`DISM6/`](./DISM6) | **Ej. 6: Geolocalización GPS** | `@capacitor/geolocation` | Coordenadas GPS y geocodificación inversa con OpenStreetMap Nominatim. |
| [`DISM7/`](./DISM7) | **Ej. 7: Mapas con Leaflet** | `leaflet` + OpenStreetMap | Mapa cartográfico interactivo con marcadores y popups en Alicante y Barcelona. |
| [`DISM8/`](./DISM8) | **Ej. 8: Diseño OpenAPI 3.0** | OpenAPI 3.0 / Swagger | Diseño del contrato YAML (`HolaMundo.yaml`) para el endpoint `/holamundo`. |
| [`DISM9/`](./DISM9) | **Ej. 9: Stub Express OpenAPI** | `@openapitools/generator` | Servidor backend Express generado desde OpenAPI con Swagger UI interactivo. |
| [`DISM10/`](./DISM10) | **Ej. 10: API REST CRUD + MySQL**| Express + OpenAPI + `mysql2` | API REST completa con persistencia en Base de Datos MySQL (`dism.usuarios`). |
| [`Anexos/`](./Anexos) | **Anexos REST** | Node.js + Express + MySQL | Scripts guiados de Express puro (`Ejercicio1.js`, `Ejercicio2.js`, `Ejercicio3.js`). |

---

## 📖 Guía de Estudio y Explicación Detallada

Para una explicación exhaustiva código a código y preguntas frecuentes de examen/defensa, consulta:
👉 **[`RESUMEN_PRACTICAS.md`](./RESUMEN_PRACTICAS.md)**

---

## 🚀 Cómo Ejecutar Cada Práctica

### Prácticas Ionic / Frontend (DISM0, DISM1, DISM2, DISM3, DISM5, DISM6, DISM7)
```bash
cd DISM<numero>
npm install
ionic serve
```
*La aplicación se abrirá automáticamente en `http://localhost:8100/`.*

> **Nota para DISM5:** Requiere tener el servidor mock activo en otra consola:
> ```bash
> cd DISM4
> npx json-server db.json --port 3000
> ```

---

### Servidores Backend OpenAPI & Express (DISM9, DISM10)

#### DISM9 (Hola Mundo OpenAPI)
```bash
cd DISM9
npm install
npm start
```
*Documentación interactiva disponible en `http://localhost:8080/api-docs`.*

#### DISM10 (API CRUD con MySQL)
```bash
# 1. Restaurar la base de datos (mediante MySQL / phpMyAdmin / XAMPP / UniformServer)
# Importar el archivo DISM10/database.sql

# 2. Iniciar el servidor
cd DISM10
npm install
npm start
```
*Documentación y prueba interactiva disponible en `http://localhost:8080/api-docs`.*
