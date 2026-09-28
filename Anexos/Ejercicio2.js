// Anexo Servicios Web Rest - Ejercicio 2. Diseño API Rest
// Cargar modulos y crear nueva aplicacion
var express = require("express"); 
var app = express();
var bodyParser = require('body-parser');
app.use(bodyParser.json()); // soporte para bodies codificados en jsonsupport
app.use(bodyParser.urlencoded({ extended: true })); // soporte para bodies codificados

// Ejercicio: GET http://localhost:8080/items
app.get('/items', function(req, res, next) {
  if(req.query.filter) {
    next();
    return;
  }
  res.send('Get all');
});

// Ejercicio: GET http://localhost:8080/items?filter=ABC
app.get('/items', function(req, res) {
  var filter = req.query.filter;
  res.send('Get filter ' + filter);
});

// Ejercicio: GET http://localhost:8080/items/10
app.get('/items/:id', function(req, res, next) {
  var itemId = req.params.id;
  res.send('Get ' + req.params.id);
});

// Ejercicio: POST http://localhost:8080/items
app.post('/items', function(req, res) {
  var data = req.body.data;
  res.send('Add ' + data);
});

// Ejercicio: PUT http://localhost:8080/items
app.put('/items', function(req, res) {
  var itemId = req.body.id;
  var data = req.body.data;
  res.send('Update ' + itemId + ' with ' + data);
});

// Ejercicio: DELETE http://localhost:8080/items
app.delete('/items/:id', function(req, res) {
  var itemId = req.params.id;
  res.send('Delete ' + itemId);
});

var server = app.listen(8080, function () {
  console.log('Servidor iniciado en puerto 8080...'); 
});
