// Anexo Servicios Web Rest - Ejercicio 3. Acceso a Base de Datos desde API Rest
var express = require("express");
var mysql = require('mysql2');
var app = express();
var bp = require('body-parser');
const cors = require('cors');

app.use(cors());
app.options('*', cors());
app.use(bp.json());

var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'root',
  password : 'password', // o 'root' / '' según el entorno
  database : 'dism'
});

// Ejercicio: GET http://localhost:8080/usuarios
app.get('/usuarios', function(req, resp) {
  connection.query('select * from usuarios', function(err, rows) {
    if (err) {
      console.log('Error en /usuarios ' + err);
      resp.status(500);
      resp.send({ message: "Error al obtener usuarios" });
    } else {
      console.log('/usuarios');
      resp.status(200);
      resp.send(rows);
    }
  });
});

var server = app.listen(8080, function () {
  console.log('Servidor iniciado en puerto 8080…'); 
});
