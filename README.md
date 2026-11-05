# DISM - Desarrollo de Interfaces para Sistemas Móviles
## Sistema de Registro Horario y Control de Jornada

Este repositorio contiene las soluciones completas e independientes para las dos entregas de la asignatura:

```text
.
├── Practica_1/        # Entrega 1: Backend REST API + BD MySQL + AppAdmin (Ionic/Angular)
├── Practica_2/        # Entrega 2: Sistema Completo (Backend + BD + AppAdmin + AppUsuarios)
└── README.md          # Índice principal del repositorio
```

---

## 📌 Contenido de las Prácticas

### 📁 [Practica_1 (Entrega 1)](./Practica_1)
- **Base de Datos MySQL**: Esquema relacional con tablas `usuarios`, `trabajos` y `fichajes`.
- **Servicios REST Backend (Node.js / Express)**: Diseñados con OpenAPI 3.0 y Swagger UI interactivo en `http://localhost:8080/api-docs`.
- **AppAdmin (Ionic / Angular)**: Panel de administración para gestión CRUD de usuarios y trabajos, y consulta de fichajes con visualización geográfica mediante mapas Leaflet / OpenStreetMap.
- **Lanzador**: `Practica_1/iniciar_practica1.bat` con opciones de arranque y modo offline.

### 📁 [Practica_2 (Entrega 2)](./Practica_2)
- **Sistema Integral**: Integra tanto la administración como la aplicación móvil del empleado.
- **AppUsuarios (Ionic / Angular)**: Aplicación para trabajadores que permite:
  - Registro de fichaje de entrada asociado a un trabajo.
  - Detección reactiva de turno abierto en menos de 12 horas para proceder al cierre de jornada.
  - Geolocalización GPS en tiempo real con `@capacitor/geolocation` y geocodificación inversa con Nominatim.
  - Histórico de fichajes con filtros por rango de fechas.
- **AppAdmin**: Panel de administración completo.
- **Backend y BD**: Módulo REST centralizado y securizado.
- **Lanzador**: `Practica_2/iniciar_practica2.bat`.

---

## 🚀 Soporte Offline para Equipos de Aula
Cada proyecto contiene un archivo `node_modules.tar.gz` preempaquetado. Si se ejecuta el repositorio en un equipo sin conexión a internet o con restricciones en `npm`, los scripts `.bat` descomprimen las dependencias automáticamente en pocos segundos sin necesidad de descargar nada por red.
