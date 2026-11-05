// Servidor estatico ligero de cero dependencias para servir AppAdmin y AppUsuarios compilados
const http = require('http');
const fs = require('fs');
const path = require('path');

const mimeTypes = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.mjs': 'application/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.otf': 'font/otf',
  '.wasm': 'application/wasm'
};

function createSpaServer(port, staticDir, appName) {
  const server = http.createServer((req, res) => {
    // Permitir CORS por si fuera necesario
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', '*');

    if (req.method === 'OPTIONS') {
      res.writeHead(200);
      res.end();
      return;
    }

    let reqPath = decodeURI(req.url.split('?')[0]);
    if (reqPath === '/' || reqPath === '') {
      reqPath = '/index.html';
    }

    let filePath = path.join(staticDir, reqPath);

    fs.stat(filePath, (err, stats) => {
      // Si el archivo no existe o es una ruta de Angular/Ionic SPA, devolver index.html
      if (err || !stats.isFile()) {
        filePath = path.join(staticDir, 'index.html');
      }

      const ext = path.extname(filePath).toLowerCase();
      const contentType = mimeTypes[ext] || 'application/octet-stream';

      fs.readFile(filePath, (readErr, content) => {
        if (readErr) {
          res.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
          res.end(`Error 500: No se pudo cargar el archivo.`);
          return;
        }
        res.writeHead(200, { 'Content-Type': contentType });
        res.end(content);
      });
    });
  });

  server.listen(port, () => {
    console.log(`[OK] ${appName} iniciado en: http://localhost:${port}`);
  });

  return server;
}

const adminDir = path.join(__dirname, 'AppAdmin', 'www');
const usuariosDir = path.join(__dirname, 'AppUsuarios', 'www');

console.log('===================================================================');
console.log('   SERVIDOR ESTATICO - APLICACIONES COMPILADAS IONIC / ANGULAR   ');
console.log('===================================================================');
createSpaServer(8100, adminDir, 'AppAdmin (Administrador)');
createSpaServer(8101, usuariosDir, 'AppUsuarios (Empleados)');
console.log('Presiona Ctrl+C para detener los servidores web.');
console.log('-------------------------------------------------------------------');
