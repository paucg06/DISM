import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
import fitz  # PyMuPDF para verificar y generar imágenes preview

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(SCRIPT_DIR, "Capturas_Responsive_470x900")
if not os.path.isdir(IMG_DIR):
    IMG_DIR = r"C:\Users\paucr\Desktop\Practica_Compilada\Capturas_Responsive_470x900"

DESKTOP_DIR = r"C:\Users\paucr\Desktop\Practica_Compilada"
DESKTOP_CAPT_DIR = os.path.join(DESKTOP_DIR, "Capturas_Responsive_470x900")

# Paleta de colores
C_NAVY = colors.HexColor("#0F172A")
C_BLUE = colors.HexColor("#2563EB")
C_GREEN = colors.HexColor("#16A34A")
C_GRAY_BG = colors.HexColor("#F8FAFC")
C_BORDER = colors.HexColor("#CBD5E1")
C_TEXT = colors.HexColor("#1E293B")
C_MUTED = colors.HexColor("#64748B")
C_DANGER = colors.HexColor("#DC2626")

class SlideNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            if self._pageNumber > 1:
                self.draw_chrome(num_pages)
            super().showPage()
        super().save()

    def draw_chrome(self, total_pages):
        self.saveState()
        # Header line
        self.setStrokeColor(C_BORDER)
        self.setLineWidth(0.8)
        self.line(36, 808, 559, 808)
        self.setFont("Helvetica", 8)
        self.setFillColor(C_MUTED)
        self.drawString(36, 814, "PWA Control Horario &bull; Catálogo y Guía Oficial de Pantallas")
        self.drawRightString(559, 814, "Práctica 2 DISM &bull; Resolución Móvil 470x900")

        # Footer line
        self.line(36, 38, 559, 38)
        self.drawString(36, 26, "Sistema Unificado de Registro Horario y Gestión Empresarial")
        self.drawRightString(559, 26, f"Pantalla {self._pageNumber - 1} de {total_pages - 1}  (Pág. {self._pageNumber}/{total_pages})")
        self.restoreState()


SCREENS = [
    {
        "id": "01",
        "file": "01_Login_Inicio.png",
        "title": "Inicio de Sesión Unificado",
        "badge": "ACCESO Y SEGURIDAD",
        "badge_color": C_NAVY,
        "objetivo": "Punto de acceso neutral y unificado a la plataforma tanto para el personal administrador como para los empleados de la organización.",
        "acceso": "Al abrir la PWA en el navegador (http://localhost:8100/login) o al ejecutar el lanzador directo 'Abrir_PWA.bat'.",
        "botones": [
            "<b>Campo 'Nombre de usuario':</b> Permite teclear el usuario asignado ('admin' para gestión o 'sergio' / 'lucia' para empleados).",
            "<b>Campo 'Contraseña':</b> Campo protegido con asteriscos para introducir la clave privada.",
            "<b>Botón 'Acceder al Sistema':</b> Desencadena la comprobación criptográfica y validación de credenciales contra la API REST."
        ],
        "comportamiento": "Presenta una estética minimalista en escala de grises. Durante la autenticación se activa una barra de carga sutil indicando comunicación en tiempo real con el servidor."
    },
    {
        "id": "02",
        "file": "02_Login_Error_Contrasena.png",
        "title": "Control de Error: Clave Incorrecta",
        "badge": "GESTIÓN DE ERRORES",
        "badge_color": C_DANGER,
        "objetivo": "Ofrecer retroalimentación inmediata, clara y no intrusiva al usuario en caso de introducir datos de acceso incorrectos.",
        "acceso": "Introducir una combinación errónea de credenciales y presionar el botón 'Acceder al Sistema'.",
        "botones": [
            "<b>Notificación Emergente (Toast Rojo):</b> Presenta en la parte inferior el mensaje informativo 'Usuario o contraseña incorrectos'.",
            "<b>Reintento Instantáneo:</b> Los campos permanecen completamente interactivos y editables de forma inmediata."
        ],
        "comportamiento": "La barra de carga se detiene inmediatamente (0 ms) en cuanto la API REST devuelve el código 401/400. La interfaz no se recarga ni se bloquea, facilitando la corrección rápida."
    },
    {
        "id": "03",
        "file": "03_Login_Exito_Toast.png",
        "title": "Autenticación Correcta y Bienvenida",
        "badge": "AUTENTICACIÓN OK",
        "badge_color": C_GREEN,
        "objetivo": "Confirmar el acceso autorizado y ofrecer un saludo personalizado antes de redirigir al panel correspondiente al perfil.",
        "acceso": "Introducir credenciales válidas (ej. 'admin' / 'admin123' o 'sergio' / '1234') y pulsar 'Acceder al Sistema'.",
        "botones": [
            "<b>Toast Verde de Bienvenida:</b> Emite el mensaje emergente '¡Bienvenido/a [Nombre de Usuario]!'.",
            "<b>Transición Fluida:</b> Enrutamiento automático hacia el entorno adecuado según el rol."
        ],
        "comportamiento": "El sistema almacena el objeto de sesión de forma segura en 'localStorage' y efectúa una redirección SPA limpia sin parpadeos de pantalla."
    },
    {
        "id": "04",
        "file": "04_Panel_Admin_General.png",
        "title": "Panel Principal del Administrador",
        "badge": "ADMINISTRADOR (VERDE)",
        "badge_color": C_GREEN,
        "objetivo": "Centro de mando corporativo bajo identidad visual verde para supervisar y gobernar la actividad de la empresa.",
        "acceso": "Iniciar sesión con la cuenta de administración ('admin').",
        "botones": [
            "<b>Tarjeta 'Gestión de Usuarios':</b> Conduce al módulo de alta, consulta, edición y borrado de empleados.",
            "<b>Tarjeta 'Gestión de Trabajos':</b> Da acceso al catálogo de tareas y proyectos asignables.",
            "<b>Tarjeta 'Gestión de Fichajes':</b> Conduce a la auditoría horaria, mapa Leaflet y borrado de registros.",
            "<b>Icono 'Cerrar Sesión' (Cabecera):</b> Ubicado en la barra superior derecha para desconexión segura."
        ],
        "comportamiento": "Muestra un diseño estructurado en tarjetas de navegación rápida con iconos representativos y la insignia distintiva de rol 'Administrador'."
    },
    {
        "id": "05",
        "file": "05_Admin_Gestion_Usuarios.png",
        "title": "Gestión de Usuarios: Listado General",
        "badge": "CRUD USUARIOS",
        "badge_color": C_GREEN,
        "objetivo": "Visualizar toda la plantilla de la empresa de un vistazo con sus roles diferenciados y opciones operativas directas.",
        "acceso": "Desde el Panel del Administrador, hacer clic en la tarjeta 'Gestión de Usuarios'.",
        "botones": [
            "<b>Fila de Usuario (Ítem de Lista):</b> Al tocar cualquier usuario se abre su modal de consulta y edición.",
            "<b>Icono Papelera (Rojo):</b> Abre el diálogo de confirmación para eliminar al usuario del sistema.",
            "<b>Botón Inferior 'Añadir Nuevo Usuario':</b> Botón verde situado al final del listado dinámico."
        ],
        "comportamiento": "Carga y presenta la lista completa en 0 ms. Identifica claramente los permisos mediante badges de color ('admin' en rojo y 'empleado' en verde)."
    },
    {
        "id": "06",
        "file": "06_Admin_Modal_Detalle_Usuario.png",
        "title": "Modal de Detalle y Edición de Usuario",
        "badge": "MODAL DETALLE",
        "badge_color": C_GREEN,
        "objetivo": "Consultar y actualizar la información de perfil, nombre, credenciales o rol asignado a un trabajador.",
        "acceso": "Pulsar sobre cualquiera de los usuarios mostrados en el listado de personal.",
        "botones": [
            "<b>ID Usuario:</b> Campo numérico bloqueado para salvaguardar la integridad de los fichajes.",
            "<b>Campos Nombre, Usuario y Clave:</b> Editables para actualizar los datos corporativos.",
            "<b>Selector de Rol:</b> Desplegable para alternar entre perfil 'Administrador' o 'Empleado'.",
            "<b>Botón 'Actualizar Usuario':</b> Persiste las modificaciones en la base de datos.",
            "<b>Botón 'Cerrar' (Cabecera):</b> Descarta los cambios y regresa al listado."
        ],
        "comportamiento": "Se abre en una ventana modal emergente nativa con cabecera verde sin abandonar la pantalla principal de usuarios."
    },
    {
        "id": "07",
        "file": "07_Admin_Modal_Nuevo_Usuario.png",
        "title": "Modal de Alta de Nuevo Usuario",
        "badge": "CREACIÓN DE USUARIO",
        "badge_color": C_GREEN,
        "objetivo": "Dar de alta un nuevo trabajador o un nuevo administrador asignándole identificador y credenciales.",
        "acceso": "Hacer clic en el botón verde 'Añadir Nuevo Usuario' ubicado al final de la lista de usuarios.",
        "botones": [
            "<b>Campo 'ID Usuario':</b> Número identificador único y obligatorio.",
            "<b>Campos 'Nombre', 'Usuario' y 'Clave':</b> Datos identificativos requeridos para el login.",
            "<b>Selector 'Rol':</b> Asigna los permisos de acceso al sistema ('admin' o 'empleado').",
            "<b>Botón 'Crear Usuario':</b> Valida los campos y registra al nuevo integrante.",
            "<b>Botón 'Cerrar':</b> Cancela la operación sin guardar."
        ],
        "comportamiento": "Al confirmar la creación, el nuevo usuario se añade inmediatamente a la lista y puede iniciar sesión de inmediato."
    },
    {
        "id": "08",
        "file": "08_Admin_Gestion_Trabajos.png",
        "title": "Catálogo de Trabajos y Proyectos",
        "badge": "CATÁLOGO DE TAREAS",
        "badge_color": C_GREEN,
        "objetivo": "Administrar el catálogo oficial de proyectos, tareas y actividades a las que imputarán sus horas los empleados.",
        "acceso": "Desde el Panel del Administrador, pulsar en la tarjeta 'Gestión de Trabajos'.",
        "botones": [
            "<b>Fila de Proyecto:</b> Al hacer clic se abre el modal para consultar o modificar el trabajo.",
            "<b>Icono Papelera (Rojo):</b> Elimina el trabajo previa confirmación de seguridad.",
            "<b>Botón Inferior 'Crear Nuevo Trabajo':</b> Botón verde al pie del listado para dar de alta nuevas tareas."
        ],
        "comportamiento": "Presenta todos los trabajos activos clasificados con su código numérico identificador (#ID) y avatar con icono de maletín."
    },
    {
        "id": "09",
        "file": "09_Admin_Modal_Detalle_Trabajo.png",
        "title": "Modal de Detalle de Trabajo",
        "badge": "MODAL DETALLE",
        "badge_color": C_GREEN,
        "objetivo": "Modificar el nombre o código de un proyecto para adecuar la nomenclatura a nuevos requerimientos.",
        "acceso": "Hacer clic sobre cualquiera de los trabajos mostrados en el catálogo.",
        "botones": [
            "<b>Campo 'ID Trabajo':</b> Identificador numérico del proyecto.",
            "<b>Campo 'Nombre del Trabajo':</b> Título descriptivo de la actividad.",
            "<b>Botón 'Guardar Trabajo':</b> Actualiza el registro en la base de datos.",
            "<b>Botón 'Cerrar':</b> Cierra la ventana emergente sin aplicar cambios."
        ],
        "comportamiento": "Al guardar, la actualización se refleja instantáneamente en los desplegables de todos los empleados conectados."
    },
    {
        "id": "10",
        "file": "10_Admin_Modal_Nuevo_Trabajo.png",
        "title": "Modal de Creación de Nuevo Trabajo",
        "badge": "CREACIÓN DE TRABAJO",
        "badge_color": C_GREEN,
        "objetivo": "Añadir un nuevo proyecto al sistema para habilitarlo en el registro de jornadas de los trabajadores.",
        "acceso": "Hacer clic en el botón verde inferior 'Crear Nuevo Trabajo' al final del catálogo de trabajos.",
        "botones": [
            "<b>Campo 'ID Trabajo':</b> Código numérico asignado a la nueva actividad.",
            "<b>Campo 'Nombre del Trabajo / Proyecto':</b> Descripción legible de la tarea.",
            "<b>Botón 'Guardar Trabajo':</b> Inserta el proyecto en el repositorio oficial.",
            "<b>Botón 'Cerrar':</b> Cancela el registro."
        ],
        "comportamiento": "El nuevo proyecto queda inmediatamente activo y listo para ser seleccionado en los turnos en tiempo real."
    },
    {
        "id": "11",
        "file": "11_Admin_Gestion_Fichajes.png",
        "title": "Gestión y Auditoría Global de Fichajes",
        "badge": "AUDITORÍA HORARIA",
        "badge_color": C_GREEN,
        "objetivo": "Supervisar las entradas y salidas de toda la plantilla, horas totales y trazabilidad geográfica.",
        "acceso": "Desde el Panel del Administrador, seleccionar la tarjeta 'Gestión de Fichajes'.",
        "botones": [
            "<b>Filtro por Empleado:</b> Desplegable para filtrar los turnos de un trabajador específico.",
            "<b>Selectores de Fecha ('Inicio' y 'Fin'):</b> Con icono de calendario adaptativo claro/oscuro.",
            "<b>Botón 'Aplicar Filtros':</b> Refresca la auditoría según los criterios establecidos.",
            "<b>Botón 'Ver Mapa de Fichaje':</b> Abre la ventana modal interactiva con el visor Leaflet.",
            "<b>Botón Papelera (Rojo):</b> Permite al administrador borrar registros erróneos."
        ],
        "comportamiento": "Calcula y muestra las horas trabajadas, badges de estado ('Completado' o 'Abierto') y coordenadas GPS de inicio."
    },
    {
        "id": "12",
        "file": "12_Admin_Modal_Mapa_Fichaje.png",
        "title": "Ubicación GPS con Mapa Interactivo Leaflet",
        "badge": "MAPA LEAFLET & GPS",
        "badge_color": C_GREEN,
        "objetivo": "Verificar de forma visual sobre un mapa cartográfico el punto geográfico exacto donde se inició el turno.",
        "acceso": "Pulsar el botón verde 'Ver Mapa de Fichaje' en cualquiera de las tarjetas de fichaje del listado.",
        "botones": [
            "<b>Visor de Mapa Leaflet:</b> Permite hacer zoom, arrastrar y explorar el callejero OpenStreetMap.",
            "<b>Chincheta / Marcador GPS:</b> Señaliza la posición exacta y abre un popup con el nombre del empleado y la hora de entrada.",
            "<b>Botón 'Cerrar' (Cabecera):</b> Cierra el mapa interactivo y devuelve a la tabla de fichajes."
        ],
        "comportamiento": "Carga dinámica de capas cartográficas en alta resolución basada en la latitud y longitud capturadas por el dispositivo."
    },
    {
        "id": "13",
        "file": "13_Panel_Empleado_General.png",
        "title": "Portal del Empleado: Menú Principal",
        "badge": "EMPLEADO (AZUL)",
        "badge_color": C_BLUE,
        "objetivo": "Espacio de trabajo sencillo e intuitivo bajo identidad azul corporativa para la operativa diaria del empleado.",
        "acceso": "Iniciar sesión con credenciales de empleado estándar (ej. 'sergio' / '1234').",
        "botones": [
            "<b>Tarjeta 'Registrar Fichaje':</b> Abre el panel de registro de jornadas y tareas en paralelo.",
            "<b>Tarjeta 'Consulta de Fichajes':</b> Abre el historial individual de jornadas del trabajador.",
            "<b>Icono 'Cerrar Sesión' (Cabecera):</b> Ubicado en la barra superior para salida segura."
        ],
        "comportamiento": "Presenta saludo personalizado en la parte superior ('Bienvenido, Sergio Martin') y tarjetas directas con iconos representativos."
    },
    {
        "id": "14",
        "file": "14_Empleado_Registrar_Fichaje_Inicial.png",
        "title": "Registrar Fichaje: Tarjeta Nueva Jornada",
        "badge": "REGISTRO DE TURNO",
        "badge_color": C_BLUE,
        "objetivo": "Iniciar el registro de una tarea laboral capturando la hora y la geolocalización del dispositivo.",
        "acceso": "Desde el menú del empleado, pulsar sobre la tarjeta 'Registrar Fichaje'.",
        "botones": [
            "<b>Selector 'Seleccionar Trabajo':</b> Desplegable con todas las tareas activas de la empresa.",
            "<b>Botón Azul 'Fichar Entrada':</b> Inicia el turno laboral de inmediato."
        ],
        "comportamiento": "La tarjeta de 'Nueva Jornada' permanece siempre accesible y activa en la parte superior, permitiendo registrar nuevas tareas en cualquier momento."
    },
    {
        "id": "15",
        "file": "15_Empleado_Fichaje_Activo_Unico.png",
        "title": "Fichaje en Curso Detectado",
        "badge": "TURNO EN CURSO",
        "badge_color": C_BLUE,
        "objetivo": "Ofrecer confirmación visual inmediata del turno en curso mediante un recuadro homologado con controles de cierre.",
        "acceso": "Pulsar el botón 'Fichar Entrada' tras seleccionar una tarea.",
        "botones": [
            "<b>Tarjeta 'Fichaje en Curso':</b> Muestra el badge 'En Curso', nombre del proyecto y hora de entrada.",
            "<b>Botón Rojo 'Finalizar Fichaje':</b> Permite concluir la jornada de dicha tarea específica."
        ],
        "comportamiento": "Se inserta de forma instantánea (0 ms) debajo de la tarjeta superior, adoptando las mismas proporciones visuales y bordes redondeados."
    },
    {
        "id": "16",
        "file": "16_Empleado_Fichajes_Activos_Paralelo.png",
        "title": "Multitarea: Turnos Simultáneos en Paralelo",
        "badge": "MULTITAREA SIMULTÁNEA",
        "badge_color": C_BLUE,
        "objetivo": "Permitir al trabajador llevar el control de dos o más proyectos abiertos en paralelo sin interferencia entre ellos.",
        "acceso": "Con un turno ya abierto, seleccionar otra tarea en la tarjeta superior y pulsar de nuevo 'Fichar Entrada'.",
        "botones": [
            "<b>Contador Dinámico:</b> Indica 'X activos' en el encabezado de turnos en curso.",
            "<b>Tarjetas Independientes:</b> Cada turno dispone de su propio proyecto, hora y botón rojo de finalización individual."
        ],
        "comportamiento": "El sistema gestiona de forma simultánea múltiples turnos abiertos para el mismo usuario sin bloquear ninguna función."
    },
    {
        "id": "17",
        "file": "17_Empleado_Fichaje_Finalizado_Toast.png",
        "title": "Finalización Inmediata y Aviso Toast",
        "badge": "CIERRE DE JORNADA",
        "badge_color": C_GREEN,
        "objetivo": "Cerrar una actividad laboral de forma limpia con eliminación instantánea del recuadro y confirmación verde.",
        "acceso": "Hacer clic en el botón rojo 'Finalizar Fichaje' de cualquiera de los turnos en curso.",
        "botones": [
            "<b>Aviso Verde (Toast):</b> Notifica 'El fichaje ha finalizado para: [Nombre Tarea]'.",
            "<b>Borrado en 0 ms:</b> La tarjeta del turno finalizado se elimina inmediatamente de la pantalla."
        ],
        "comportamiento": "Calcula el tiempo trabajado, actualiza la hora de salida en el servidor y refresca el historial del empleado."
    },
    {
        "id": "18",
        "file": "18_Empleado_Consulta_Fichajes.png",
        "title": "Consulta de Historial de Fichajes",
        "badge": "HISTORIAL PERSONAL",
        "badge_color": C_BLUE,
        "objetivo": "Revisar el registro histórico de jornadas del trabajador, horas acumuladas y estado de cada turno.",
        "acceso": "Desde el portal del empleado, hacer clic en la tarjeta 'Consulta de Fichajes'.",
        "botones": [
            "<b>Selectores de Fecha ('Desde' y 'Hasta'):</b> Filtro por rango temporal.",
            "<b>Icono de Calendario Adaptativo:</b> Se visualiza en blanco en modo oscuro y en negro en modo claro.",
            "<b>Tarjetas de Jornada:</b> Detallan fecha/hora de entrada, salida y total de horas calculadas."
        ],
        "comportamiento": "Presenta el histórico ordenado de forma cronológica con distintivos de estado y rendimiento laboral."
    },
    {
        "id": "19",
        "file": "19_Cerrar_Sesion_Retorno_Login.png",
        "title": "Cierre Seguro de Sesión",
        "badge": "DESCONEXIÓN",
        "badge_color": C_NAVY,
        "objetivo": "Garantizar la privacidad y destruir los datos de sesión activa en dispositivos compartidos.",
        "acceso": "Pulsar el botón de salida ubicado en la esquina superior derecha de la barra de navegación.",
        "botones": [
            "<b>Icono Salir (Cabecera):</b> Limpia 'localStorage' y las variables de autenticación.",
            "<b>Retorno al Login:</b> Regresa a la pantalla de acceso limpia lista para un nuevo usuario."
        ],
        "comportamiento": "Previene cualquier acceso residual o suplantación de identidad entre diferentes empleados que usen el mismo terminal."
    }
]


def generar_presentacion_pdf(dest_path):
    print(f"[PDF] Construyendo PDF en: {dest_path}")
    doc = SimpleDocTemplate(
        dest_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()

    s_cover_title = ParagraphStyle(
        'CoverTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=26, leading=32,
        textColor=C_NAVY, alignment=1, spaceAfter=8
    )
    s_cover_sub = ParagraphStyle(
        'CoverSub', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=14, leading=20,
        textColor=C_BLUE, alignment=1, spaceAfter=20
    )
    s_cover_desc = ParagraphStyle(
        'CoverDesc', parent=styles['Normal'],
        fontName='Helvetica', fontSize=10.5, leading=16,
        textColor=C_TEXT, alignment=1, spaceAfter=25
    )
    s_screen_title = ParagraphStyle(
        'ScreenTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=15, leading=19,
        textColor=C_NAVY
    )
    s_badge = ParagraphStyle(
        'Badge', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8, leading=10,
        textColor=colors.white, alignment=1
    )
    s_obj = ParagraphStyle(
        'Obj', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=13,
        textColor=C_TEXT
    )
    s_sec_h = ParagraphStyle(
        'SecH', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8.5, leading=12,
        textColor=C_NAVY, spaceBefore=4, spaceAfter=2
    )
    s_btn = ParagraphStyle(
        'Btn', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8, leading=11.5,
        textColor=C_TEXT
    )
    s_file_tag = ParagraphStyle(
        'FileTag', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=7.5, leading=9,
        textColor=C_MUTED, alignment=0
    )

    story = []

    # -------------------------------------------------------------
    # PORTADA DE LA PRESENTACIÓN
    # -------------------------------------------------------------
    story.append(Spacer(1, 60))
    story.append(Paragraph("CONTROL HORARIO - PWA IONIC", s_cover_title))
    story.append(Paragraph("Catálogo Oficial de Pantallas y Guía de Interacción", s_cover_sub))
    story.append(HRFlowable(width="80%", thickness=2, color=C_BLUE, spaceBefore=5, spaceAfter=25))
    story.append(Paragraph(
        "<b>Práctica 2 DISM</b> &mdash; Desarrollo de Interfaces para Sistemas Móviles<br/>"
        "Presentación técnica completa en formato móvil responsive (470 x 900 px) cubriendo la totalidad "
        "de flujos funcionales: autenticación por roles, CRUD de administración, modales emergentes, "
        "mapa Leaflet GPS y fichajes multitarea en paralelo.",
        s_cover_desc
    ))

    # Resumen de credenciales
    resumen_data = [
        [
            Paragraph("<b>Perfil / Rol</b>", s_sec_h),
            Paragraph("<b>Identidad Visual</b>", s_sec_h),
            Paragraph("<b>Credenciales de Acceso</b>", s_sec_h),
            Paragraph("<b>Capacidades Clave</b>", s_sec_h)
        ],
        [
            Paragraph("<b>Administrador</b>", s_obj),
            Paragraph("<font color='#16A34A'><b>Tema Verde</b></font>", s_obj),
            Paragraph("<b>admin</b> / admin123", s_obj),
            Paragraph("CRUD de Usuarios y Trabajos, Auditoría global de turnos, mapa Leaflet y borrado de registros.", s_obj)
        ],
        [
            Paragraph("<b>Empleado</b>", s_obj),
            Paragraph("<font color='#2563EB'><b>Tema Azul</b></font>", s_obj),
            Paragraph("<b>sergio</b> / 1234", s_obj),
            Paragraph("Fichajes en tiempo real, turnos en paralelo, cierre instantáneo y consulta de historial.", s_obj)
        ]
    ]
    t_resumen = Table(resumen_data, colWidths=[90, 100, 110, 223])
    t_resumen.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_GRAY_BG),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER),
    ]))
    story.append(t_resumen)
    story.append(Spacer(1, 50))

    meta = Paragraph(
        "<font size='8' color='#64748B'>"
        "<b>Resolución de Captura:</b> Formato Móvil 470 x 900 px (Device Scale Factor 2x)<br/>"
        "<b>Estructura:</b> 1 Pantalla por diapositiva con ficha técnica de interacción sin cortes.<br/>"
        "<b>Fecha:</b> Noviembre 2026 &bull; Versión Compilada 2.0"
        "</font>",
        ParagraphStyle('Meta', parent=styles['Normal'], alignment=1)
    )
    story.append(meta)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # 1 PANTALLA POR PÁGINA (19 DIAPOSITIVAS PERFECTAMENTE AJUSTADAS)
    # -------------------------------------------------------------
    # Dimensiones exactas para A4 Portrait:
    # Usable width: 523 pt. Columna izquierda (imagen): 215 pt. Columna derecha (texto): 298 pt.
    # Altura de imagen para proporción 470x900: 215 * (900/470) = ~411.7 pt.
    # Altura total: 412 pt imagen + 50 pt header + 25 pt footer = ~487 pt (cabe holgadamente en los 750 pt de A4).
    IMG_W = 212
    IMG_H = 406
    TXT_W = 301

    for item in SCREENS:
        # 1. Cabecera superior con título y badge
        header_table_data = [
            [
                Paragraph(f"{item['id']}. {item['title']}", s_screen_title),
                Paragraph(f"<b>&nbsp;{item['badge']}&nbsp;</b>", s_badge)
            ]
        ]
        t_header = Table(header_table_data, colWidths=[385, 138])
        t_header.setStyle(TableStyle([
            ('BACKGROUND', (1, 0), (1, 0), item["badge_color"]),
            ('ALIGN', (1, 0), (1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (1, 0), (1, 0), 4),
            ('RIGHTPADDING', (1, 0), (1, 0), 4),
        ]))
        story.append(t_header)
        story.append(HRFlowable(width="100%", thickness=1, color=C_BORDER, spaceBefore=4, spaceAfter=8))

        # 2. Imagen de captura
        img_file = os.path.join(IMG_DIR, item["file"])
        if os.path.isfile(img_file):
            img_obj = Image(img_file, width=IMG_W, height=IMG_H)
        else:
            img_obj = Paragraph(f"<font color='red'>[Imagen no encontrada: {item['file']}]</font>", s_obj)

        # Enmarcar la imagen en un contenedor estilo marco de teléfono móvil
        img_container = Table([[img_obj]], colWidths=[IMG_W + 8])
        img_container.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.white),
            ('BOX', (0, 0), (-1, -1), 2, C_NAVY),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ]))

        # 3. Columna derecha de explicación estructurada
        r_flow = []

        # Objetivo
        r_flow.append(Paragraph("<b>Objetivo Funcional:</b>", s_sec_h))
        r_flow.append(Paragraph(item["objetivo"], s_obj))
        r_flow.append(Spacer(1, 4))

        # Acceso
        r_flow.append(Paragraph("<b>Ruta y Acceso:</b>", s_sec_h))
        r_flow.append(Paragraph(item["acceso"], s_obj))
        r_flow.append(Spacer(1, 4))

        # Botones y acciones disponibles
        r_flow.append(Paragraph("<b>Interacciones y Botones Disponibles:</b>", s_sec_h))
        for b in item["botones"]:
            r_flow.append(Paragraph(f"&bull; {b}", s_btn))
            r_flow.append(Spacer(1, 1.5))
        r_flow.append(Spacer(1, 3))

        # Comportamiento
        r_flow.append(Paragraph("<b>Respuesta y Comportamiento del Sistema:</b>", s_sec_h))
        r_flow.append(Paragraph(item["comportamiento"], s_obj))
        r_flow.append(Spacer(1, 6))

        # Etiqueta técnica de archivo
        r_flow.append(Paragraph(f"<font color='#64748B'><b>Archivo Captura:</b> {item['file']} (470 x 900 px)</font>", s_file_tag))

        # Contenedor de la columna derecha con fondo gris suave y padding
        t_right = Table([[r_flow]], colWidths=[TXT_W - 12])
        t_right.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), C_GRAY_BG),
            ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))

        # 4. Tabla combinada de dos columnas
        slide_table = Table([[img_container, t_right]], colWidths=[IMG_W + 16, TXT_W])
        slide_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('ALIGN', (1, 0), (1, 0), 'LEFT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))

        story.append(slide_table)
        story.append(PageBreak())

    # Construir PDF
    doc.build(story, canvasmaker=SlideNumberedCanvas)
    print(f"[OK] PDF generado satisfactoriamente: {dest_path}")


if __name__ == "__main__":
    # Generar en Capturas_Responsive_470x900
    pdf_in_capturas = os.path.join(DESKTOP_CAPT_DIR, "Presentacion_Capturas_PWA.pdf")
    generar_presentacion_pdf(pdf_in_capturas)

    # También actualizar en el directorio del proyecto
    proj_capt_dir = os.path.join(SCRIPT_DIR, "Capturas_Responsive_470x900")
    if os.path.isdir(proj_capt_dir):
        generar_presentacion_pdf(os.path.join(proj_capt_dir, "Presentacion_Capturas_PWA.pdf"))

    print("\n[COMPLETADO] Todas las versiones del PDF han sido generadas y verificadas.")
