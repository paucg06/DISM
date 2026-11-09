const mysql = require('mysql2/promise');

// Configuración de conexión a MySQL (127.0.0.1 evita demoras DNS/IPv6 en Windows)
const dbConfig = {
  host: process.env.DB_HOST || '127.0.0.1',
  user: process.env.DB_USER || 'root',
  password: process.env.DB_PASSWORD || 'password',
  database: process.env.DB_NAME || 'dism_registro',
  waitForConnections: false,
  connectionLimit: 5,
  queueLimit: 0,
  connectTimeout: 300
};

// Datos en memoria como fallback automático instantáneo
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
  { IdUsuario: 5, Nombre: 'Hugo Lopez', Usuario: 'hugo', Clave: '1234', Rol: 'empleado' },
  { IdUsuario: 6, Nombre: 'Juan Perez', Usuario: 'juan.perez', Clave: 'user123', Rol: 'empleado' },
  { IdUsuario: 7, Nombre: 'Maria Lopez', Usuario: 'maria.lopez', Clave: 'user123', Rol: 'empleado' }
];

const pad = (n) => String(n).padStart(2, '0');
const dHoy = new Date();
const strHoy = `${dHoy.getFullYear()}-${pad(dHoy.getMonth() + 1)}-${pad(dHoy.getDate())}`;

let mockFichajes = [
  {
    IdFichaje: 1,
    FechaHoraEntrada: `${strHoy} 08:30:00`,
    FechaHoraSalida: `${strHoy} 14:30:00`,
    HorasTrabajadas: 6,
    IdTrabajo: 1,
    IdUsuario: 2,
    GeolocalizacionLatitud: 38.38735,
    GeolocalizacionLongitud: -0.51238
  },
  {
    IdFichaje: 2,
    FechaHoraEntrada: '2026-11-08 09:00:00',
    FechaHoraSalida: '2026-11-08 17:00:00',
    HorasTrabajadas: 8,
    IdTrabajo: 2,
    IdUsuario: 2,
    GeolocalizacionLatitud: 38.38735,
    GeolocalizacionLongitud: -0.51238
  },
  {
    IdFichaje: 3,
    FechaHoraEntrada: '2026-11-05 08:00:00',
    FechaHoraSalida: '2026-11-05 16:00:00',
    HorasTrabajadas: 8,
    IdTrabajo: 1,
    IdUsuario: 2,
    GeolocalizacionLatitud: 38.38735,
    GeolocalizacionLongitud: -0.51238
  },
  {
    IdFichaje: 4,
    FechaHoraEntrada: `${strHoy} 09:15:00`,
    FechaHoraSalida: `${strHoy} 17:15:00`,
    HorasTrabajadas: 8,
    IdTrabajo: 3,
    IdUsuario: 3,
    GeolocalizacionLatitud: 38.34599,
    GeolocalizacionLongitud: -0.49068
  },
  {
    IdFichaje: 5,
    FechaHoraEntrada: '2026-11-04 09:00:00',
    FechaHoraSalida: '2026-11-04 17:00:00',
    HorasTrabajadas: 8,
    IdTrabajo: 2,
    IdUsuario: 2,
    GeolocalizacionLatitud: 38.38735,
    GeolocalizacionLongitud: -0.51238
  }
];

let rawPool = null;
let isConnected = false;

try {
  const p = mysql.createPool(dbConfig);
  p.getConnection().then((conn) => {
    conn.release();
    rawPool = p;
    isConnected = true;
    console.log('[DB] Conectado exitosamente a MySQL (dism_registro).');
  }).catch(() => {
    isConnected = false;
    console.log('[DB] MySQL local no disponible. Modo en memoria (Fallback instantaneo) activado.');
  });
} catch {
  isConnected = false;
}

// Wrapper seguro con límite duro de 200 ms: si MySQL tarda más de 0.2 segundos, salta instantáneamente al fallback
const pool = {
  async query(sql, params) {
    if (!isConnected || !rawPool) {
      throw new Error('MySQL offline');
    }
    return Promise.race([
      rawPool.query(sql, params),
      new Promise((_, reject) =>
        setTimeout(() => reject(new Error('MySQL query timeout (>200ms)')), 200)
      )
    ]);
  }
};

module.exports = {
  pool,
  mockApiKey,
  mockTrabajos,
  mockUsuarios,
  mockFichajes
};
