const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');
const { fork } = require('child_process');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const OUTPUT_DIR = path.join(__dirname, '..', 'Capturas_Responsive_470x900');
const DESKTOP_OUTPUT_DIR = 'C:\\Users\\paucr\\Desktop\\Practica_Compilada\\Capturas_Responsive_470x900';

const cleanDir = (dir) => {
  if (fs.existsSync(dir)) {
    const files = fs.readdirSync(dir);
    for (const f of files) {
      if (f.endsWith('.png') || f.endsWith('.pdf')) {
        try { fs.unlinkSync(path.join(dir, f)); } catch (e) {}
      }
    }
  }
};

cleanDir(OUTPUT_DIR);
cleanDir(DESKTOP_OUTPUT_DIR);

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function run() {
  console.log('[0/5] Iniciando servidores de backend (8080) y frontend PWA (8100)...');
  const serverProc = fork(path.join(__dirname, 'server.js'), [], { stdio: 'ignore' });
  const staticProc = fork(path.join(__dirname, '..', 'servidor_estatico.js'), [], { stdio: 'ignore' });
  await sleep(3000);

  console.log('[1/5] Iniciando navegador Chrome headless a resolución móvil 470x900 (deviceScaleFactor: 2)...');
  const browser = await puppeteer.launch({
    executablePath: CHROME_PATH,
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']
  });

  const page = await browser.newPage();
  await page.setViewport({
    width: 470,
    height: 900,
    deviceScaleFactor: 2,
    isMobile: true,
    hasTouch: true
  });

  // Emular geolocalización fija para que la captura muestre coordenadas reales en Leaflet
  await page.setGeolocation({ latitude: 39.4699, longitude: -0.3763 });

  const capture = async (filename, desc) => {
    const fullPath = path.join(OUTPUT_DIR, filename);
    await page.screenshot({ path: fullPath, type: 'png' });
    // Copiar también de inmediato al directorio del Escritorio
    const desktopPath = path.join(DESKTOP_OUTPUT_DIR, filename);
    fs.copyFileSync(fullPath, desktopPath);
    console.log(`[CAPTURA OK] -> ${filename} (${desc})`);
  };

  try {
    // -------------------------------------------------------------
    // SECCIÓN 1: LOGIN Y ACCESOS
    // -------------------------------------------------------------
    console.log('\n[2/5] Capturando flujo de Inicio de Sesión...');
    await page.goto('http://localhost:8100/login', { waitUntil: 'networkidle0' });
    await sleep(800);
    await capture('01_Login_Inicio.png', 'Pantalla de Inicio de Sesión limpia en tema gris neutral');

    // Test de error de contraseña
    await page.evaluate(() => {
      const inputs = document.querySelectorAll('ion-input input');
      if (inputs[0]) { inputs[0].value = 'admin'; inputs[0].dispatchEvent(new Event('input', { bubbles: true })); }
      if (inputs[1]) { inputs[1].value = 'clave_incorrecta'; inputs[1].dispatchEvent(new Event('input', { bubbles: true })); }
    });
    await sleep(200);
    await page.click('.login-btn');
    await sleep(500);
    await capture('02_Login_Error_Contrasena.png', 'Error de contraseña con aviso toast rojo y barra de carga detenida');

    // Login exitoso Administrador
    await page.evaluate(() => {
      const inputs = document.querySelectorAll('ion-input input');
      if (inputs[1]) { inputs[1].value = 'admin123'; inputs[1].dispatchEvent(new Event('input', { bubbles: true })); }
    });
    await sleep(200);
    await page.click('.login-btn');
    await sleep(350);
    await capture('03_Login_Exito_Toast.png', 'Aviso emergente de bienvenida tras autenticación correcta');

    // Panel General Admin
    await sleep(1500);
    await capture('04_Panel_Admin_General.png', 'Panel principal del Administrador (Tema Verde)');

    // -------------------------------------------------------------
    // SECCIÓN 2: ADMINISTRADOR - CRUD Y MAPA LEAFLET
    // -------------------------------------------------------------
    console.log('\n[3/5] Capturando vistas y ventanas emergentes del Administrador...');

    // 5. Gestión de Usuarios
    await page.goto('http://localhost:8100/usuarios', { waitUntil: 'networkidle0' });
    await sleep(1000);
    await capture('05_Admin_Gestion_Usuarios.png', 'Gestión de Usuarios con lista completa y botón inferior Añadir Nuevo Usuario');

    // 6. Modal Detalle / Edición Usuario (click en primer usuario de la lista)
    await page.evaluate(() => {
      const firstItem = document.querySelector('ion-list ion-item');
      if (firstItem) firstItem.click();
    });
    await sleep(1000);
    await capture('06_Admin_Modal_Detalle_Usuario.png', 'Modal emergente de consulta y edición de usuario');

    // Cerrar modal
    await page.evaluate(() => {
      const closeBtn = Array.from(document.querySelectorAll('ion-modal ion-button')).find(b => b.innerText.includes('Cerrar'));
      if (closeBtn) closeBtn.click();
    });
    await sleep(700);

    // 7. Modal Añadir Nuevo Usuario (click en botón verde al pie)
    await page.evaluate(() => {
      const btn = Array.from(document.querySelectorAll('ion-button')).find(b => b.innerText.includes('Añadir Nuevo Usuario'));
      if (btn) btn.click();
    });
    await sleep(1000);
    await capture('07_Admin_Modal_Nuevo_Usuario.png', 'Modal emergente para registrar un nuevo usuario');

    // Cerrar modal
    await page.evaluate(() => {
      const closeBtn = Array.from(document.querySelectorAll('ion-modal ion-button')).find(b => b.innerText.includes('Cerrar'));
      if (closeBtn) closeBtn.click();
    });
    await sleep(700);

    // 8. Gestión de Trabajos
    await page.goto('http://localhost:8100/trabajos', { waitUntil: 'networkidle0' });
    await sleep(1000);
    await capture('08_Admin_Gestion_Trabajos.png', 'Gestión de Trabajos con lista de proyectos y botón Crear Nuevo Trabajo');

    // 9. Modal Detalle Trabajo (click en primer trabajo)
    await page.evaluate(() => {
      const firstItem = document.querySelector('ion-list ion-item');
      if (firstItem) firstItem.click();
    });
    await sleep(1000);
    await capture('09_Admin_Modal_Detalle_Trabajo.png', 'Modal emergente con detalles del trabajo asignable');

    // Cerrar modal
    await page.evaluate(() => {
      const closeBtn = Array.from(document.querySelectorAll('ion-modal ion-button')).find(b => b.innerText.includes('Cerrar'));
      if (closeBtn) closeBtn.click();
    });
    await sleep(700);

    // 10. Modal Crear Nuevo Trabajo
    await page.evaluate(() => {
      const btn = Array.from(document.querySelectorAll('ion-button')).find(b => b.innerText.includes('Crear Nuevo Trabajo'));
      if (btn) btn.click();
    });
    await sleep(1000);
    await capture('10_Admin_Modal_Nuevo_Trabajo.png', 'Modal emergente para dar de alta un nuevo trabajo');

    // Cerrar modal
    await page.evaluate(() => {
      const closeBtn = Array.from(document.querySelectorAll('ion-modal ion-button')).find(b => b.innerText.includes('Cerrar'));
      if (closeBtn) closeBtn.click();
    });
    await sleep(700);

    // 11. Gestión de Fichajes
    await page.goto('http://localhost:8100/fichajes', { waitUntil: 'networkidle0' });
    await sleep(1200);
    await capture('11_Admin_Gestion_Fichajes.png', 'Gestión de Fichajes con filtros de fecha adaptativos y botón para eliminar');

    // 12. Modal con Mapa Leaflet de Ubicación del Fichaje
    console.log('[MAPA] Abriendo modal de mapa interactivo Leaflet...');
    const mapaAbierto = await page.evaluate(() => {
      const cards = Array.from(document.querySelectorAll('ion-list ion-card'));
      for (const card of cards) {
        const btn = Array.from(card.querySelectorAll('ion-button')).find(b => b.innerText.includes('Ver Mapa') || b.textContent.includes('Ver Mapa'));
        if (btn) {
          btn.click();
          return true;
        }
      }
      return false;
    });

    if (mapaAbierto) {
      // Esperar a que el modal y las capas de Leaflet se inicialicen y rendericen
      await sleep(1800);
      await capture('12_Admin_Modal_Mapa_Fichaje.png', 'Modal emergente con mapa Leaflet interactivo, chincheta y coordenadas');

      // Cerrar modal de mapa
      await page.evaluate(() => {
        const closeBtn = Array.from(document.querySelectorAll('ion-modal ion-button')).find(b => b.innerText.includes('Cerrar'));
        if (closeBtn) closeBtn.click();
      });
      await sleep(700);
    }

    // -------------------------------------------------------------
    // SECCIÓN 3: PORTAL DEL EMPLEADO - FICHAJES SIMULTÁNEOS
    // -------------------------------------------------------------
    console.log('\n[4/5] Capturando Portal del Empleado y turnos en paralelo...');

    // Iniciar sesión como Empleado
    await page.goto('http://localhost:8100/login', { waitUntil: 'networkidle0' });
    await sleep(600);
    await page.evaluate(() => {
      localStorage.setItem('auth_user', JSON.stringify({
        IdUsuario: 2,
        Nombre: 'Sergio Martin',
        Usuario: 'sergio',
        Rol: 'empleado'
      }));
      const inputs = document.querySelectorAll('ion-input input');
      if (inputs[0]) { inputs[0].value = 'sergio'; }
      if (inputs[1]) { inputs[1].value = '1234'; }
    });
    await sleep(400);
    await page.click('.login-btn');
    await sleep(1500);

    // 13. Panel Empleado General
    await capture('13_Panel_Empleado_General.png', 'Portal del Empleado (Tema Azul)');

    // 14. Registrar Fichaje Inicial (solo tarjeta de Nueva Jornada)
    await page.goto('http://localhost:8100/registrar-fichaje', { waitUntil: 'networkidle0' });
    await sleep(1200);
    await capture('14_Empleado_Registrar_Fichaje_Inicial.png', 'Pantalla Registrar Fichaje con tarjeta superior de Nueva Jornada');

    // 15. Iniciar un fichaje activo (1 turno en curso)
    console.log('[FICHAJE] Iniciando primer turno activo...');
    await page.evaluate(() => {
      const btn = Array.from(document.querySelectorAll('ion-card:first-of-type ion-button')).find(b => b.innerText.includes('Fichar Entrada') || b.textContent.includes('Fichar Entrada'));
      if (btn) btn.click();
    });
    await sleep(1200);
    await capture('15_Empleado_Fichaje_Activo_Unico.png', 'Turno en curso activo mostrado debajo con métricas homologadas y botón Finalizar');

    // 16. Iniciar segundo fichaje en paralelo (2 turnos simultáneos)
    console.log('[FICHAJE] Iniciando segundo turno en paralelo...');
    await page.evaluate(() => {
      const select = document.querySelector('ion-select');
      if (select) {
        select.value = 2;
        select.dispatchEvent(new CustomEvent('ionChange', { detail: { value: 2 } }));
      }
      const btn = Array.from(document.querySelectorAll('ion-card:first-of-type ion-button')).find(b => b.innerText.includes('Fichar Entrada') || b.textContent.includes('Fichar Entrada'));
      if (btn) btn.click();
    });
    await sleep(1200);
    await capture('16_Empleado_Fichajes_Activos_Paralelo.png', 'Múltiples fichajes activos simultáneos en paralelo con contador dinámico');

    // 17. Finalizar un fichaje con aviso Toast verde
    console.log('[FICHAJE] Finalizando turno con confirmación Toast...');
    await page.evaluate(() => {
      const btnDanger = Array.from(document.querySelectorAll('ion-card ion-button[color="danger"]')).find(b => b.innerText.includes('Finalizar Fichaje') || b.textContent.includes('Finalizar Fichaje'));
      if (btnDanger) btnDanger.click();
    });
    await sleep(400); // Capturar con el toast verde visible
    await capture('17_Empleado_Fichaje_Finalizado_Toast.png', 'Confirmación verde de fichaje finalizado y borrado automático del recuadro');
    await sleep(1000);

    // 18. Consulta de Fichajes Empleado
    await page.goto('http://localhost:8100/consulta-fichajes', { waitUntil: 'networkidle0' });
    await sleep(1200);
    await capture('18_Empleado_Consulta_Fichajes.png', 'Consulta de Fichajes con historial, horas totales y selector de fechas adaptativo');

    // 19. Cierre de Sesión seguro
    console.log('[LOGOUT] Cerrando sesión de usuario...');
    await page.evaluate(() => {
      const logoutBtn = Array.from(document.querySelectorAll('ion-header ion-button')).find(b => (b.title && b.title.includes('Cerrar sesión')) || b.querySelector('ion-icon[name="log-out-outline"]'));
      if (logoutBtn) logoutBtn.click();
    });
    await sleep(1000);
    await capture('19_Cerrar_Sesion_Retorno_Login.png', 'Retorno limpio a la pantalla de Login tras cerrar sesión');

    console.log('\n[EXITO] Las 19 capturas completas han sido generadas y sincronizadas en Escritorio.');

    // -------------------------------------------------------------
    // GENERAR PDF DE PRESENTACIÓN A4
    // -------------------------------------------------------------
    console.log('\n[5/5] Compilando PDF oficial de presentación con el catálogo completo...');
    const pdfPage = await browser.newPage();
    await pdfPage.setViewport({ width: 1200, height: 1600 });

    const screensCatalog = [
      { f: '01_Login_Inicio.png', t: '1. Inicio de Sesión', d: 'Interfaz neutral y minimalista en escala de grises. Acceso unificado mediante usuario y contraseña con autenticación en tiempo real.' },
      { f: '02_Login_Error_Contrasena.png', t: '2. Error de Credenciales', d: 'Gestión inmediata de error ante clave incorrecta: la barra de progreso se detiene en 0 ms y se muestra un aviso emergente rojo sin bloquear la interfaz.' },
      { f: '03_Login_Exito_Toast.png', t: '3. Acceso Correcto', d: 'Saludo de bienvenida personalizado al usuario antes de redirigir fluidamente al panel correspondiente según su rol.' },
      { f: '04_Panel_Admin_General.png', t: '4. Panel Principal Administrador', d: 'Hub de control con identidad corporativa verde: módulos de Usuarios, Trabajos y Gestión de Fichajes.' },
      { f: '05_Admin_Gestion_Usuarios.png', t: '5. Gestión de Usuarios', d: 'Listado completo de personal cargado por defecto, badges de rol diferenciados, borrado directo y botón inferior para alta de usuarios.' },
      { f: '06_Admin_Modal_Detalle_Usuario.png', t: '6. Modal Detalle / Edición Usuario', d: 'Ventana modal interactiva para inspeccionar y modificar los datos de un usuario existente.' },
      { f: '07_Admin_Modal_Nuevo_Usuario.png', t: '7. Modal Nuevo Usuario', d: 'Formulario modal activado desde el botón inferior para dar de alta nuevos empleados o administradores en el sistema.' },
      { f: '08_Admin_Gestion_Trabajos.png', t: '8. Gestión de Trabajos', d: 'Catálogo de proyectos y tareas activas cargadas de forma inmediata al entrar, con opción de eliminación y botón de alta al pie.' },
      { f: '09_Admin_Modal_Detalle_Trabajo.png', t: '9. Modal Detalle de Trabajo', d: 'Ventana modal emergente con la información y edición del código y denominación de la tarea seleccionada.' },
      { f: '10_Admin_Modal_Nuevo_Trabajo.png', t: '10. Modal Crear Nuevo Trabajo', d: 'Formulario modal para registrar nuevas actividades asignables en las jornadas laborales.' },
      { f: '11_Admin_Gestion_Fichajes.png', t: '11. Gestión y Auditoría de Fichajes', d: 'Historial global de fichajes con filtros adaptativos de fecha e icono de calendario optimizado claro/oscuro, y botón de borrado de registros.' },
      { f: '12_Admin_Modal_Mapa_Fichaje.png', t: '12. Modal con Mapa Leaflet Interactivo', d: 'Ventana emergente que renderiza un visor interactivo de mapa Leaflet con chincheta GPS y coordenadas del lugar de inicio de jornada.' },
      { f: '13_Panel_Empleado_General.png', t: '13. Portal del Empleado', d: 'Panel principal de usuario con identidad corporativa azul. Acceso directo a Registrar Fichaje y Consulta de Historial.' },
      { f: '14_Empleado_Registrar_Fichaje_Inicial.png', t: '14. Registrar Fichaje - Tarjeta Nueva Jornada', d: 'Tarjeta principal de registro con selector de tarea y botón Fichar Entrada siempre activo para permitir registros continuos.' },
      { f: '15_Empleado_Fichaje_Activo_Unico.png', t: '15. Fichaje en Curso Detectado', d: 'Recuadro dinámico generado debajo que homologa exactamente las métricas de la tarjeta superior, mostrando estado En Curso y botón rojo Finalizar Fichaje.' },
      { f: '16_Empleado_Fichajes_Activos_Paralelo.png', t: '16. Múltiples Fichajes Activos en Paralelo', d: 'Demostración del registro multitarea en paralelo: el usuario mantiene abiertos turnos simultáneos con recuadros independientes.' },
      { f: '17_Empleado_Fichaje_Finalizado_Toast.png', t: '17. Finalización Inmediata y Aviso Toast', d: 'Al pulsar el botón rojo de finalizar, el recuadro se elimina al instante (0 ms) y se confirma la jornada completada con una notificación verde.' },
      { f: '18_Empleado_Consulta_Fichajes.png', t: '18. Consulta de Historial de Fichajes', d: 'Historial individual del empleado con filtro de fechas adaptativo, cálculo automático de horas trabajadas y visualización optimizada.' },
      { f: '19_Cerrar_Sesion_Retorno_Login.png', t: '19. Cierre de Sesión Seguro', d: 'Desconexión limpia de la sesión mediante el botón de logout de la barra superior, destruyendo tokens y retornando a la pantalla de entrada.' }
    ];

    const htmlContent = `
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Catálogo Oficial de Pantallas - PWA Control Horario</title>
  <style>
    @page { size: A4; margin: 12mm; }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; color: #1e293b; margin: 0; background: #ffffff; }
    .cover { text-align: center; padding: 40px 20px 30px; page-break-after: always; }
    .cover h1 { font-size: 32px; color: #0f172a; margin-bottom: 8px; }
    .cover h2 { font-size: 20px; color: #2563eb; font-weight: 500; margin-bottom: 20px; }
    .cover p { font-size: 15px; color: #64748b; line-height: 1.6; max-width: 650px; margin: 0 auto; }
    .badge { display: inline-block; padding: 6px 14px; border-radius: 20px; font-size: 13px; font-weight: 600; margin: 4px; }
    .badge-admin { background: #dcfce7; color: #166534; }
    .badge-emp { background: #dbeafe; color: #1e40af; }
    .grid { display: flex; flex-direction: column; gap: 30px; }
    .screen-card { page-break-inside: avoid; border: 1px solid #e2e8f0; border-radius: 12px; padding: 18px; background: #f8fafc; margin-bottom: 20px; display: flex; gap: 24px; align-items: center; }
    .screen-img { width: 235px; height: 450px; border-radius: 12px; border: 3px solid #0f172a; box-shadow: 0 10px 25px rgba(0,0,0,0.12); object-fit: cover; background: #000; flex-shrink: 0; }
    .screen-info { flex: 1; }
    .screen-info h3 { margin: 0 0 10px 0; font-size: 20px; color: #0f172a; }
    .screen-info p { font-size: 14px; color: #475569; line-height: 1.6; margin: 0 0 14px 0; }
    .file-tag { font-family: monospace; font-size: 12px; color: #475569; background: #e2e8f0; padding: 6px 10px; border-radius: 6px; display: inline-block; font-weight: 600; }
  </style>
</head>
<body>
  <div class="cover">
    <h1>Control Horario - PWA Ionic</h1>
    <h2>Práctica 2 DISM - Sistema Unificado de Registro y Gestión</h2>
    <p>Documento de presentación técnica con el catálogo visual completo en formato móvil responsive (470 x 900 px). Cubre la totalidad de estados de la aplicación: autenticación, CRUD de administración, ventanas modales emergentes, mapa GPS interactivo Leaflet y flujo multitarea de fichajes en paralelo.</p>
    <div style="margin-top: 25px;">
      <span class="badge badge-admin">Rol Administrador (Tema Verde)</span>
      <span class="badge badge-emp">Rol Empleado (Tema Azul)</span>
    </div>
  </div>

  <div class="grid">
    ${screensCatalog.map(item => `
      <div class="screen-card">
        <img class="screen-img" src="file://${path.join(OUTPUT_DIR, item.f).replace(/\\/g, '/')}" alt="${item.t}">
        <div class="screen-info">
          <h3>${item.t}</h3>
          <p>${item.d}</p>
          <div class="file-tag">Archivo: ${item.f}</div>
        </div>
      </div>
    `).join('')}
  </div>
</body>
</html>
    `;

    await pdfPage.setContent(htmlContent, { waitUntil: 'networkidle0' });
    const localPdf = path.join(OUTPUT_DIR, 'Presentacion_Capturas_PWA.pdf');
    const desktopPdf = path.join(DESKTOP_OUTPUT_DIR, 'Presentacion_Capturas_PWA.pdf');

    await pdfPage.pdf({
      path: localPdf,
      format: 'A4',
      printBackground: true,
      margin: { top: '12mm', bottom: '12mm', left: '12mm', right: '12mm' }
    });
    fs.copyFileSync(localPdf, desktopPdf);
    console.log('[PDF OK] Documento PDF compilado con éxito en:', desktopPdf);

  } catch (err) {
    console.error('Error durante la generación de capturas:', err);
  } finally {
    if (browser) await browser.close();
    if (serverProc) serverProc.kill();
    if (staticProc) staticProc.kill();
    console.log('[FIN] Proceso completado y servidores liberados.');
  }
}

run();
