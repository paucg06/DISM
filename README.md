# 📱 DISM - Práctica 1: Sistema de Registro Horario y Fichajes
> **Universidad de Alicante** | Curso Académico 2026-2027  
> **Entrega 1 Oficial:** Base de Datos MySQL, Servicios Web REST (Node.js/Express + OpenAPI 3.0) y AppAdmin (Ionic / Angular).

---

## 🎯 Acceso Directo: ENTREGA 1
La carpeta principal para la corrección y evaluación de la Entrega 1 es:
👉 **[`Entrega1_RegistroHorario/`](./Entrega1_RegistroHorario/)**

Dentro encontrarás la [Memoria Técnica detallada](./Entrega1_RegistroHorario/README.md) y el lanzador automático `iniciar_entrega1.bat`.

### 📂 Contenido de la Entrega 1:
```text
Entrega1_RegistroHorario/
├── database/
│   └── schema.sql              # Script MySQL DDL y datos de prueba (Usuarios, Trabajos, Fichajes, ApiKey)
├── backend-api/                # API REST Node.js / Express con OpenAPI 3.0
│   ├── openapi.yaml            # Especificación formal OpenAPI 3.0 (Swagger UI en /api-docs)
│   ├── server.js               # Servidor Express, endpoints CRUD, login y x-api-key
│   ├── db.js                   # Conexión MySQL2 con fallback resiliente en memoria
│   └── package.json            # Dependencias
├── AppAdmin/                   # Aplicación Ionic / Angular para Administradores
│   ├── src/app/login/          # Login de Administrador con validación en BD
│   ├── src/app/home/           # Menú principal con los 3 módulos requeridos
│   ├── src/app/usuarios/       # Gestión de Usuarios: CRUD completo + modal detalle
│   ├── src/app/trabajos/       # Gestión de Trabajos: CRUD completo + modal detalle
│   ├── src/app/fichajes/       # Filtro por usuario/fechas (searchbar) + Mapa interactivo Leaflet
│   └── src/app/services/api.ts # Servicio HTTP inyectando cabecera x-api-key
├── iniciar_entrega1.bat         # Script para instalar dependencias y arrancar con 1 clic
└── README.md                   # Memoria Técnica completa para la defensa
```

---

## 🚀 Puesta en Marcha Rápida (Entrega 1)

### Opción 1: Con el lanzador automatizado
Ejecuta el archivo:
📁 **`Entrega1_RegistroHorario/iniciar_entrega1.bat`**
- Opción `[4]`: Instala dependencias (`npm install`).
- Opción `[1]`: Arranca el servidor Backend (puerto 8080 y Swagger UI interactivo).
- Opción `[2]`: Arranca la AppAdmin en `http://localhost:8100`.

### Opción 2: Manual por consola
```bash
# 1. Arrancar Backend REST API (Node.js)
cd Entrega1_RegistroHorario/backend-api
npm install
npm start
# Swagger UI disponible en: http://localhost:8080/api-docs

# 2. Arrancar AppAdmin (Ionic)
cd Entrega1_RegistroHorario/AppAdmin
npm install
ionic serve
# Aplicación disponible en: http://localhost:8100
```

---

## 📁 Prácticas Guiadas del Curso (DISM 0 a 10)
Todos los ejercicios previos guiados realizados a lo largo de las sesiones se encuentran organizados y archivados en:
👉 **[`Practicas_Guiadas_DISM0_10/`](./Practicas_Guiadas_DISM0_10/)**
- Contiene los ejercicios `DISM0` a `DISM10`, los `Anexos` y el documento de estudio `RESUMEN_PRACTICAS.md`.
