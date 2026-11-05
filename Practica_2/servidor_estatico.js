// Servidor estatico nativo Node.js para servir la aplicacion PWA unificada de Registro Horario
const http = require('http');
const fs = require('fs');
const path = require('path');

const mimeTypes = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.mjs': 'application/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.webmanifest': 'application/manifest+json; charset=utf-8',
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
      // Si el archivo no existe o es una ruta Angular SPA, servir index.html
      if (err || !stats.isFile()) {
        filePath = path.join(staticDir, 'index.html');
      }

      const ext = path.extname(filePath).toLowerCase();
      const contentType = mimeTypes[ext] || 'application/octet-stream';

      fs.readFile(filePath, (readErr, content) => {
        if (readErr) {
          res.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
          res.end('Error 500: No se pudo cargar el archivo.');
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

const appDir = path.join(__dirname, 'AppRegistroHorario', 'www');

console.log('===================================================================');
console.log('    SERVIDOR WEB PWA - SISTEMA UNIFICADO DE REGISTRO HORARIO       ');
console.log('===================================================================');
createSpaServer(8100, appDir, 'AppRegistroHorario (PWA)');

// Puerto secundario 8101 redirige al 8100 para compatibilidad
const redirectServer = http.createServer((req, res) => {
  res.writeHead(302, { Location: 'http://localhost:8100' + req.url });
  res.end();
});
redirectServer.listen(8101, () => {
  console.log('[OK] Redireccion de compatibilidad activa en: http://localhost:8101 -> 8100');
});

console.log('Presiona Ctrl+C para detener el servidor.');
console.log('-------------------------------------------------------------------');
