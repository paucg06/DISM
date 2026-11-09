const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const OUTPUT_DIR = path.join(__dirname, '..', 'Capturas_Responsive_470x900');

if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function run() {
  console.log('[1/4] Iniciando navegador Chrome headless en 470x900...');
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

  const capture = async (filename, desc) => {
    const fullPath = path.join(OUTPUT_DIR, filename);
    await page.screenshot({ path: fullPath, type: 'png' });
    console.log(`[CAPTURA] Guardada: ${filename} (${desc})`);
  };

  try {
    // 1. Login inicial
    console.log('[2/4] Capturando pantallas de Inicio de Sesión...');
    await page.goto('http://localhost:8100/login', { waitUntil: 'networkidle0' });
    await sleep(800);
    await capture('01_Login_Inicio.png', 'Pantalla de Inicio de Sesión limpia');

    // 2. Error contraseña
    await page.type('ion-input[placeholder*="usuario"] input, ion-item:nth-of-type(1) input', 'admin');
    await page.type('ion-input[type="password"] input', 'clave_erronea');
    await page.click('.login-btn');
    await sleep(500);
    await capture('02_Login_Error_Contrasena.png', 'Error de contraseña con aviso toast rojo y barra de carga detenida');

    // 3. Login exitoso Admin
    await page.click('ion-input[type="password"] input', { clickCount: 3 });
    await page.keyboard.press('Backspace');
    await page.type('ion-input[type="password"] input', 'admin123');
    await page.click('.login-btn');
    await sleep(400);
    await capture('03_Login_Exito_Toast.png', 'Bienvenida de inicio de sesión correcto');

    // 4. Panel Admin
    await sleep(1500);
    await capture('04_Panel_Admin_General.png', 'Panel del Administrador (Tema Verde)');

    // 5. Gestión de Usuarios
    console.log('[3/4] Capturando pantallas del Administrador...');
    await page.goto('http://localhost:8100/usuarios', { waitUntil: 'networkidle0' });
    await sleep(1000);
    await capture('05_Admin_Gestion_Usuarios.png', 'Gestión de Usuarios con lista completa y botón inferior Añadir Nuevo Usuario');

    // 6. Modal Detalle Usuario
    await page.click('ion-list ion-item:first-of-type');
    await sleep(800);
    await capture('06_Admin_Modal_Detalle_Usuario.png', 'Modal de detalle y edición de usuario');

    // 7. Gestión de Trabajos
    await page.goto('http://localhost:8100/trabajos', { waitUntil: 'networkidle0' });
    await sleep(1000);
    await capture('07_Admin_Gestion_Trabajos.png', 'Gestión de Trabajos con proyectos y botón inferior Crear Nuevo Trabajo');

    // 8. Modal Detalle Trabajo
    await page.click('ion-list ion-item:first-of-type');
    await sleep(800);
    await capture('08_Admin_Modal_Detalle_Trabajo.png', 'Modal de detalle de trabajo');

    // 9. Gestión de Fichajes
    await page.goto('http://localhost:8100/fichajes', { waitUntil: 'networkidle0' });
    await sleep(1000);
    await capture('09_Admin_Gestion_Fichajes.png', 'Gestión de Fichajes con filtros de fecha adaptativos y botón rojo para eliminar');

    // 10. Modal Mapa Fichaje
    const mapaBtn = await page.$('ion-card ion-button[color="success"]');
    if (mapaBtn) {
      await mapaBtn.click();
      await sleep(1200);
      await capture('10_Admin_Modal_Mapa_Fichaje.png', 'Modal con mapa de ubicación interactivo');
    }

    // 11. Login como Empleado
    console.log('[4/4] Capturando pantallas del Portal del Empleado...');
    await page.goto('http://localhost:8100/login', { waitUntil: 'networkidle0' });
    await sleep(800);
    await page.type('ion-input[placeholder*="usuario"] input, ion-item:nth-of-type(1) input', 'sergio');
    await page.type('ion-input[type="password"] input', '1234');
    await page.click('.login-btn');
    await sleep(1500);
    await capture('11_Panel_Empleado_General.png', 'Portal del Empleado (Tema Azul)');

    // 12. Registrar Fichaje Inicial
    await page.goto('http://localhost:8100/registrar-fichaje', { waitUntil: 'networkidle0' });
    await sleep(1000);
    await capture('12_Empleado_Registrar_Fichaje_Inicial.png', 'Registrar Fichaje con tarjeta superior de Nueva Jornada');

    // 13. Fichar dos tareas en paralelo
    await page.click('ion-button[color="primary"]');
    await sleep(600);
    // Cambiar trabajo y fichar segunda entrada en paralelo
    await page.evaluate(() => {
      const select = document.querySelector('ion-select');
      if (select) select.value = 2;
    });
    await sleep(300);
    await page.click('ion-button[color="primary"]');
    await sleep(800);
    await capture('13_Empleado_Fichajes_Activos_Paralelo.png', 'Fichajes activos en curso con métricas homologadas y botón Finalizar');

    // 14. Finalizar fichaje
    const finBtn = await page.$('ion-button[color="danger"]');
    if (finBtn) {
      await finBtn.click();
      await sleep(400);
      await capture('14_Empleado_Fichaje_Finalizado_Toast.png', 'Aviso verde de fichaje finalizado y borrado inmediato del turno');
      await sleep(1000);
    }

    // 15. Consulta de Fichajes
    await page.goto('http://localhost:8100/consulta-fichajes', { waitUntil: 'networkidle0' });
    await sleep(1000);
    await capture('15_Empleado_Consulta_Fichajes.png', 'Consulta de Fichajes con filtros de fecha adaptativos e historial de jornadas');

    // 16. Cerrar Sesión
    await page.click('ion-header ion-buttons[slot="end"] ion-button');
    await sleep(800);
    await capture('16_Cerrar_Sesion_Retorno_Login.png', 'Cierre de sesión seguro y retorno a pantalla de login');

    console.log('\n[EXITO] Todas las 16 capturas generadas correctamente en:', OUTPUT_DIR);

    // Generar documento PDF de presentación
    console.log('\n[PDF] Generando PDF de presentación responsive...');
    const pdfPage = await browser.newPage();
    await pdfPage.setViewport({ width: 1200, height: 1600 });

    const htmlContent = `
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Presentación Capturas PWA Control Horario</title>
  <style>
    @page { size: A4; margin: 15mm; }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; color: #1e293b; margin: 0; background: #ffffff; }
    .cover { text-align: center; padding: 40px 20px 20px; page-break-after: always; }
    .cover h1 { font-size: 32px; color: #0f172a; margin-bottom: 8px; }
    .cover h2 { font-size: 20px; color: #2563eb; font-weight: 500; margin-bottom: 24px; }
    .cover p { font-size: 15px; color: #64748b; line-height: 1.6; max-width: 600px; margin: 0 auto; }
    .badge { display: inline-block; padding: 6px 14px; border-radius: 20px; font-size: 13px; font-weight: 600; margin: 4px; }
    .badge-admin { background: #dcfce7; color: #166534; }
    .badge-emp { background: #dbeafe; color: #1e40af; }
    .grid { display: flex; flex-direction: column; gap: 40px; }
    .screen-card { page-break-inside: avoid; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; background: #f8fafc; margin-bottom: 25px; display: flex; gap: 24px; align-items: center; }
    .screen-img { width: 235px; height: 450px; border-radius: 12px; border: 3px solid #0f172a; box-shadow: 0 10px 25px rgba(0,0,0,0.15); object-fit: cover; background: #000; flex-shrink: 0; }
    .screen-info { flex: 1; }
    .screen-info h3 { margin: 0 0 10px 0; font-size: 20px; color: #0f172a; }
    .screen-info p { font-size: 14px; color: #475569; line-height: 1.6; margin: 0 0 12px 0; }
  </style>
</head>
<body>
  <div class="cover">
    <h1>Control Horario - PWA Ionic</h1>
    <h2>Práctica 2 DISM - Sistema Unificado de Registro y Gestión</h2>
    <p>Presentación técnica y catálogo de capturas responsive en formato móvil (470 x 900 px) cubriendo todos los estados y flujos funcionales del sistema.</p>
    <div style="margin-top: 20px;">
      <span class="badge badge-admin">Rol Administrador (Tema Verde)</span>
      <span class="badge badge-emp">Rol Empleado (Tema Azul)</span>
    </div>
  </div>

  <div class="grid">
    ${[
      { f: '01_Login_Inicio.png', t: '1. Pantalla de Inicio de Sesión', d: 'Interfaz neutral y minimalista en tema gris. Proporciona acceso unificado mediante usuario y contraseña tanto para administradores como para empleados.' },
      { f: '02_Login_Error_Contrasena.png', t: '2. Feedback Inmediato ante Error de Clave', d: 'Al introducir credenciales incorrectas, el spinner y la barra de carga se detienen en 0 ms mostrando un aviso toast de advertencia sin bloquear la interacción.' },
      { f: '03_Login_Exito_Toast.png', t: '3. Autenticación Exitosa', d: 'Notificación emergente con saludo personalizado al usuario antes de redirigir fluidamente a su panel correspondiente.' },
      { f: '04_Panel_Admin_General.png', t: '4. Panel del Administrador (Tema Verde)', d: 'Pantalla principal de gestión integral para la cuenta de administración. Acceso modular a Usuarios, Trabajos y Fichajes con identidad visual verde.' },
      { f: '05_Admin_Gestion_Usuarios.png', t: '5. Gestión de Usuarios (CRUD)', d: 'Listado completo de usuarios renderizado inmediatamente en la carga, con roles diferenciados, eliminación directa y botón inferior para añadir nuevos usuarios.' },
      { f: '06_Admin_Modal_Detalle_Usuario.png', t: '6. Modal de Detalle y Edición de Usuario', d: 'Ventana modal para visualizar, editar o crear usuarios con validación de identificador, nombre, usuario y contraseña.' },
      { f: '07_Admin_Gestion_Trabajos.png', t: '7. Gestión de Trabajos (Catálogo)', d: 'Listado de proyectos y tareas asignables. Se muestra de forma instantánea al ingresar con opción de eliminación y botón de alta al pie de la lista.' },
      { f: '08_Admin_Modal_Detalle_Trabajo.png', t: '8. Modal de Detalle de Trabajo', d: 'Formulario modal para consultar o definir nuevas tareas asignables a los fichajes de los empleados.' },
      { f: '09_Admin_Gestion_Fichajes.png', t: '9. Gestión y Auditoría de Fichajes', d: 'Panel de fichajes con filtros avanzados de fecha adaptativos (icono dinámico claro/oscuro), estado de turnos y botón de eliminación de registros.' },
      { f: '10_Admin_Modal_Mapa_Fichaje.png', t: '10. Ubicación GPS con Mapa Interactivo', d: 'Modal con visor interactivo de mapa Leaflet que posiciona con precisión las coordenadas geográficas capturadas al inicio del turno.' },
      { f: '11_Panel_Empleado_General.png', t: '11. Portal del Empleado (Tema Azul)', d: 'Panel principal del usuario estándar bajo identidad corporativa azul. Acceso directo a Registrar Fichaje y Consulta de Historial.' },
      { f: '12_Empleado_Registrar_Fichaje_Inicial.png', t: '12. Registro de Fichaje (Tarjeta Nueva Jornada)', d: 'Tarjeta principal de registro con selector de tarea y botón Fichar Entrada siempre activo para permitir registros continuos.' },
      { f: '13_Empleado_Fichajes_Activos_Paralelo.png', t: '13. Fichajes Activos Simultáneos en Paralelo', d: 'Recuadros de turnos en curso con exactamente las mismas métricas visuales que la tarjeta superior y botón Finalizar Fichaje en rojo.' },
      { f: '14_Empleado_Fichaje_Finalizado_Toast.png', t: '14. Finalización Inmediata de Fichaje', d: 'Cierre del turno al pulsar el botón rojo: el fichaje se borra de la lista en 0 ms y se presenta la confirmación verde de jornada completada.' },
      { f: '15_Empleado_Consulta_Fichajes.png', t: '15. Consulta de Historial de Fichajes', d: 'Historial de jornadas del empleado con selector de fechas adaptativo, cálculo de horas trabajadas y visualización en tiempo real.' },
      { f: '16_Cerrar_Sesion_Retorno_Login.png', t: '16. Cierre de Sesión Seguro', d: 'Botón de cierre de sesión en barra superior que destruye el almacenamiento local y devuelve al usuario de forma segura a la pantalla inicial.' }
    ].map(item => `
      <div class="screen-card">
        <img class="screen-img" src="file://${path.join(OUTPUT_DIR, item.f).replace(/\\/g, '/')}" alt="${item.t}">
        <div class="screen-info">
          <h3>${item.t}</h3>
          <p>${item.d}</p>
          <div style="font-family: monospace; font-size: 12px; color: #64748b; background: #e2e8f0; padding: 6px 10px; border-radius: 6px; display: inline-block;">
            Archivo: ${item.f}
          </div>
        </div>
      </div>
    `).join('')}
  </div>
</body>
</html>
    `;

    await pdfPage.setContent(htmlContent, { waitUntil: 'networkidle0' });
    const pdfPath = path.join(OUTPUT_DIR, 'Presentacion_Capturas_PWA.pdf');
    await pdfPage.pdf({
      path: pdfPath,
      format: 'A4',
      printBackground: true,
      margin: { top: '15mm', bottom: '15mm', left: '15mm', right: '15mm' }
    });
    console.log('[PDF] Archivo PDF generado exitosamente en:', pdfPath);

  } catch (err) {
    console.error('Error durante la sesión de capturas:', err);
  } finally {
    await browser.close();
  }
}

run();
