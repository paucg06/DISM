"""
========================================================================================
GUÍA Y MANUAL OFICIAL DE USUARIO - PWA CONTROL HORARIO Y GESTIÓN EMPRESARIAL
========================================================================================
Proyecto: Práctica 2 DISM (Desarrollo de Interfaces para Sistemas Móviles)
Autor: Antigravity AI & Pau
Generador: Script automatizado en Python para compilación de Manual de Usuario en PDF.
Diseñado para consumo humano y procesamiento modular por agentes de Inteligencia Artificial.
========================================================================================
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm, inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas


# ======================================================================================
# CONFIGURACIÓN DE RUTAS Y CONSTANTES DE DISEÑO
# ======================================================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

POSSIBLE_IMG_DIRS = [
    os.path.join(SCRIPT_DIR, "Capturas_Responsive_470x900"),
    os.path.join(SCRIPT_DIR, "..", "Capturas_Responsive_470x900"),
    r"C:\Users\paucr\Desktop\Practica_Compilada\Capturas_Responsive_470x900",
    r"C:\Users\paucr\Documents\antigravity\modest-lavoisier\Practica_2\Capturas_Responsive_470x900"
]

IMG_DIR = None
for d in POSSIBLE_IMG_DIRS:
    if os.path.isdir(d):
        IMG_DIR = d
        break

if not IMG_DIR:
    IMG_DIR = os.path.join(SCRIPT_DIR, "Capturas_Responsive_470x900")

OUTPUT_PDF_PATH = os.path.join(SCRIPT_DIR, "Manual_Usuario_PWA_Control_Horario.pdf")

# Paleta corporativa unificada
COLOR_PRIMARY = colors.HexColor("#0F172A")    # Azul noche / Navy profundo
COLOR_ACCENT_BLUE = colors.HexColor("#2563EB")# Azul corporativo empleado
COLOR_ACCENT_GREEN = colors.HexColor("#16A34A")# Verde corporativo admin
COLOR_TEXT_MAIN = colors.HexColor("#1E293B")  # Gris oscuro principal
COLOR_TEXT_MUTED = colors.HexColor("#64748B") # Gris secundario
COLOR_BG_LIGHT = colors.HexColor("#F8FAFC")   # Fondo gris suave
COLOR_BORDER = colors.HexColor("#E2E8F0")     # Borde sutil
COLOR_DANGER = colors.HexColor("#DC2626")     # Rojo advertencia / finalizar


# ======================================================================================
# CANVAS CON NUMERACIÓN AUTOMÁTICA "PÁGINA X DE Y" Y ENCABEZADOS DINÁMICOS
# ======================================================================================
class ManualNumberedCanvas(canvas.Canvas):
    """
    Canvas en dos pasadas que calcula el número total de páginas y estampa
    encabezados y pies de página profesionales en todas las páginas excepto la portada.
    """
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
                self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, total_pages):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(COLOR_TEXT_MUTED)

        # Encabezado superior
        self.drawString(36, 810, "Manual de Usuario Oficial | PWA Control Horario - DISM")
        self.drawRightString(559, 810, "Entrega 2 - Sistema Unificado")
        self.setStrokeColor(COLOR_BORDER)
        self.setLineWidth(0.6)
        self.line(36, 804, 559, 804)

        # Pie de página inferior
        self.line(36, 40, 559, 40)
        self.drawString(36, 28, "Documento Técnico para Evaluación y Guía de Operación")
        page_str = f"Página {self._pageNumber} de {total_pages}"
        self.drawRightString(559, 28, page_str)
        self.restoreState()


# ======================================================================================
# DEFINICIÓN DEL CATÁLOGO COMPLETO DE PANTALLAS Y GUÍA DE INTERACCIÓN
# ======================================================================================
SCREENS_DATA = [
    # -------------------------------------------------------------
    # SECCIÓN 1: ACCESO Y AUTENTICACIÓN
    # -------------------------------------------------------------
    {
        "id": "01",
        "file": "01_Login_Inicio.png",
        "title": "1. Pantalla de Inicio de Sesión",
        "badge": "AUTENTICACIÓN",
        "badge_color": COLOR_PRIMARY,
        "objetivo": "Punto de entrada único y neutral a la plataforma para todos los usuarios.",
        "acceso": "Abrir la aplicación en el navegador o mediante el acceso directo 'Abrir_PWA.bat'.",
        "botones": [
            "<b>Campo Usuario:</b> Introducir el identificador de cuenta (ej. 'admin' o 'sergio').",
            "<b>Campo Contraseña:</b> Introducir la clave de acceso privada.",
            "<b>Botón 'Acceder al Sistema':</b> Valida las credenciales en tiempo real contra el servidor REST."
        ],
        "comportamiento": "Presenta una interfaz minimalista en escala de grises. Dispone de indicador visual de carga durante la comprobación de seguridad."
    },
    {
        "id": "02",
        "file": "02_Login_Error_Contrasena.png",
        "title": "2. Control de Acceso: Contraseña Incorrecta",
        "badge": "SEGURIDAD",
        "badge_color": COLOR_DANGER,
        "objetivo": "Feedback inmediato y no bloqueante ante un intento de acceso no autorizado o clave errónea.",
        "acceso": "Introducir una contraseña no coincidente y pulsar 'Acceder al Sistema'.",
        "botones": [
            "<b>Aviso Emergente (Toast Rojo):</b> Informa 'Usuario o clave incorrectos'.",
            "<b>Reintento Inmediato:</b> La barra de carga se detiene en 0 ms para permitir corregir la clave sin recargar."
        ],
        "comportamiento": "El sistema rechaza la petición con código HTTP 401/400 sin filtrar datos internos y mantiene los campos editables al instante."
    },
    {
        "id": "03",
        "file": "03_Login_Exito_Toast.png",
        "title": "3. Autenticación Exitosa y Saludo",
        "badge": "ACCESO OK",
        "badge_color": COLOR_ACCENT_GREEN,
        "objetivo": "Confirmación visual de bienvenida previa a la redirección según el rol asignado.",
        "acceso": "Introducir credenciales válidas ('admin' / 'admin123' o 'sergio' / '1234') y pulsar acceder.",
        "botones": [
            "<b>Toast de Bienvenida:</b> Muestra 'Bienvenido/a [Nombre de Usuario]'.",
            "<b>Transición Automática:</b> Redirige fluidamente al panel que corresponde al usuario."
        ],
        "comportamiento": "El sistema guarda la sesión de forma segura en almacenamiento local y redirige según el rol: administradores a la vista verde y empleados a la azul."
    },

    # -------------------------------------------------------------
    # SECCIÓN 2: PANEL DEL ADMINISTRADOR (TEMA VERDE)
    # -------------------------------------------------------------
    {
        "id": "04",
        "file": "04_Panel_Admin_General.png",
        "title": "4. Panel Principal del Administrador",
        "badge": "ADMINISTRADOR",
        "badge_color": COLOR_ACCENT_GREEN,
        "objetivo": "Centro de mando integral con identidad corporativa verde para la gestión de la empresa.",
        "acceso": "Iniciar sesión con la cuenta de administrador ('admin').",
        "botones": [
            "<b>Tarjeta 'Gestión de Usuarios':</b> Accede al mantenimiento y control de personal.",
            "<b>Tarjeta 'Gestión de Trabajos':</b> Accede al catálogo de proyectos y actividades.",
            "<b>Tarjeta 'Gestión de Fichajes':</b> Accede a la auditoría horaria y visualización GPS.",
            "<b>Botón Cerrar Sesión (Cabecera):</b> Icono en la barra superior para salir de forma segura."
        ],
        "comportamiento": "Estructura modular con accesos directos destacados y cabecera con el rol activo 'Administrador'."
    },
    {
        "id": "05",
        "file": "05_Admin_Gestion_Usuarios.png",
        "title": "5. Gestión de Usuarios: Listado General",
        "badge": "CRUD USUARIOS",
        "badge_color": COLOR_ACCENT_GREEN,
        "objetivo": "Visualización y administración completa del personal registrado en la organización.",
        "acceso": "Desde el Panel de Admin, pulsar sobre la tarjeta 'Gestión de Usuarios'.",
        "botones": [
            "<b>Elemento de Usuario (Fila):</b> Al pulsar sobre cualquier usuario se abre su modal de edición.",
            "<b>Icono Papelera (Rojo):</b> Abre el diálogo de confirmación para eliminar al usuario.",
            "<b>Botón Inferior 'Añadir Nuevo Usuario':</b> Botón verde al pie para dar de alta nuevo personal."
        ],
        "comportamiento": "Carga inmediata de la plantilla completa al entrar. Distingue visualmente los roles mediante badges de color ('admin' en rojo y 'empleado' en verde)."
    },
    {
        "id": "06",
        "file": "06_Admin_Modal_Detalle_Usuario.png",
        "title": "6. Modal de Edición de Usuario",
        "badge": "MODAL DETALLE",
        "badge_color": COLOR_ACCENT_GREEN,
        "objetivo": "Consultar y actualizar los datos identificativos y de autenticación de un empleado.",
        "acceso": "Hacer clic en cualquier usuario del listado de personal.",
        "botones": [
            "<b>ID Usuario:</b> Campo bloqueado para preservar la integridad referencial.",
            "<b>Nombre Completo, Login y Clave:</b> Campos editables para modificar los datos.",
            "<b>Selector de Rol:</b> Permite conmutar entre 'Administrador' o 'Empleado'.",
            "<b>Botón 'Actualizar Usuario':</b> Guarda los cambios en la base de datos.",
            "<b>Botón 'Cerrar':</b> Cancela y descarta cambios."
        ],
        "comportamiento": "Se abre en una ventana modal emergente nativa sin perder el contexto de la lista principal."
    },
    {
        "id": "07",
        "file": "07_Admin_Modal_Nuevo_Usuario.png",
        "title": "7. Modal de Alta de Nuevo Usuario",
        "badge": "CREACIÓN",
        "badge_color": COLOR_ACCENT_GREEN,
        "objetivo": "Dar de alta un nuevo trabajador o administrador en el sistema corporativo.",
        "acceso": "Pulsar el botón verde inferior 'Añadir Nuevo Usuario' en la pantalla de usuarios.",
        "botones": [
            "<b>Campos de Formulario:</b> ID numérico obligatorio, Nombre completo, Nombre de usuario y Contraseña.",
            "<b>Selector de Rol:</b> Define los permisos de acceso a la plataforma.",
            "<b>Botón 'Crear Usuario':</b> Valida los campos y persiste el nuevo registro.",
            "<b>Botón 'Cerrar':</b> Cierra el formulario modal."
        ],
        "comportamiento": "Tras la creación satisfactoria, la lista principal se actualiza automáticamente con el nuevo integrante."
    },
    {
        "id": "08",
        "file": "08_Admin_Gestion_Trabajos.png",
        "title": "8. Catálogo de Trabajos y Proyectos",
        "badge": "CATÁLOGO",
        "badge_color": COLOR_ACCENT_GREEN,
        "objetivo": "Administrar las tareas, actividades y proyectos a los que imputarán sus jornadas los empleados.",
        "acceso": "Desde el Panel de Admin, pulsar sobre la tarjeta 'Gestión de Trabajos'.",
        "botones": [
            "<b>Elemento de Trabajo (Fila):</b> Abre el modal para ver o modificar el nombre y código.",
            "<b>Icono Papelera:</b> Permite eliminar el trabajo tras confirmar la acción.",
            "<b>Botón Inferior 'Crear Nuevo Trabajo':</b> Botón verde ubicado al final de la lista."
        ],
        "comportamiento": "Renderizado instantáneo del catálogo completo. Cada trabajo cuenta con su código identificador (#ID)."
    },
    {
        "id": "09",
        "file": "09_Admin_Modal_Detalle_Trabajo.png",
        "title": "9. Modal de Detalle de Trabajo",
        "badge": "MODAL DETALLE",
        "badge_color": COLOR_ACCENT_GREEN,
        "objetivo": "Inspeccionar o renombrar una tarea existente en el catálogo empresarial.",
        "acceso": "Hacer clic en cualquier trabajo de la lista.",
        "botones": [
            "<b>ID Trabajo:</b> Código numérico del proyecto.",
            "<b>Nombre del Trabajo:</b> Denominación descriptiva de la actividad.",
            "<b>Botón 'Guardar Trabajo':</b> Persiste las modificaciones introducidas.",
            "<b>Botón 'Cerrar':</b> Cierra la ventana emergente."
        ],
        "comportamiento": "Actualiza la denominación de la tarea de forma transparente para todos los empleados vinculados."
    },
    {
        "id": "10",
        "file": "10_Admin_Modal_Nuevo_Trabajo.png",
        "title": "10. Modal de Creación de Nuevo Trabajo",
        "badge": "CREACIÓN",
        "badge_color": COLOR_ACCENT_GREEN,
        "objetivo": "Registrar un nuevo proyecto asignable para los fichajes de la plantilla.",
        "acceso": "Pulsar el botón verde 'Crear Nuevo Trabajo' al pie del catálogo.",
        "botones": [
            "<b>ID Trabajo (Numérico):</b> Identificador único para el proyecto.",
            "<b>Nombre del Trabajo:</b> Título descriptivo (ej. 'Mantenimiento Preventivo').",
            "<b>Botón 'Guardar Trabajo':</b> Crea el proyecto y lo habilita para fichajes.",
            "<b>Botón 'Cerrar':</b> Descarta el registro."
        ],
        "comportamiento": "El nuevo trabajo queda disponible de forma instantánea en los selectores del Portal del Empleado."
    },
    {
        "id": "11",
        "file": "11_Admin_Gestion_Fichajes.png",
        "title": "11. Auditoría y Control Global de Fichajes",
        "badge": "AUDITORÍA",
        "badge_color": COLOR_ACCENT_GREEN,
        "objetivo": "Supervisar todos los registros de entrada y salida, horas calculadas y geolocalización.",
        "acceso": "Desde el Panel de Admin, pulsar sobre 'Gestión de Fichajes'.",
        "botones": [
            "<b>Filtro por Empleado:</b> Desplegable para aislar los turnos de un usuario específico.",
            "<b>Filtros Fecha Inicio / Fin:</b> Selectores nativos con icono de calendario adaptativo.",
            "<b>Botón 'Aplicar Filtros':</b> Refresca los registros según los criterios seleccionados.",
            "<b>Botón 'Ver Mapa de Fichaje':</b> Abre el visor interactivo Leaflet.",
            "<b>Botón Papelera (Rojo):</b> Permite al administrador borrar fichajes erróneos."
        ],
        "comportamiento": "Muestra distintivos de estado ('Completado' o 'Abierto <12h') y horas totales de trabajo computadas."
    },
    {
        "id": "12",
        "file": "12_Admin_Modal_Mapa_Fichaje.png",
        "title": "12. Ubicación GPS con Mapa Interactivo Leaflet",
        "badge": "GEOLOCALIZACIÓN",
        "badge_color": COLOR_ACCENT_GREEN,
        "objetivo": "Verificar con precisión geográfica el lugar exacto donde el empleado inició su jornada.",
        "acceso": "Pulsar el botón 'Ver Mapa de Fichaje' en cualquiera de las tarjetas de fichaje.",
        "botones": [
            "<b>Visor de Mapa Leaflet:</b> Zoom y desplazamiento interactivo sobre OpenStreetMap.",
            "<b>Chincheta / Marcador GPS:</b> Indica las coordenadas de entrada y abre popup con nombre y hora.",
            "<b>Botón 'Cerrar':</b> Cierra el modal y regresa a la tabla de fichajes."
        ],
        "comportamiento": "Carga dinámica de teselas cartográficas en alta resolución basada en las coordenadas reales capturadas por el dispositivo móvil."
    },

    # -------------------------------------------------------------
    # SECCIÓN 3: PORTAL DEL EMPLEADO (TEMA AZUL)
    # -------------------------------------------------------------
    {
        "id": "13",
        "file": "13_Panel_Empleado_General.png",
        "title": "13. Portal del Empleado: Menú Principal",
        "badge": "EMPLEADO",
        "badge_color": COLOR_ACCENT_BLUE,
        "objetivo": "Entorno simplificado y enfocado en la operativa diaria del trabajador bajo identidad azul.",
        "acceso": "Iniciar sesión con cuenta de empleado estándar ('sergio' / '1234').",
        "botones": [
            "<b>Tarjeta 'Registrar Fichaje':</b> Accede al panel de inicio y cierre de jornadas laborales.",
            "<b>Tarjeta 'Consulta de Fichajes':</b> Historial personal de turnos y horas trabajadas.",
            "<b>Botón Cerrar Sesión (Cabecera):</b> Icono en barra superior para salir."
        ],
        "comportamiento": "Saludo personalizado con el nombre del usuario conectado y acceso en un clic a las funciones habituales."
    },
    {
        "id": "14",
        "file": "14_Empleado_Registrar_Fichaje_Inicial.png",
        "title": "14. Registrar Fichaje: Tarjeta Nueva Jornada",
        "badge": "FICHAJE",
        "badge_color": COLOR_ACCENT_BLUE,
        "objetivo": "Iniciar el registro de una nueva actividad o turno de trabajo con geolocalización.",
        "acceso": "Desde el menú del empleado, pulsar sobre 'Registrar Fichaje'.",
        "botones": [
            "<b>Selector 'Seleccionar Trabajo':</b> Desplegable con todos los proyectos asignables.",
            "<b>Botón 'Fichar Entrada':</b> Registra la entrada actual e inicia el turno."
        ],
        "comportamiento": "La tarjeta de 'Nueva Jornada' permanece siempre activa en la parte superior, permitiendo iniciar tareas de forma continua sin bloquearse."
    },
    {
        "id": "15",
        "file": "15_Empleado_Fichaje_Activo_Unico.png",
        "title": "15. Fichaje en Curso Detectado",
        "badge": "TURNO ACTIVO",
        "badge_color": COLOR_ACCENT_BLUE,
        "objetivo": "Confirmación inmediata del turno iniciado mostrada debajo con métricas visuales homologadas.",
        "acceso": "Pulsar el botón 'Fichar Entrada'.",
        "botones": [
            "<b>Tarjeta 'Fichaje en Curso':</b> Muestra badge 'En Curso', nombre del proyecto y hora exacta.",
            "<b>Botón Rojo 'Finalizar Fichaje':</b> Cierra la jornada laboral de dicha tarea específica."
        ],
        "comportamiento": "Aparece de forma instantánea (0 ms) debajo de la tarjeta superior, respetando las mismas proporciones y estilo corporativo."
    },
    {
        "id": "16",
        "file": "16_Empleado_Fichajes_Activos_Paralelo.png",
        "title": "16. Multitarea: Turnos Simultáneos en Paralelo",
        "badge": "MULTITAREA",
        "badge_color": COLOR_ACCENT_BLUE,
        "objetivo": "Permitir al trabajador imputar horas a múltiples tareas o proyectos abiertos al mismo tiempo.",
        "acceso": "Con un turno ya abierto, seleccionar otra tarea arriba y pulsar de nuevo 'Fichar Entrada'.",
        "botones": [
            "<b>Contador Dinámico:</b> Indica 'X activos' en la cabecera de turnos.",
            "<b>Tarjetas Independientes:</b> Cada turno cuenta con su propia información y su propio botón de cierre rojo."
        ],
        "comportamiento": "El sistema gestiona de forma paralela el cronometraje de cada actividad sin que una interfiera con la otra."
    },
    {
        "id": "17",
        "file": "17_Empleado_Fichaje_Finalizado_Toast.png",
        "title": "17. Finalización de Turno y Notificación Toast",
        "badge": "CIERRE TURNO",
        "badge_color": COLOR_ACCENT_GREEN,
        "objetivo": "Cierre de jornada con eliminación inmediata de la tarjeta activa y confirmación visual.",
        "acceso": "Pulsar el botón rojo 'Finalizar Fichaje' en la tarjeta del turno que se desea concluir.",
        "botones": [
            "<b>Aviso Verde Toast:</b> Muestra 'El fichaje ha finalizado para: [Nombre Tarea]'.",
            "<b>Borrado Inmediato:</b> La tarjeta finalizada desaparece al instante de la pantalla (0 ms)."
        ],
        "comportamiento": "Calcula el total de horas trabajadas y persiste la hora de salida en la base de datos en segundo plano."
    },
    {
        "id": "18",
        "file": "18_Empleado_Consulta_Fichajes.png",
        "title": "18. Consulta de Historial de Fichajes",
        "badge": "HISTORIAL",
        "badge_color": COLOR_ACCENT_BLUE,
        "objetivo": "Consultar las jornadas previas del trabajador, fechas de entrada/salida y cómputo de horas.",
        "acceso": "Desde el portal del empleado, pulsar sobre 'Consulta de Fichajes'.",
        "botones": [
            "<b>Selectores de Fecha ('Desde' y 'Hasta'):</b> Filtro por rango temporal.",
            "<b>Icono de Calendario Adaptativo:</b> Se adapta automáticamente al tema claro/oscuro del sistema.",
            "<b>Cómputo de Horas:</b> Muestra el tiempo invertido en cada turno realizado."
        ],
        "comportamiento": "Presenta el histórico ordenado cronológicamente con indicadores de estado de cada jornada."
    },
    {
        "id": "19",
        "file": "19_Cerrar_Sesion_Retorno_Login.png",
        "title": "19. Cierre Seguro de Sesión y Desconexión",
        "badge": "DESCONEXIÓN",
        "badge_color": COLOR_PRIMARY,
        "objetivo": "Destruir de forma segura los tokens de sesión en el navegador y volver a la pantalla de login.",
        "acceso": "Pulsar el botón con el icono de salida en la esquina superior derecha de cualquier pantalla.",
        "botones": [
            "<b>Icono Salir (Cabecera):</b> Limpia el almacenamiento de sesión ('localStorage').",
            "<b>Retorno al Login:</b> Vuelve a presentar la pantalla de acceso limpia."
        ],
        "comportamiento": "Evita accesos indebidos si el dispositivo es compartido entre distintos trabajadores de la empresa."
    }
]


# ======================================================================================
# CONSTRUCTOR PRINCIPAL DEL DOCUMENTO PDF
# ======================================================================================
def construir_manual_pdf(pdf_path=OUTPUT_PDF_PATH, img_dir=IMG_DIR):
    """
    Compila el manual de usuario oficial en PDF utilizando ReportLab Platypus.
    Integra las 19 capturas de pantalla responsive emparejadas con explicaciones técnicas.
    """
    print(f"[INICIO] Generando Manual de Usuario en PDF: {pdf_path}")
    print(f"[RECURSOS] Directorio de capturas: {img_dir}")

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()

    # Estilos tipográficos personalizados
    style_cover_title = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=COLOR_PRIMARY,
        alignment=1, # Centrado
        spaceAfter=12
    )

    style_cover_sub = ParagraphStyle(
        'CoverSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=15,
        leading=22,
        textColor=COLOR_ACCENT_BLUE,
        alignment=1,
        spaceAfter=25
    )

    style_cover_desc = ParagraphStyle(
        'CoverDesc',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=17,
        textColor=COLOR_TEXT_MAIN,
        alignment=1,
        spaceAfter=30
    )

    style_chapter_h1 = ParagraphStyle(
        'ChapterH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=COLOR_PRIMARY,
        spaceBefore=15,
        spaceAfter=10
    )

    style_card_title = ParagraphStyle(
        'CardTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=COLOR_PRIMARY
    )

    style_badge = ParagraphStyle(
        'BadgeStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=1
    )

    style_field_label = ParagraphStyle(
        'FieldLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=COLOR_PRIMARY
    )

    style_field_val = ParagraphStyle(
        'FieldVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=COLOR_TEXT_MAIN
    )

    style_btn_item = ParagraphStyle(
        'BtnItem',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=COLOR_TEXT_MAIN
    )

    story = []

    # -------------------------------------------------------------
    # 1. PÁGINA DE PORTADA
    # -------------------------------------------------------------
    story.append(Spacer(1, 40))
    story.append(Paragraph("MANUAL DE USUARIO OFICIAL", style_cover_title))
    story.append(Paragraph("Sistema Unificado de Control Horario y Gestión PWA", style_cover_sub))
    story.append(HRFlowable(width="80%", thickness=2, color=COLOR_ACCENT_BLUE, spaceBefore=5, spaceAfter=25))

    story.append(Paragraph(
        "<b>Práctica 2 DISM</b> &mdash; Desarrollo de Interfaces para Sistemas Móviles<br/>"
        "Guía completa de interacción, control de accesos por roles, gestión multitarea de turnos en paralelo, "
        "auditoría con mapas Leaflet GPS y catálogo visual a resolución responsive 470x900 px.",
        style_cover_desc
    ))

    # Tabla resumen de roles en portada
    roles_table_data = [
        [
            Paragraph("<b>Perfil</b>", style_field_label),
            Paragraph("<b>Identidad Visual</b>", style_field_label),
            Paragraph("<b>Credenciales Demo</b>", style_field_label),
            Paragraph("<b>Alcance Funcional Principal</b>", style_field_label)
        ],
        [
            Paragraph("<b>Administrador</b>", style_field_val),
            Paragraph("<font color='#16A34A'><b>Tema Verde</b></font>", style_field_val),
            Paragraph("<b>admin</b> / admin123", style_field_val),
            Paragraph("CRUD de Usuarios y Trabajos, Auditoría global de turnos, Visor Leaflet GPS y eliminación de registros.", style_field_val)
        ],
        [
            Paragraph("<b>Empleado</b>", style_field_val),
            Paragraph("<font color='#2563EB'><b>Tema Azul</b></font>", style_field_val),
            Paragraph("<b>sergio</b> / 1234", style_field_val),
            Paragraph("Registro de turnos en tiempo real, soporte multitarea en paralelo, finalización y consulta histórica con cálculo de horas.", style_field_val)
        ]
    ]

    roles_table = Table(roles_table_data, colWidths=[85, 95, 100, 243])
    roles_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_BG_LIGHT),
        ('TEXTCOLOR', (0, 0), (-1, 0), COLOR_PRIMARY),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('BOX', (0, 0), (-1, -1), 1, COLOR_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
    ]))
    story.append(roles_table)

    story.append(Spacer(1, 40))

    meta_info = Paragraph(
        "<font size='8' color='#64748B'>"
        "<b>Entorno:</b> Ionic Framework / Angular / Node.js Express / Leaflet / SQLite / PWA Standalone<br/>"
        "<b>Resolución de Captura:</b> Formato Móvil 470 x 900 px (Device Scale Factor 2x)<br/>"
        "<b>Fecha de Edición:</b> Noviembre 2026 &mdash; Versión 2.0 Unificada"
        "</font>",
        ParagraphStyle('MetaInfo', parent=styles['Normal'], alignment=1)
    )
    story.append(meta_info)

    story.append(PageBreak())

    # -------------------------------------------------------------
    # 2. CAPÍTULOS DETALLADOS CON CAPTURAS INTEGRADAS
    # -------------------------------------------------------------
    # Agrupamos las pantallas por bloques temáticos
    bloques = [
        ("CAPÍTULO 1: ACCESO, AUTENTICACIÓN Y SEGURIDAD", SCREENS_DATA[0:3]),
        ("CAPÍTULO 2: PANEL DE ADMINISTRACIÓN (TEMA VERDE)", SCREENS_DATA[3:12]),
        ("CAPÍTULO 3: PORTAL DEL EMPLEADO Y TURNOS EN PARALELO (TEMA AZUL)", SCREENS_DATA[12:19])
    ]

    img_width_pt = 135
    img_height_pt = 258 # Mantiene proporción 470x900 (~1:1.91)
    text_col_width = 375

    for titulo_capitulo, pantallas in bloques:
        story.append(Paragraph(titulo_capitulo, style_chapter_h1))
        story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_PRIMARY, spaceBefore=2, spaceAfter=14))

        for item in pantallas:
            img_path = os.path.join(img_dir, item["file"])

            # Carga de la imagen o placeholder en caso de ausencia
            if os.path.isfile(img_path):
                img_flowable = Image(img_path, width=img_width_pt, height=img_height_pt)
            else:
                img_flowable = Paragraph(f"<font color='red'>[Imagen no encontrada:<br/>{item['file']}]</font>", style_field_val)

            # Contenido explicativo de la columna derecha
            right_content = []

            # Encabezado con título e insignia de rol
            badge_html = f"<font color='white'><b>&nbsp;{item['badge']}&nbsp;</b></font>"
            header_table_data = [
                [
                    Paragraph(item["title"], style_card_title),
                    Paragraph(badge_html, style_badge)
                ]
            ]
            header_table = Table(header_table_data, colWidths=[285, 90])
            header_table.setStyle(TableStyle([
                ('BACKGROUND', (1, 0), (1, 0), item["badge_color"]),
                ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('LEFTPADDING', (1, 0), (1, 0), 4),
                ('RIGHTPADDING', (1, 0), (1, 0), 4),
            ]))
            right_content.append(header_table)
            right_content.append(Spacer(1, 6))

            # Objetivo
            right_content.append(Paragraph("<b>Objetivo:</b> " + item["objetivo"], style_field_val))
            right_content.append(Spacer(1, 4))

            # Cómo acceder
            right_content.append(Paragraph("<b>Cómo acceder:</b> " + item["acceso"], style_field_val))
            right_content.append(Spacer(1, 5))

            # Botones e interacciones disponibles
            right_content.append(Paragraph("<b>Interacciones y botones disponibles:</b>", style_field_label))
            for b in item["botones"]:
                right_content.append(Paragraph(f"&bull; {b}", style_btn_item))
            right_content.append(Spacer(1, 5))

            # Comportamiento del sistema
            right_content.append(Paragraph("<b>Comportamiento del sistema:</b>", style_field_label))
            right_content.append(Paragraph(item["comportamiento"], style_btn_item))

            # Empaquetar en tarjeta horizontal de 2 columnas
            card_data = [[img_flowable, right_content]]
            card_table = Table(card_data, colWidths=[img_width_pt + 10, text_col_width])
            card_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), COLOR_BG_LIGHT),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('BOX', (0, 0), (-1, -1), 1, COLOR_BORDER),
            ]))

            # KeepTogether asegura que cada tarjeta completa se mantenga en la misma página
            story.append(KeepTogether([card_table, Spacer(1, 14)]))

        story.append(PageBreak())

    # -------------------------------------------------------------
    # 3. CAPÍTULO 4: RESUMEN OPERATIVO Y MATRIZ DE BOTONES
    # -------------------------------------------------------------
    story.append(Paragraph("CAPÍTULO 4: RESUMEN DE BOTONES Y OPERACIONES CLAVE", style_chapter_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_PRIMARY, spaceBefore=2, spaceAfter=14))

    story.append(Paragraph(
        "A continuación se sintetiza el mapa de navegación y las acciones asociadas a cada botón "
        "fundamental implementado en el sistema:",
        style_field_val
    ))
    story.append(Spacer(1, 10))

    matriz_data = [
        [
            Paragraph("<b>Módulo / Pantalla</b>", style_field_label),
            Paragraph("<b>Botón / Control</b>", style_field_label),
            Paragraph("<b>Color / Aspecto</b>", style_field_label),
            Paragraph("<b>Acción Ejecutada</b>", style_field_label)
        ],
        [
            Paragraph("Login", style_field_val),
            Paragraph("Acceder al Sistema", style_field_val),
            Paragraph("Gris Corporativo", style_field_val),
            Paragraph("Valida credenciales en el servidor y redirige al panel según rol.", style_field_val)
        ],
        [
            Paragraph("Gestión Usuarios", style_field_val),
            Paragraph("Fila de Usuario", style_field_val),
            Paragraph("Ítem con avatar", style_field_val),
            Paragraph("Abre modal emergente de consulta y edición de usuario.", style_field_val)
        ],
        [
            Paragraph("Gestión Usuarios", style_field_val),
            Paragraph("Añadir Nuevo Usuario", style_field_val),
            Paragraph("Verde inferior", style_field_val),
            Paragraph("Abre modal en blanco para crear un nuevo usuario con ID y rol.", style_field_val)
        ],
        [
            Paragraph("Gestión Trabajos", style_field_val),
            Paragraph("Crear Nuevo Trabajo", style_field_val),
            Paragraph("Verde inferior", style_field_val),
            Paragraph("Abre modal para dar de alta un nuevo proyecto asignable.", style_field_val)
        ],
        [
            Paragraph("Gestión Fichajes", style_field_val),
            Paragraph("Ver Mapa de Fichaje", style_field_val),
            Paragraph("Verde contorno", style_field_val),
            Paragraph("Abre modal con visor interactivo Leaflet y coordenadas GPS.", style_field_val)
        ],
        [
            Paragraph("Gestión Fichajes", style_field_val),
            Paragraph("Eliminar Fichaje", style_field_val),
            Paragraph("Rojo papelera", style_field_val),
            Paragraph("Borra el registro tras diálogo de confirmación de seguridad.", style_field_val)
        ],
        [
            Paragraph("Registrar Fichaje", style_field_val),
            Paragraph("Fichar Entrada", style_field_val),
            Paragraph("Azul siempre activo", style_field_val),
            Paragraph("Inicia turno, muestra tarjeta en curso abajo y permite fichajes paralelos.", style_field_val)
        ],
        [
            Paragraph("Fichaje en Curso", style_field_val),
            Paragraph("Finalizar Fichaje", style_field_val),
            Paragraph("Rojo bloque", style_field_val),
            Paragraph("Cierra el turno específico, borra el recuadro (0 ms) y emite toast verde.", style_field_val)
        ],
        [
            Paragraph("Todas las vistas", style_field_val),
            Paragraph("Icono Salir (Cabecera)", style_field_val),
            Paragraph("Icono transparente", style_field_val),
            Paragraph("Cierra la sesión, destruye almacenamiento local y retorna al login.", style_field_val)
        ]
    ]

    matriz_table = Table(matriz_data, colWidths=[105, 115, 95, 208])
    matriz_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_BG_LIGHT),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('BOX', (0, 0), (-1, -1), 1, COLOR_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
    ]))
    story.append(matriz_table)

    # -------------------------------------------------------------
    # COMPILACIÓN DEL DOCUMENTO
    # -------------------------------------------------------------
    doc.build(story, canvasmaker=ManualNumberedCanvas)
    print(f"[EXITO] Manual de Usuario generado satisfactoriamente en: {pdf_path}")
    return pdf_path


if __name__ == "__main__":
    construir_manual_pdf()
