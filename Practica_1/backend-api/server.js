const express = require('express');
const cors = require('cors');
const path = require('path');
const swaggerUi = require('swagger-ui-express');
const YAML = require('yamljs');
const { pool, mockApiKey, mockTrabajos, mockUsuarios, mockFichajes } = require('./db');

const app = express();
const PORT = process.env.PORT || 8080;

app.use(cors());
app.use(express.json());

// Cargar documentación Swagger UI
try {
  const swaggerDocument = YAML.load(path.join(__dirname, 'openapi.yaml'));
  app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));
  console.log('[Swagger] Documentación interactiva en http://localhost:8080/api-docs');
} catch (err) {
  console.warn('[Swagger] Error cargando openapi.yaml:', err.message);
}

// Middleware de validación opcional de ApiKey (header x-api-key)
const checkApiKey = async (req, res, next) => {
  const clientKey = req.headers['x-api-key'];
  if (!clientKey) {
    // Si no se envía x-api-key, permitimos continuar para compatibilidad o pruebas directas
    return next();
  }
  try {
    if (pool) {
      const [rows] = await pool.query('SELECT * FROM ApiKey WHERE `Key` = ?', [clientKey]);
      if (rows.length > 0) return next();
    }
    const found = mockApiKey.find(k => k.Key === clientKey);
    if (found) return next();
    return res.status(403).json({ message: 'ApiKey no válida' });
  } catch (error) {
    next();
  }
};

app.use(checkApiKey);

// -------------------------------------------------------------
// RUTAS DE AUTENTICACIÓN (LOGIN)
// -------------------------------------------------------------
app.post('/api/v1/auth/login', async (req, res) => {
  const { usuario, clave } = req.body;
  if (!usuario || !clave) {
    return res.status(400).json({ message: 'Faltan credenciales (usuario y clave)' });
  }
  try {
    if (pool) {
      try {
        const [rows] = await pool.query('SELECT IdUsuario, Nombre, Usuario, Rol FROM Usuarios WHERE Usuario = ? AND Clave = ?', [usuario, clave]);
        if (rows.length > 0) {
          return res.json(rows[0]);
        }
      } catch (errDB) {
        console.warn('[DB] Fallback login a mockUsuarios:', errDB.message);
      }
    }
    const user = mockUsuarios.find(u => u.Usuario === usuario && u.Clave === clave);
    if (user) {
      const { Clave, ...userData } = user;
      return res.json(userData);
    }
    return res.status(401).json({ message: 'Usuario o contraseña incorrectos' });
  } catch (err) {
    res.status(500).json({ message: 'Error en servidor', error: err.message });
  }
});

// -------------------------------------------------------------
// CRUD DE USUARIOS
// -------------------------------------------------------------
app.get('/api/v1/usuarios', async (req, res) => {
  try {
    if (pool) {
      try {
        const [rows] = await pool.query('SELECT IdUsuario, Nombre, Usuario, Clave, Rol FROM Usuarios ORDER BY IdUsuario ASC');
        return res.json(rows);
      } catch (e) {
        console.warn('[DB] Fallback usuariosGET a mock:', e.message);
      }
    }
    res.json(mockUsuarios);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

app.get('/api/v1/usuarios/:id', async (req, res) => {
  const id = parseInt(req.params.id);
  try {
    if (pool) {
      try {
        const [rows] = await pool.query('SELECT IdUsuario, Nombre, Usuario, Clave, Rol FROM Usuarios WHERE IdUsuario = ?', [id]);
        if (rows.length > 0) return res.json(rows[0]);
      } catch (e) {}
    }
    const user = mockUsuarios.find(u => u.IdUsuario === id);
    if (!user) return res.status(404).json({ message: 'Usuario no encontrado' });
    res.json(user);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

app.post('/api/v1/usuarios', async (req, res) => {
  const { IdUsuario, Nombre, Usuario, Clave, Rol = 'empleado' } = req.body;
  if (!Nombre || !Usuario || !Clave) {
    return res.status(400).json({ message: 'Campos obligatorios incompletos' });
  }
  const id = IdUsuario ? parseInt(IdUsuario) : (mockUsuarios.length > 0 ? Math.max(...mockUsuarios.map(u => u.IdUsuario)) + 1 : 1);
  const newUser = { IdUsuario: id, Nombre, Usuario, Clave, Rol };

  try {
    if (pool) {
      try {
        await pool.query('INSERT INTO Usuarios (IdUsuario, Nombre, Usuario, Clave, Rol) VALUES (?, ?, ?, ?, ?)', [id, Nombre, Usuario, Clave, Rol]);
        return res.status(201).json(newUser);
      } catch (e) {
        console.warn('[DB] Fallback insert usuario a mock:', e.message);
      }
    }
    mockUsuarios.push(newUser);
    res.status(201).json(newUser);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

app.put('/api/v1/usuarios/:id', async (req, res) => {
  const id = parseInt(req.params.id);
  const { Nombre, Usuario, Clave, Rol } = req.body;
  try {
    if (pool) {
      try {
        await pool.query('UPDATE Usuarios SET Nombre = ?, Usuario = ?, Clave = ?, Rol = ? WHERE IdUsuario = ?', [Nombre, Usuario, Clave, Rol || 'empleado', id]);
        return res.json({ IdUsuario: id, Nombre, Usuario, Clave, Rol: Rol || 'empleado' });
      } catch (e) {}
    }
    const idx = mockUsuarios.findIndex(u => u.IdUsuario === id);
    if (idx === -1) return res.status(404).json({ message: 'Usuario no encontrado' });
    mockUsuarios[idx] = { ...mockUsuarios[idx], Nombre, Usuario, Clave, Rol: Rol || mockUsuarios[idx].Rol };
    res.json(mockUsuarios[idx]);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

app.delete('/api/v1/usuarios/:id', async (req, res) => {
  const id = parseInt(req.params.id);
  try {
    if (pool) {
      try {
        await pool.query('DELETE FROM Usuarios WHERE IdUsuario = ?', [id]);
        return res.json({ message: 'Usuario eliminado correctamente' });
      } catch (e) {}
    }
    const idx = mockUsuarios.findIndex(u => u.IdUsuario === id);
    if (idx !== -1) mockUsuarios.splice(idx, 1);
    res.json({ message: 'Usuario eliminado correctamente' });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// -------------------------------------------------------------
// CRUD DE TRABAJOS
// -------------------------------------------------------------
app.get('/api/v1/trabajos', async (req, res) => {
  try {
    if (pool) {
      try {
        const [rows] = await pool.query('SELECT * FROM Trabajos ORDER BY IdTrabajo ASC');
        return res.json(rows);
      } catch (e) {}
    }
    res.json(mockTrabajos);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

app.get('/api/v1/trabajos/:id', async (req, res) => {
  const id = parseInt(req.params.id);
  try {
    if (pool) {
      try {
        const [rows] = await pool.query('SELECT * FROM Trabajos WHERE IdTrabajo = ?', [id]);
        if (rows.length > 0) return res.json(rows[0]);
      } catch (e) {}
    }
    const item = mockTrabajos.find(t => t.IdTrabajo === id);
    if (!item) return res.status(404).json({ message: 'Trabajo no encontrado' });
    res.json(item);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

app.post('/api/v1/trabajos', async (req, res) => {
  const { IdTrabajo, Nombre } = req.body;
  if (!Nombre) return res.status(400).json({ message: 'Nombre de trabajo obligatorio' });
  const id = IdTrabajo ? parseInt(IdTrabajo) : (mockTrabajos.length > 0 ? Math.max(...mockTrabajos.map(t => t.IdTrabajo)) + 1 : 1);
  const newTrabajo = { IdTrabajo: id, Nombre };

  try {
    if (pool) {
      try {
        await pool.query('INSERT INTO Trabajos (IdTrabajo, Nombre) VALUES (?, ?)', [id, Nombre]);
        return res.status(201).json(newTrabajo);
      } catch (e) {}
    }
    mockTrabajos.push(newTrabajo);
    res.status(201).json(newTrabajo);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

app.put('/api/v1/trabajos/:id', async (req, res) => {
  const id = parseInt(req.params.id);
  const { Nombre } = req.body;
  try {
    if (pool) {
      try {
        await pool.query('UPDATE Trabajos SET Nombre = ? WHERE IdTrabajo = ?', [Nombre, id]);
        return res.json({ IdTrabajo: id, Nombre });
      } catch (e) {}
    }
    const idx = mockTrabajos.findIndex(t => t.IdTrabajo === id);
    if (idx === -1) return res.status(404).json({ message: 'Trabajo no encontrado' });
    mockTrabajos[idx].Nombre = Nombre;
    res.json(mockTrabajos[idx]);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

app.delete('/api/v1/trabajos/:id', async (req, res) => {
  const id = parseInt(req.params.id);
  try {
    if (pool) {
      try {
        await pool.query('DELETE FROM Trabajos WHERE IdTrabajo = ?', [id]);
        return res.json({ message: 'Trabajo eliminado correctamente' });
      } catch (e) {}
    }
    const idx = mockTrabajos.findIndex(t => t.IdTrabajo === id);
    if (idx !== -1) mockTrabajos.splice(idx, 1);
    res.json({ message: 'Trabajo eliminado correctamente' });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// -------------------------------------------------------------
// FICHAJES (REGISTRO, CONSULTA, CÁLCULO DE 12 HORAS)
// -------------------------------------------------------------

// Helper para enriquecer fichaje con nombres de usuario y trabajo
const enriquecerFichajes = (fichajes) => {
  return fichajes.map(f => {
    const usuario = mockUsuarios.find(u => u.IdUsuario === f.IdUsuario);
    const trabajo = mockTrabajos.find(t => t.IdTrabajo === f.IdTrabajo);
    return {
      ...f,
      NombreUsuario: usuario ? usuario.Nombre : `Usuario #${f.IdUsuario}`,
      NombreTrabajo: trabajo ? trabajo.Nombre : `Trabajo #${f.IdTrabajo}`
    };
  });
};

// Listar fichajes con filtros opcionales (idUsuario, fechaInicio, fechaFin)
app.get('/api/v1/fichajes', async (req, res) => {
  const { idUsuario, fechaInicio, fechaFin } = req.query;
  try {
    if (pool) {
      try {
        let sql = `
          SELECT f.*, u.Nombre AS NombreUsuario, t.Nombre AS NombreTrabajo
          FROM Fichajes f
          JOIN Usuarios u ON f.IdUsuario = u.IdUsuario
          JOIN Trabajos t ON f.IdTrabajo = t.IdTrabajo
          WHERE 1=1
        `;
        const params = [];
        if (idUsuario) {
          sql += ' AND f.IdUsuario = ?';
          params.push(parseInt(idUsuario));
        }
        if (fechaInicio) {
          sql += ' AND DATE(f.FechaHoraEntrada) >= ?';
          params.push(fechaInicio);
        }
        if (fechaFin) {
          sql += ' AND DATE(f.FechaHoraEntrada) <= ?';
          params.push(fechaFin);
        }
        sql += ' ORDER BY f.FechaHoraEntrada DESC';
        const [rows] = await pool.query(sql, params);
        return res.json(rows);
      } catch (e) {
        console.warn('[DB] Fallback fichajes a mock:', e.message);
      }
    }

    let resultado = [...mockFichajes];
    if (idUsuario) {
      resultado = resultado.filter(f => f.IdUsuario === parseInt(idUsuario));
    }
    if (fechaInicio) {
      resultado = resultado.filter(f => f.FechaHoraEntrada.substring(0, 10) >= fechaInicio);
    }
    if (fechaFin) {
      resultado = resultado.filter(f => f.FechaHoraEntrada.substring(0, 10) <= fechaFin);
    }
    resultado.sort((a, b) => new Date(b.FechaHoraEntrada) - new Date(a.FechaHoraEntrada));
    res.json(enriquecerFichajes(resultado));
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Comprobar si el usuario tiene un fichaje abierto en las últimas 12 horas
app.get('/api/v1/fichajes/ultimo-activo/:idUsuario', async (req, res) => {
  const idUsuario = parseInt(req.params.idUsuario);
  try {
    const ahora = new Date();
    const limite12h = new Date(ahora.getTime() - 12 * 60 * 60 * 1000);

    if (pool) {
      try {
        const sql = `
          SELECT f.*, u.Nombre AS NombreUsuario, t.Nombre AS NombreTrabajo
          FROM Fichajes f
          JOIN Usuarios u ON f.IdUsuario = u.IdUsuario
          JOIN Trabajos t ON f.IdTrabajo = t.IdTrabajo
          WHERE f.IdUsuario = ? AND f.FechaHoraSalida IS NULL AND f.FechaHoraEntrada >= ?
          ORDER BY f.FechaHoraEntrada DESC LIMIT 1
        `;
        const [rows] = await pool.query(sql, [idUsuario, limite12h]);
        if (rows.length > 0) return res.json(rows[0]);
        return res.json(null);
      } catch (e) {}
    }

    const activo = mockFichajes.find(f => {
      if (f.IdUsuario !== idUsuario) return false;
      if (f.FechaHoraSalida !== null) return false;
      const fEntrada = new Date(f.FechaHoraEntrada);
      return fEntrada >= limite12h;
    });

    if (activo) {
      const enriched = enriquecerFichajes([activo])[0];
      return res.json(enriched);
    }
    return res.json(null);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Iniciar fichaje (Entrada con GPS y Trabajo seleccionado)
app.post('/api/v1/fichajes', async (req, res) => {
  const { IdUsuario, IdTrabajo, GeolocalizacionLatitud, GeolocalizacionLongitud } = req.body;
  if (!IdUsuario || !IdTrabajo) {
    return res.status(400).json({ message: 'IdUsuario e IdTrabajo son obligatorios' });
  }

  const pad = (n) => String(n).padStart(2, '0');
  const d = new Date();
  const fechaHoraEntrada = `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;

  const lat = GeolocalizacionLatitud !== undefined ? parseFloat(GeolocalizacionLatitud) : 38.38735;
  const lon = GeolocalizacionLongitud !== undefined ? parseFloat(GeolocalizacionLongitud) : -0.51238;

  try {
    if (pool) {
      try {
        const [result] = await pool.query(
          'INSERT INTO Fichajes (FechaHoraEntrada, IdTrabajo, IdUsuario, GeolocalizacionLatitud, GeolocalizacionLongitud) VALUES (?, ?, ?, ?, ?)',
          [fechaHoraEntrada, IdTrabajo, IdUsuario, lat, lon]
        );
        return res.status(201).json({
          IdFichaje: result.insertId,
          FechaHoraEntrada: fechaHoraEntrada,
          FechaHoraSalida: null,
          HorasTrabajadas: null,
          IdTrabajo,
          IdUsuario,
          GeolocalizacionLatitud: lat,
          GeolocalizacionLongitud: lon
        });
      } catch (e) {
        console.warn('[DB] Fallback insert fichaje a mock:', e.message);
      }
    }

    const newId = mockFichajes.length > 0 ? Math.max(...mockFichajes.map(f => f.IdFichaje)) + 1 : 1;
    const nuevoFichaje = {
      IdFichaje: newId,
      FechaHoraEntrada: fechaHoraEntrada,
      FechaHoraSalida: null,
      HorasTrabajadas: null,
      IdTrabajo,
      IdUsuario,
      GeolocalizacionLatitud: lat,
      GeolocalizacionLongitud: lon
    };
    mockFichajes.unshift(nuevoFichaje);
    res.status(201).json(nuevoFichaje);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Cerrar fichaje (Salida y cálculo de HorasTrabajadas)
app.put('/api/v1/fichajes/cerrar/:idFichaje', async (req, res) => {
  const idFichaje = parseInt(req.params.idFichaje);
  const pad = (n) => String(n).padStart(2, '0');
  const d = new Date();
  const fechaHoraSalida = req.body.fechaHoraSalida || `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;

  try {
    let fEntrada;
    if (pool) {
      try {
        const [rows] = await pool.query('SELECT FechaHoraEntrada FROM Fichajes WHERE IdFichaje = ?', [idFichaje]);
        if (rows.length > 0) {
          fEntrada = new Date(rows[0].FechaHoraEntrada);
          const diffMs = new Date(fechaHoraSalida) - fEntrada;
          const horas = Math.max(1, Math.round(diffMs / (1000 * 60 * 60)));
          await pool.query('UPDATE Fichajes SET FechaHoraSalida = ?, HorasTrabajadas = ? WHERE IdFichaje = ?', [fechaHoraSalida, horas, idFichaje]);
          const [updated] = await pool.query('SELECT * FROM Fichajes WHERE IdFichaje = ?', [idFichaje]);
          return res.json(updated[0]);
        }
      } catch (e) {}
    }

    const fichaje = mockFichajes.find(f => f.IdFichaje === idFichaje);
    if (!fichaje) return res.status(404).json({ message: 'Fichaje no encontrado' });

    fEntrada = new Date(fichaje.FechaHoraEntrada);
    const diffMs = new Date(fechaHoraSalida) - fEntrada;
    const horas = Math.max(1, Math.round(diffMs / (1000 * 60 * 60)));

    fichaje.FechaHoraSalida = fechaHoraSalida;
    fichaje.HorasTrabajadas = horas;

    res.json(fichaje);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// -------------------------------------------------------------
// API KEY LIST
// -------------------------------------------------------------
app.get('/api/v1/apikey', async (req, res) => {
  try {
    if (pool) {
      try {
        const [rows] = await pool.query('SELECT * FROM ApiKey');
        return res.json(rows);
      } catch (e) {}
    }
    res.json(mockApiKey);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`=======================================================`);
  console.log(`🚀 API REST DISM corriendo en http://localhost:${PORT}`);
  console.log(`📖 Documentación Swagger UI en http://localhost:${PORT}/api-docs`);
  console.log(`=======================================================`);
});
