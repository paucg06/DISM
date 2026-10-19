// Anexo Servicios Web Rest - Ejercicio 1. Nodejs Hola Mundo
var express = require('express');
const app = express();
const puerto = 8080;

// http://localhost:8080/HolaMundo/{"nombre":"Hugo"}
app.get('/HolaMundo/:nombre', (req, resp) => {
  var entrada = JSON.parse(req.params.nombre);
  resp.writeHead(200, { 'content-type': 'text/plain' });
  resp.write('!Hola, Mundo ' + entrada.nombre + ' !');
  resp.end();
});

app.listen(puerto, () => {
  console.log('Aplicación escuchando en: http://localhost:' + puerto);
});
