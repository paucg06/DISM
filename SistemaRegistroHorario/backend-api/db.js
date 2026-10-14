const mysql = require('mysql2/promise');

// Configuración de conexión a MySQL
const dbConfig = {
  host: process.env.DB_HOST || 'localhost',
  user: process.env.DB_USER || 'root',
  password: process.env.DB_PASSWORD || 'password', // o 'root' o '' segun instalacion
  database: process.env.DB_NAME || 'dism_registro',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
};

// Datos en memoria como fallback automático si MySQL no está levantado en el equipo del alumno
let mockApiKey = [{ idKey: 1, Key: 'dism-secret-key-2026' }];

let mockTrabajos = [
  { IdTrabajo: 1, Nombre: 'Desarrollo Frontend Ionic' },
  { IdTrabajo: 2, Nombre: 'Auditoría de Sistemas Móviles' },
  { IdTrabajo: 3, Nombre: 'Mantenimiento Base de Datos MySQL' },
  { IdTrabajo: 4, Nombre: 'Soporte y Atención al Cliente' }
];

let mockUsuarios = [
  { IdUsuario: 1, Nombre: 'Administrador General', Usuario: 'admin', Clave: 'admin123', Rol: 'admin' },
  { IdUsuario: 2, Nombre: 'Sergio Garcia', Usuario: 'sergio', Clave: '1234', Rol: 'empleado' },
  { IdUsuario: 3, Nombre: 'Estela Martinez', Usuario: 'estela', Clave: '1234', Rol: 'empleado' },
  { IdUsuario: 4, Nombre: 'Susana Gomez', Usuario: 'susana', Clave: '1234', Rol: 'empleado' },
  { IdUsuario: 5, Nombre: 'Hugo Lopez', Usuario: 'hugo', Clave: '1234', Rol: 'empleado' }
];

let mockFichajes = [
  {
    IdFichaje: 1,
    FechaHoraEntrada: '2026-10-14 08:30:00',
    FechaHoraSalida: '2026-10-14 16:30:00',
    HorasTrabajadas: 8,
    IdTrabajo: 1,
    IdUsuario: 2,
    GeolocalizacionLatitud: 38.38735,
    GeolocalizacionLongitud: -0.51238
  },
  {
    IdFichaje: 2,
    FechaHoraEntrada: '2026-10-14 09:00:00',
    FechaHoraSalida: '2026-10-14 17:00:00',
    HorasTrabajadas: 8,
    IdTrabajo: 2,
    IdUsuario: 3,
    GeolocalizacionLatitud: 38.34599,
    GeolocalizacionLongitud: -0.49068
  }
];

let pool;
try {
  pool = mysql.createPool(dbConfig);
} catch (e) {
  console.warn('[DB] Fallback a memoria activado:', e.message);
}

module.exports = {
  pool,
  mockApiKey,
  mockTrabajos,
  mockUsuarios,
  mockFichajes
};
