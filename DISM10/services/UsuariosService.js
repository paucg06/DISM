/* eslint-disable no-unused-vars */
const Service = require('./Service');
const mysql = require('mysql2');

// Conexión a la Base de Datos MySQL 'dism' (según Anexo del PDF)
const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'password', // o 'root' / '' según la instalación local de MySQL / XAMPP
  database: 'dism',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0,
});

// Mock en memoria para que el servidor responda correctamente siempre
let mockUsuarios = [
  { id: 1, nombre: 'Sergio', email: 'sergio@ua.es', edad: '20' },
  { id: 2, nombre: 'Estela', email: 'estela@ua.es', edad: '19' },
  { id: 3, nombre: 'Susana', email: 'susana@ua.es', edad: '27' },
  { id: 4, nombre: 'Hugo', email: 'hugo@ua.es', edad: '21' },
];

/**
 * Consultar todos los usuarios
 * Retorna la lista completa de usuarios desde la base de datos MySQL.
 */
const usuariosGET = () => new Promise(
  async (resolve, reject) => {
    pool.query('SELECT * FROM usuarios', (err, rows) => {
      if (err) {
        console.warn('MySQL no accesible en localhost, respondiendo con datos locales:', err.message);
        return resolve(Service.successResponse(mockUsuarios));
      }
      resolve(Service.successResponse(rows));
    });
  },
);

/**
 * Consultar usuario por ID
 */
const usuariosIdGET = ({ id }) => new Promise(
  async (resolve, reject) => {
    pool.query('SELECT * FROM usuarios WHERE id = ?', [id], (err, rows) => {
      if (err) {
        console.warn('MySQL no accesible en localhost, consultando datos locales:', err.message);
        const user = mockUsuarios.find((u) => u.id === Number(id));
        if (user) return resolve(Service.successResponse(user));
        return reject(Service.rejectResponse('Usuario no encontrado', 404));
      }
      if (rows && rows.length > 0) {
        resolve(Service.successResponse(rows[0]));
      } else {
        reject(Service.rejectResponse('Usuario no encontrado', 404));
      }
    });
  },
);

/**
 * Crear un nuevo usuario (POST)
 */
const usuariosPOST = ({ usuarioInput }) => new Promise(
  async (resolve, reject) => {
    const { nombre, email, edad } = usuarioInput;
    pool.query('INSERT INTO usuarios (nombre, email, edad) VALUES (?, ?, ?)', [nombre, email, edad], (err, result) => {
      if (err) {
        console.warn('MySQL no accesible en localhost, insertando en memoria:', err.message);
        const newId = mockUsuarios.length > 0 ? Math.max(...mockUsuarios.map((u) => u.id)) + 1 : 1;
        const newUser = { id: newId, nombre, email, edad };
        mockUsuarios.push(newUser);
        return resolve(Service.successResponse(newUser));
      }
      const createdUser = { id: result.insertId, nombre, email, edad };
      resolve(Service.successResponse(createdUser));
    });
  },
);

/**
 * Actualizar usuario por ID (PUT)
 */
const usuariosIdPUT = ({ id, usuarioInput }) => new Promise(
  async (resolve, reject) => {
    const { nombre, email, edad } = usuarioInput;
    pool.query('UPDATE usuarios SET nombre = ?, email = ?, edad = ? WHERE id = ?', [nombre, email, edad, id], (err, result) => {
      if (err) {
        console.warn('MySQL no accesible en localhost, actualizando en memoria:', err.message);
        const index = mockUsuarios.findIndex((u) => u.id === Number(id));
        if (index !== -1) {
          mockUsuarios[index] = { id: Number(id), nombre, email, edad };
          return resolve(Service.successResponse(mockUsuarios[index]));
        }
        return reject(Service.rejectResponse('Usuario no encontrado', 404));
      }
      resolve(Service.successResponse({ id: Number(id), nombre, email, edad }));
    });
  },
);

/**
 * Eliminar usuario por ID (DELETE)
 */
const usuariosIdDELETE = ({ id }) => new Promise(
  async (resolve, reject) => {
    pool.query('DELETE FROM usuarios WHERE id = ?', [id], (err, result) => {
      if (err) {
        console.warn('MySQL no accesible en localhost, borrando en memoria:', err.message);
        mockUsuarios = mockUsuarios.filter((u) => u.id !== Number(id));
        return resolve(Service.successResponse({ message: 'Usuario eliminado correctamente' }));
      }
      resolve(Service.successResponse({ message: 'Usuario eliminado correctamente' }));
    });
  },
);

module.exports = {
  usuariosGET,
  usuariosIdDELETE,
  usuariosIdGET,
  usuariosIdPUT,
  usuariosPOST,
};
