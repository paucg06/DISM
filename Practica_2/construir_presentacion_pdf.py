"""
========================================================================================
GUÍA PARA USUARIOS - CONTROL HORARIO PWA IONIC
========================================================================================
Asignatura: DISM - Dispositivos e Infraestructuras de Sistemas Multimedia
Entrega: Entrega 2: Ionic & REST
Autor: Pau Cremades García
Titulación: 3.er curso del Grado en Ingeniería Multimedia
Institución: Universidad de Alicante (UA)
========================================================================================
"""

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
import fitz

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(SCRIPT_DIR, "Capturas_Responsive_470x900")
if not os.path.isdir(IMG_DIR):
    IMG_DIR = r"C:\Users\paucr\Desktop\Practica_Compilada\Capturas_Responsive_470x900"

DESKTOP_DIR = r"C:\Users\paucr\Desktop\Practica_Compilada"
DESKTOP_CAPT_DIR = os.path.join(DESKTOP_DIR, "Capturas_Responsive_470x900")

# Paleta de colores corporativa
C_NAVY = colors.HexColor("#0F172A")
C_BLUE = colors.HexColor("#2563EB")
C_GREEN = colors.HexColor("#16A34A")
C_GRAY_BG = colors.HexColor("#F8FAFC")
C_BORDER = colors.HexColor("#CBD5E1")
C_TEXT = colors.HexColor("#1E293B")
C_MUTED = colors.HexColor("#64748B")
C_DANGER = colors.HexColor("#DC2626")


# ======================================================================================
# CANVAS CON ENCABEZADOS Y PIES DE PÁGINA FORMALES SOLICITADOS
# ======================================================================================
class UserGuideNumberedCanvas(canvas.Canvas):
    """
    Canvas en dos pasadas que numera las páginas e inserta:
    - Encabezado: 'Práctica 2 DISM' (izq) y 'Pau Cremades García' (dcha).
    - Pie de página: 'Guía para Usuarios • Control Horario PWA Ionic' (izq) y 'Página X de Y' (dcha).
    (Se activa a partir de la página 2).
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
                self.draw_chrome(num_pages)
            super().showPage()
        super().save()

    def draw_chrome(self, total_pages):
        self.saveState()
        # Línea y textos del encabezado superior
        self.setStrokeColor(C_BORDER)
        self.setLineWidth(0.8)
        self.line(36, 808, 559, 808)
        self.setFont("Helvetica-Bold", 8.5)
        self.setFillColor(C_NAVY)
        self.drawString(36, 814, "Práctica 2 DISM")
        self.setFont("Helvetica", 8.5)
        self.setFillColor(C_MUTED)
        self.drawRightString(559, 814, "Pau Cremades García")

        # Línea y textos del pie de página inferior
        self.line(36, 38, 559, 38)
        self.setFont("Helvetica", 8)
        self.setFillColor(C_MUTED)
        self.drawString(36, 26, "Guía para Usuarios • Control Horario PWA Ionic")
        self.drawRightString(559, 26, f"Página {self._pageNumber} de {total_pages}")
        self.restoreState()


# ======================================================================================
# DATOS EXTENSOS DE CADA PANTALLA (ORIENTADOS AL USUARIO FINAL)
# ======================================================================================
SCREENS_DATA = [
    # -------------------------------------------------------------
    # BLOQUE 1: ACCESO, AUTENTICACIÓN Y SEGURIDAD
    # -------------------------------------------------------------
    {
        "id": "01",
        "file": "01_Login_Inicio.png",
        "title": "Inicio de Sesión Unificado",
        "badge": "ACCESO Y SEGURIDAD",
        "badge_color": C_NAVY,
        "objetivo": "Punto de acceso unificado a la aplicación corporativa para toda la plantilla. Permite la identificación y validación segura tanto de administradores como de empleados mediante sus credenciales personales asignadas.",
        "acceso": "Al abrir la aplicación corporativa desde el navegador del dispositivo móvil o mediante el acceso directo de la PWA instalada.",
        "botones": [
            "<b>Campo 'Nombre de usuario':</b> Espacio para introducir el nombre de usuario facilitado por la empresa (por ejemplo, 'admin' para labores directivas o 'sergio' / 'lucia' para trabajadores).",
            "<b>Campo 'Contraseña':</b> Campo protegido mediante caracteres enmascarados para escribir la clave privada asignada a la cuenta.",
            "<b>Botón 'Acceder al Sistema':</b> Al pulsar este botón, la aplicación envía los datos de autenticación de forma segura y comprueba los permisos de acceso al instante."
        ],
        "comportamiento": "Presenta una interfaz limpia y minimalista en escala de grises. Durante la validación se visualiza un indicador de carga animado que certifica la comunicación fluida con los servicios centrales de la organización sin bloquear la interacción."
    },
    {
        "id": "02",
        "file": "02_Login_Error_Contrasena.png",
        "title": "Gestión de Error: Contraseña No Válida",
        "badge": "CONTROL DE ERRORES",
        "badge_color": C_DANGER,
        "objetivo": "Avisar al usuario de forma inmediata y no intrusiva si se han introducido credenciales erróneas o si el usuario no figura registrado en el sistema corporativo.",
        "acceso": "Introducir una contraseña incorrecta en el formulario de acceso y presionar el botón 'Acceder al Sistema'.",
        "botones": [
            "<b>Notificación Emergente (Toast Rojo):</b> Aparece en la zona inferior de la pantalla indicando de forma explícita el mensaje 'Usuario o contraseña incorrectos'.",
            "<b>Edición Inmediata de Campos:</b> Permite hacer clic o tocar de nuevo en el campo de contraseña para corregir el dato tecleado sin necesidad de recargar la aplicación."
        ],
        "comportamiento": "La barra de progreso de carga se detiene en 0 milisegundos en el momento exacto en que se detecta el fallo. La pantalla se mantiene totalmente interactiva, evitando pérdidas de tiempo y permitiendo al usuario volver a intentar el acceso de inmediato."
    },
    {
        "id": "03",
        "file": "03_Login_Exito_Toast.png",
        "title": "Autenticación Correcta y Saludo",
        "badge": "ACCESO AUTORIZADO",
        "badge_color": C_GREEN,
        "objetivo": "Confirmar la validación exitosa de la identidad del usuario y darle la bienvenida antes de conducirlo automáticamente al entorno adaptado a sus permisos laborales.",
        "acceso": "Introducir un nombre de usuario y contraseña válidos y presionar el botón 'Acceder al Sistema'.",
        "botones": [
            "<b>Aviso de Bienvenida (Toast Verde):</b> Muestra en pantalla el mensaje emergente personalizado '¡Bienvenido/a [Nombre]!' para certificar la conexión exitosa.",
            "<b>Transición Automática:</b> Sin necesidad de pulsar ningún botón adicional, la aplicación realiza la redirección hacia el panel principal correspondiente."
        ],
        "comportamiento": "El sistema guarda los datos de sesión de forma segura y abre el entorno correspondiente: si el usuario tiene rol de 'Administrador', se abre el panel general verde con herramientas de supervisión; si tiene rol de 'Empleado', se abre el portal azul de fichajes."
    },

    # -------------------------------------------------------------
    # BLOQUE 2: PANEL DEL ADMINISTRADOR (TEMA VERDE)
    # -------------------------------------------------------------
    {
        "id": "04",
        "file": "04_Panel_Admin_General.png",
        "title": "Panel Principal del Administrador",
        "badge": "ADMINISTRADOR (TEMA VERDE)",
        "badge_color": C_GREEN,
        "objetivo": "Centro de control integral con identidad visual corporativa verde, diseñado para que los responsables de la organización gestionen personal, proyectos y la auditoría horaria de la plantilla.",
        "acceso": "Iniciar sesión con una cuenta de usuario con privilegios de gestión (ej. usuario 'admin').",
        "botones": [
            "<b>Tarjeta 'Gestión de Usuarios':</b> Conduce a la pestaña de administración de personal, donde se consultan, editan, añaden o dan de baja los trabajadores.",
            "<b>Tarjeta 'Gestión de Trabajos':</b> Da acceso al catálogo de tareas y proyectos a los que la plantilla imputará sus jornadas.",
            "<b>Tarjeta 'Gestión de Fichajes':</b> Conduce al módulo de auditoría de jornadas, filtros de fechas, mapas interactivos Leaflet con chincheta GPS y borrado de turnos.",
            "<b>Icono 'Cerrar Sesión' (Barra Superior):</b> Permite salir del sistema y desconectar la cuenta de forma segura."
        ],
        "comportamiento": "Presenta una navegación rápida en tarjetas organizadas por categorías, con iconos distintivos y el badge superior que identifica permanentemente al usuario como 'Administrador'."
    },
    {
        "id": "05",
        "file": "05_Admin_Gestion_Usuarios.png",
        "title": "Gestión de Usuarios: Lista de Personal",
        "badge": "ADMINISTRACIÓN DE PERSONAL",
        "badge_color": C_GREEN,
        "objetivo": "Visualizar el listado completo de trabajadores de la empresa, consultar sus roles laborales asignados y acceder rápidamente a las operaciones de alta, edición y baja.",
        "acceso": "Desde el Panel Principal del Administrador, presionar sobre la tarjeta 'Gestión de Usuarios'.",
        "botones": [
            "<b>Fila de Usuario (Tocar sobre el elemento):</b> Al pulsar sobre cualquier empleado de la lista se abre una ventana modal emergente con su información completa para editarla.",
            "<b>Icono Papelera (Color Rojo):</b> Ubicado a la derecha de cada usuario. Abre una ventana de confirmación para eliminar al trabajador del sistema.",
            "<b>Botón Inferior 'Añadir Nuevo Usuario':</b> Botón verde situado al final del listado dinámico para registrar un nuevo integrante."
        ],
        "comportamiento": "Carga la lista completa de empleados nada más entrar sin necesidad de pulsar botones adicionales. Diferencia los permisos mediante etiquetas de color ('admin' en rojo y 'empleado' en verde)."
    },
    {
        "id": "06",
        "file": "06_Admin_Modal_Detalle_Usuario.png",
        "title": "Modal de Detalle y Edición de Usuario",
        "badge": "MODAL DE EDICIÓN",
        "badge_color": C_GREEN,
        "objetivo": "Consultar de forma detallada y modificar los datos de un empleado, incluyendo su nombre completo, nombre de inicio de sesión, clave de acceso o cambio de rol.",
        "acceso": "Hacer clic o pulsar sobre cualquiera de las filas de usuario en la pantalla de gestión de personal.",
        "botones": [
            "<b>Campo 'ID Usuario':</b> Muestra el código numérico asignado al usuario. Se encuentra protegido contra edición para preservar el historial previo de fichajes.",
            "<b>Campos 'Nombre', 'Usuario' y 'Clave':</b> Permiten actualizar la información personal y restablecer la contraseña.",
            "<b>Selector desplegable 'Rol':</b> Permite conmutar los permisos del usuario entre 'Administrador' o 'Empleado'.",
            "<b>Botón 'Actualizar Usuario':</b> Guarda inmediatamente todos los cambios en la base de datos.",
            "<b>Botón 'Cerrar' (Cabecera):</b> Descarta cualquier modificación y regresa al listado."
        ],
        "comportamiento": "Se despliega como una ventana emergente nativa con cabecera verde sin abandonar la vista del listado general, garantizando agilidad operativa al responsable."
    },
    {
        "id": "07",
        "file": "07_Admin_Modal_Nuevo_Usuario.png",
        "title": "Modal de Alta de Nuevo Usuario",
        "badge": "REGISTRO DE PERSONAL",
        "badge_color": C_GREEN,
        "objetivo": "Dar de alta a un nuevo trabajador o directivo en la organización, asignándole su número de empleado, datos de acceso y nivel de permisos.",
        "acceso": "Presionar el botón verde 'Añadir Nuevo Usuario' ubicado al pie de la lista de usuarios.",
        "botones": [
            "<b>Campo 'ID Usuario':</b> Número identificador obligatorio que representará al trabajador.",
            "<b>Campo 'Nombre Completo':</b> Nombre y apellidos del empleado para las consultas y reportes.",
            "<b>Campo 'Nombre de Usuario':</b> Identificador exclusivo que utilizará para iniciar sesión.",
            "<b>Campo 'Contraseña':</b> Clave de seguridad provisional o definitiva.",
            "<b>Selector 'Rol':</b> Asigna si la cuenta tendrá acceso al portal de empleado o al de administración.",
            "<b>Botón 'Crear Usuario':</b> Valida los campos y persiste el nuevo registro.",
            "<b>Botón 'Cerrar':</b> Cancela el registro y cierra la ventana modal."
        ],
        "comportamiento": "Al confirmar el alta, el nuevo empleado se incorpora inmediatamente a la lista y puede iniciar sesión en la aplicación al instante."
    },
    {
        "id": "08",
        "file": "08_Admin_Gestion_Trabajos.png",
        "title": "Catálogo de Trabajos y Proyectos",
        "badge": "CATÁLOGO DE PROYECTOS",
        "badge_color": C_GREEN,
        "objetivo": "Administrar el catálogo oficial de actividades, tareas y proyectos a los que los empleados imputarán sus horas durante sus turnos laborales.",
        "acceso": "Desde el Panel Principal del Administrador, seleccionar la tarjeta 'Gestión de Trabajos'.",
        "botones": [
            "<b>Fila de Proyecto:</b> Al hacer clic sobre cualquier trabajo se abre la ventana modal para editar su nombre o código.",
            "<b>Icono Papelera (Rojo):</b> Permite eliminar una tarea que ya no esté en curso previa confirmación.",
            "<b>Botón Inferior 'Crear Nuevo Trabajo':</b> Botón verde situado al final de la lista para dar de alta una nueva actividad."
        ],
        "comportamiento": "Muestra todas las tareas vigentes con su identificador (#ID) e icono representativo de maletín. La lista está disponible inmediatamente al acceder a la pestaña."
    },
    {
        "id": "09",
        "file": "09_Admin_Modal_Detalle_Trabajo.png",
        "title": "Modal de Detalle y Edición de Trabajo",
        "badge": "MODAL DE PROYECTO",
        "badge_color": C_GREEN,
        "objetivo": "Inspeccionar o renombrar una tarea existente para adecuar su denominación a nuevas necesidades del centro de trabajo o de los clientes.",
        "acceso": "Pulsar sobre cualquiera de los proyectos que figuran en el catálogo de trabajos.",
        "botones": [
            "<b>Campo 'ID Trabajo':</b> Identificador numérico asociado a la tarea.",
            "<b>Campo 'Nombre del Trabajo / Proyecto':</b> Denominación descriptiva de la actividad laboral.",
            "<b>Botón 'Guardar Trabajo':</b> Actualiza el nombre del proyecto en todo el sistema.",
            "<b>Botón 'Cerrar' (Cabecera):</b> Cierra el formulario modal sin guardar cambios."
        ],
        "comportamiento": "Al guardar los cambios, la nueva denominación se sincroniza de forma transparente en los selectores de fichaje de todos los empleados en tiempo real."
    },
    {
        "id": "10",
        "file": "10_Admin_Modal_Nuevo_Trabajo.png",
        "title": "Modal de Alta de Nuevo Trabajo",
        "badge": "NUEVO PROYECTO",
        "badge_color": C_GREEN,
        "objetivo": "Registrar una nueva tarea o proyecto en el catálogo para que la plantilla pueda seleccionarlo al fichar su entrada.",
        "acceso": "Hacer clic en el botón verde inferior 'Crear Nuevo Trabajo' situado al final del catálogo.",
        "botones": [
            "<b>Campo 'ID Trabajo (Numérico)':</b> Código identificativo de la nueva tarea.",
            "<b>Campo 'Nombre del Trabajo':</b> Título descriptivo (ej. 'Auditoría de Sistemas', 'Soporte Técnico', etc.).",
            "<b>Botón 'Guardar Trabajo':</b> Da de alta el proyecto y lo habilita para el registro de turnos.",
            "<b>Botón 'Cerrar':</b> Descarta el formulario y regresa a la vista general."
        ],
        "comportamiento": "El proyecto recién creado pasa a estar disponible de forma inmediata en el desplegable de tareas de todos los empleados conectados a la aplicación."
    },
    {
        "id": "11",
        "file": "11_Admin_Gestion_Fichajes.png",
        "title": "Gestión y Auditoría Global de Fichajes",
        "badge": "SUPERVISIÓN HORARIA",
        "badge_color": C_GREEN,
        "objetivo": "Supervisar todos los fichajes de entrada y salida de la plantilla, verificar las horas de trabajo acumuladas y acceder a la geolocalización de cada jornada.",
        "acceso": "Desde el Panel Principal del Administrador, presionar en la tarjeta 'Gestión de Fichajes'.",
        "botones": [
            "<b>Selector 'Filtrar por Empleado':</b> Desplegable para consultar los turnos de un trabajador específico o de toda la plantilla conjunta.",
            "<b>Campos de Fecha ('Inicio' y 'Fin'):</b> Selectores de fecha con icono de calendario adaptativo que se ajusta automáticamente al tema claro u oscuro del dispositivo.",
            "<b>Botón 'Aplicar Filtros':</b> Refresca la lista de turnos según los criterios seleccionados.",
            "<b>Botón 'Ver Mapa de Fichaje':</b> Abre la ventana modal interactiva con el visor cartográfico Leaflet.",
            "<b>Botón Papelera (Rojo):</b> Permite al administrador borrar registros de jornada duplicados o erróneos previa confirmación."
        ],
        "comportamiento": "Presenta el histórico detallado con tarjetas individuales que muestran el nombre del trabajador, proyecto imputado, fecha/hora de entrada, salida, total de horas calculadas y coordenadas GPS."
    },
    {
        "id": "12",
        "file": "12_Admin_Modal_Mapa_Fichaje.png",
        "title": "Ubicación GPS con Mapa Interactivo Leaflet",
        "badge": "GEOLOCALIZACIÓN GPS",
        "badge_color": C_GREEN,
        "objetivo": "Inspeccionar visualmente sobre un mapa cartográfico interactivo la ubicación exacta donde el trabajador se encontraba al registrar su entrada.",
        "acceso": "Pulsar el botón 'Ver Mapa de Fichaje' en cualquiera de las tarjetas de fichaje supervisadas.",
        "botones": [
            "<b>Visor de Mapa Leaflet:</b> Permite desplazarse por el mapa, acercar o alejar el zoom y explorar el callejero oficial de OpenStreetMap.",
            "<b>Chincheta / Marcador GPS:</b> Señaliza las coordenadas capturadas por el dispositivo y abre un globo informativo con el nombre del empleado y la hora de inicio.",
            "<b>Botón 'Cerrar' (Cabecera):</b> Cierra el visor de mapa y devuelve al administrador a la auditoría de fichajes."
        ],
        "comportamiento": "Renderiza en alta definición las teselas cartográficas en tiempo real basándose en la latitud y longitud certificadas por el navegador del empleado en el instante de fichar."
    },

    # -------------------------------------------------------------
    # BLOQUE 3: PORTAL DEL EMPLEADO (TEMA AZUL)
    # -------------------------------------------------------------
    {
        "id": "13",
        "file": "13_Panel_Empleado_General.png",
        "title": "Portal del Empleado: Menú Principal",
        "badge": "PORTAL EMPLEADO (AZUL)",
        "badge_color": C_BLUE,
        "objetivo": "Entorno simplificado y enfocado bajo identidad visual corporativa azul para que el trabajador gestione sus registros diarios y consulte sus horas de forma rápida y sencilla.",
        "acceso": "Iniciar sesión con una cuenta de empleado estándar (ej. usuario 'sergio' o 'lucia').",
        "botones": [
            "<b>Tarjeta 'Registrar Fichaje':</b> Conduce al área de inicio de turnos, gestión de actividades simultáneas en paralelo y finalización de jornada.",
            "<b>Tarjeta 'Consulta de Fichajes':</b> Conduce al historial personal del empleado para verificar las horas imputadas en cada proyecto.",
            "<b>Icono 'Cerrar Sesión' (Barra Superior):</b> Ubicado a la derecha para desconectarse de la aplicación de manera segura."
        ],
        "comportamiento": "Presenta un saludo personalizado al empleado ('Bienvenido, Sergio Martin') y dos accesos destacados en tarjetas azules para la operativa habitual."
    },
    {
        "id": "14",
        "file": "14_Empleado_Registrar_Fichaje_Inicial.png",
        "title": "Registrar Fichaje: Tarjeta Nueva Jornada",
        "badge": "REGISTRO DE ENTRADA",
        "badge_color": C_BLUE,
        "objetivo": "Iniciar el registro de un turno o actividad laboral seleccionando el proyecto deseado y capturando la hora y ubicación del trabajador.",
        "acceso": "Desde el menú principal del empleado, presionar sobre la tarjeta 'Registrar Fichaje'.",
        "botones": [
            "<b>Desplegable 'Seleccionar Trabajo':</b> Permite escoger a qué proyecto o tarea se van a imputar las horas del turno que se inicia.",
            "<b>Botón Azul 'Fichar Entrada':</b> Registra la entrada en el sistema, captura la posición GPS y genera inmediatamente la tarjeta de turno activo debajo."
        ],
        "comportamiento": "La tarjeta superior 'Nueva Jornada / Tarea' permanece siempre activa y visible en la parte superior. Nunca se bloquea para que el empleado pueda iniciar tareas adicionales si desempeña varias funciones en su jornada."
    },
    {
        "id": "15",
        "file": "15_Empleado_Fichaje_Activo_Unico.png",
        "title": "Fichaje en Curso Detectado",
        "badge": "TURNO EN CURSO",
        "badge_color": C_BLUE,
        "objetivo": "Ofrecer confirmación visual al trabajador del turno que mantiene abierto, mostrando los detalles de la tarea y el control para finalizarlo cuando concluya.",
        "acceso": "Pulsar el botón 'Fichar Entrada' tras seleccionar una actividad en la tarjeta superior.",
        "botones": [
            "<b>Tarjeta 'Fichaje en Curso':</b> Muestra el subtítulo azul, la insignia amarilla 'En Curso', el nombre de la tarea y la hora exacta de inicio.",
            "<b>Botón Rojo 'Finalizar Fichaje':</b> Permite concluir la jornada o actividad de ese turno específico en el momento que el empleado termine la tarea."
        ],
        "comportamiento": "Aparece de forma inmediata (0 ms) justo debajo de la tarjeta superior de inicio, homologando exactamente sus dimensiones, bordes redondeados y estilo visual para ofrecer máxima coherencia estética."
    },
    {
        "id": "16",
        "file": "16_Empleado_Fichajes_Activos_Paralelo.png",
        "title": "Multitarea: Turnos Simultáneos en Paralelo",
        "badge": "FICHAJES EN PARALELO",
        "badge_color": C_BLUE,
        "objetivo": "Permitir al empleado registrar y mantener abiertos dos o más turnos de trabajo de forma simultánea en paralelo, ideal para jornadas donde se compaginan múltiples proyectos a la vez.",
        "acceso": "Con un turno ya abierto, seleccionar otra tarea diferente en la tarjeta superior y pulsar nuevamente 'Fichar Entrada'.",
        "botones": [
            "<b>Contador de Turnos Activos:</b> En la cabecera se indica dinámicamente el número de tareas abiertas (ej. '2 activos').",
            "<b>Tarjetas Independientes:</b> Cada turno en curso cuenta con su propio recuadro, sus datos específicos y su propio botón rojo 'Finalizar Fichaje' individual."
        ],
        "comportamiento": "El sistema computa de forma paralela e independiente el tiempo de cada actividad. El empleado puede cerrar una de las tareas en cualquier momento sin afectar en absoluto a las demás."
    },
    {
        "id": "17",
        "file": "17_Empleado_Fichaje_Finalizado_Toast.png",
        "title": "Finalización de Turno y Notificación",
        "badge": "CIERRE DE ACTIVIDAD",
        "badge_color": C_GREEN,
        "objetivo": "Cerrar un turno de trabajo activo, registrar la hora de salida, calcular el total de horas empleadas y certificar la operación ante el usuario.",
        "acceso": "Hacer clic o pulsar sobre el botón rojo 'Finalizar Fichaje' en la tarjeta de la tarea que se desea concluir.",
        "botones": [
            "<b>Notificación Toast Verde:</b> Aparece en la parte inferior informando 'El fichaje ha finalizado para: [Nombre de la Tarea]'.",
            "<b>Eliminación Instantánea del Recuadro:</b> La tarjeta del turno cerrado se borra de la vista en 0 milisegundos."
        ],
        "comportamiento": "Al finalizar, el registro se consolida en el historial personal con la fecha y hora de salida y el cómputo de horas trabajadas. Si el empleado tenía otros turnos abiertos en paralelo, estos permanecen activos sin alteración."
    },
    {
        "id": "18",
        "file": "18_Empleado_Consulta_Fichajes.png",
        "title": "Consulta de Historial de Fichajes",
        "badge": "HISTORIAL PERSONAL",
        "badge_color": C_BLUE,
        "objetivo": "Permitir al trabajador revisar todas sus jornadas anteriores, verificar las horas computadas y filtrar por rangos de fechas específicos.",
        "acceso": "Desde el portal principal del empleado, hacer clic sobre la tarjeta 'Consulta de Fichajes'.",
        "botones": [
            "<b>Filtros de Fecha ('Fecha Inicio' y 'Fecha Fin'):</b> Permiten acotar la búsqueda temporal. Incorporan iconos de calendario adaptativos que se muestran en blanco sobre fondos oscuros y en negro sobre fondos claros.",
            "<b>Tarjetas de Historial:</b> Detallan el nombre del proyecto, fecha/hora de entrada, salida y total de horas calculadas de forma automática."
        ],
        "comportamiento": "Presenta el histórico ordenado cronológicamente con indicadores de estado ('Completado' o 'Abierto') para facilitar el autocontrol horario del empleado."
    },
    {
        "id": "19",
        "file": "19_Cerrar_Sesion_Retorno_Login.png",
        "title": "Cierre Seguro de Sesión y Desconexión",
        "badge": "DESCONEXIÓN SEGURA",
        "badge_color": C_NAVY,
        "objetivo": "Cerrar la sesión de trabajo destruyendo de forma segura los datos de acceso temporal para proteger la privacidad en dispositivos compartidos de la empresa.",
        "acceso": "Presionar el botón con el icono de salida situado en la esquina superior derecha de cualquier barra de navegación.",
        "botones": [
            "<b>Icono 'Cerrar Sesión' (Cabecera):</b> Limpia de inmediato la memoria de sesión activa del navegador.",
            "<b>Retorno Limpio a Pantalla Inicial:</b> Devuelve al usuario a la pantalla de acceso sin credenciales retenidas."
        ],
        "comportamiento": "Garantiza que ningún usuario posterior pueda acceder a la cuenta anterior sin volver a introducir la clave correspondiente, preservando la confidencialidad de los datos."
    }
]


# ======================================================================================
# CONSTRUCTOR PRINCIPAL DEL MANUAL EN PDF
# ======================================================================================
def generar_guia_usuario_pdf(dest_path):
    print(f"[PDF] Compilando Guía Oficial para Usuarios en: {dest_path}")
    doc = SimpleDocTemplate(
        dest_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()

    # Estilos tipográficos formales y refinados
    s_cover_title = ParagraphStyle(
        'CoverTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=26, leading=32,
        textColor=C_NAVY, alignment=1, spaceAfter=8
    )
    s_cover_sub = ParagraphStyle(
        'CoverSub', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=14, leading=20,
        textColor=C_BLUE, alignment=1, spaceAfter=18
    )
    s_cover_desc = ParagraphStyle(
        'CoverDesc', parent=styles['Normal'],
        fontName='Helvetica', fontSize=10.5, leading=16,
        textColor=C_TEXT, alignment=1, spaceAfter=22
    )
    s_toc_title = ParagraphStyle(
        'TocTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=18, leading=22,
        textColor=C_NAVY, spaceBefore=10, spaceAfter=10
    )
    s_toc_item = ParagraphStyle(
        'TocItem', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=14,
        textColor=C_BLUE
    )
    s_screen_title = ParagraphStyle(
        'ScreenTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=14.5, leading=18,
        textColor=C_NAVY
    )
    s_badge = ParagraphStyle(
        'Badge', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8, leading=10,
        textColor=colors.white, alignment=1
    )
    s_obj = ParagraphStyle(
        'Obj', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=12.5,
        textColor=C_TEXT
    )
    s_sec_h = ParagraphStyle(
        'SecH', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8.5, leading=11.5,
        textColor=C_NAVY, spaceBefore=3.5, spaceAfter=1.5
    )
    s_btn = ParagraphStyle(
        'Btn', parent=styles['Normal'],
        fontName='Helvetica', fontSize=7.8, leading=11,
        textColor=C_TEXT
    )
    s_back_link = ParagraphStyle(
        'BackLink', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=7.5, leading=9,
        textColor=C_BLUE, alignment=2
    )

    story = []

    # -------------------------------------------------------------
    # 1. PORTADA FORMAL DEL DOCUMENTO
    # -------------------------------------------------------------
    story.append(Spacer(1, 35))
    story.append(Paragraph("GUÍA PARA USUARIOS", s_cover_title))
    story.append(Paragraph("Control Horario PWA Ionic", s_cover_sub))
    story.append(HRFlowable(width="80%", thickness=2, color=C_BLUE, spaceBefore=2, spaceAfter=20))

    story.append(Paragraph(
        "<b>DISM &mdash; Dispositivos e Infraestructuras de Sistemas Multimedia</b><br/>"
        "<b>Entrega 2: Ionic &amp; REST</b> &bull; Guía Oficial de Uso y Operación del Sistema<br/>"
        "Documento para usuarios finales de organizaciones y centros educativos que detalla el acceso unificado, "
        "la gestión integral del administrador, la operativa diaria del empleado y el registro multitarea de turnos en paralelo.",
        s_cover_desc
    ))

    # Ficha del Alumno y Asignatura
    datos_alumno = [
        [
            Paragraph("<b>Asignatura:</b>", s_sec_h),
            Paragraph("Dispositivos e Infraestructuras de Sistemas Multimedia (DISM)", s_obj)
        ],
        [
            Paragraph("<b>Práctica / Entrega:</b>", s_sec_h),
            Paragraph("Entrega 2 &mdash; Ionic &amp; REST (PWA Control Horario)", s_obj)
        ],
        [
            Paragraph("<b>Estudiante / Autor:</b>", s_sec_h),
            Paragraph("<b>Pau Cremades García</b>", s_obj)
        ],
        [
            Paragraph("<b>Titulación y Curso:</b>", s_sec_h),
            Paragraph("3.er curso &mdash; Grado en Ingeniería Multimedia", s_obj)
        ],
        [
            Paragraph("<b>Universidad:</b>", s_sec_h),
            Paragraph("Universidad de Alicante (UA)", s_obj)
        ]
    ]
    t_alumno = Table(datos_alumno, colWidths=[130, 393])
    t_alumno.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_GRAY_BG),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER),
    ]))
    story.append(t_alumno)

    story.append(Spacer(1, 15))

    # Resumen de Perfiles de Acceso
    resumen_data = [
        [
            Paragraph("<b>Perfil de Acceso</b>", s_sec_h),
            Paragraph("<b>Identidad Visual</b>", s_sec_h),
            Paragraph("<b>Credenciales Ejemplo</b>", s_sec_h),
            Paragraph("<b>Alcance Funcional Principal</b>", s_sec_h)
        ],
        [
            Paragraph("<b>Administrador</b>", s_obj),
            Paragraph("<font color='#16A34A'><b>Tema Verde</b></font>", s_obj),
            Paragraph("<b>admin</b> / admin123", s_obj),
            Paragraph("Mantenimiento de Personal y Catálogo de Trabajos, Auditoría horaria con filtros de fecha, visor de mapa Leaflet con chincheta GPS y borrado de turnos.", s_obj)
        ],
        [
            Paragraph("<b>Empleado</b>", s_obj),
            Paragraph("<font color='#2563EB'><b>Tema Azul</b></font>", s_obj),
            Paragraph("<b>sergio</b> / 1234", s_obj),
            Paragraph("Registro de entradas continuo, soporte de tareas simultáneas en paralelo, cierre instantáneo de turnos y consulta histórica de horas trabajadas.", s_obj)
        ]
    ]
    t_resumen = Table(resumen_data, colWidths=[90, 95, 110, 228])
    t_resumen.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_GRAY_BG),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER),
    ]))
    story.append(t_resumen)

    story.append(PageBreak())

    # -------------------------------------------------------------
    # 2. ÍNDICE DINÁMICO E INTERACTIVO (TABLA DE CONTENIDOS CON ENLACES)
    # -------------------------------------------------------------
    story.append(Paragraph("<a name='indice'/>ÍNDICE DE CONTENIDOS Y NAVEGACIÓN", s_toc_title))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_NAVY, spaceBefore=2, spaceAfter=14))
    story.append(Paragraph(
        "Haz clic sobre cualquiera de las secciones para saltar directamente a su ficha de instrucción correspondiente:",
        s_obj
    ))
    story.append(Spacer(1, 10))

    toc_rows = [
        [
            Paragraph("<b>Sección / Bloque</b>", s_sec_h),
            Paragraph("<b>Pantalla y Funcionalidad</b>", s_sec_h),
            Paragraph("<b>Enlace Rápido</b>", s_sec_h)
        ]
    ]

    for item in SCREENS_DATA:
        sec_label = "Bloque 1: Acceso" if int(item['id']) <= 3 else ("Bloque 2: Administrador" if int(item['id']) <= 12 else "Bloque 3: Empleado")
        link_html = f'<a href="#pantalla_{item["id"]}" color="#2563EB"><u>Ir a Pantalla {item["id"]} &rarr;</u></a>'
        desc_html = f'<b>{item["id"]}. {item["title"]}</b> ({item["badge"]})'
        toc_rows.append([
            Paragraph(f"<font color='#64748B'>{sec_label}</font>", s_obj),
            Paragraph(desc_html, s_obj),
            Paragraph(link_html, s_toc_item)
        ])

    t_toc = Table(toc_rows, colWidths=[120, 303, 100])
    t_toc.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_GRAY_BG),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # 3. PANTALLAS INDIVIDUALES (1 PANTALLA COMPLETA POR PÁGINA)
    # -------------------------------------------------------------
    IMG_W = 212
    IMG_H = 406
    TXT_W = 301

    for item in SCREENS_DATA:
        # Ancla interna para el enlace interactivo desde el índice
        anchor_html = f'<a name="pantalla_{item["id"]}"/>'

        # Cabecera con título formal y badge de rol
        header_table_data = [
            [
                Paragraph(f"{anchor_html}<b>{item['id']}. {item['title']}</b>", s_screen_title),
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

        # Contenedor de la imagen
        img_file = os.path.join(IMG_DIR, item["file"])
        if os.path.isfile(img_file):
            img_obj = Image(img_file, width=IMG_W, height=IMG_H)
        else:
            img_obj = Paragraph(f"<font color='red'>[Imagen no encontrada: {item['file']}]</font>", s_obj)

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

        # Columna de texto explicativo estructurado (orientado al usuario)
        r_flow = []

        # Objetivo del Módulo
        r_flow.append(Paragraph("<b>Objetivo del Módulo:</b>", s_sec_h))
        r_flow.append(Paragraph(item["objetivo"], s_obj))
        r_flow.append(Spacer(1, 3))

        # Ruta de Acceso
        r_flow.append(Paragraph("<b>Ruta y Modo de Acceso:</b>", s_sec_h))
        r_flow.append(Paragraph(item["acceso"], s_obj))
        r_flow.append(Spacer(1, 3))

        # Operaciones y Botones Disponibles
        r_flow.append(Paragraph("<b>Operaciones y Botones Disponibles:</b>", s_sec_h))
        for b in item["botones"]:
            r_flow.append(Paragraph(f"&bull; {b}", s_btn))
            r_flow.append(Spacer(1, 1.5))
        r_flow.append(Spacer(1, 2.5))

        # Respuesta y Comportamiento del Sistema
        r_flow.append(Paragraph("<b>Respuesta y Comportamiento del Sistema:</b>", s_sec_h))
        r_flow.append(Paragraph(item["comportamiento"], s_obj))
        r_flow.append(Spacer(1, 6))

        # Enlace de retorno al índice
        r_flow.append(Paragraph('<a href="#indice" color="#2563EB"><u>&larr; Volver al Índice de Contenidos</u></a>', s_back_link))

        t_right = Table([[r_flow]], colWidths=[TXT_W - 12])
        t_right.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), C_GRAY_BG),
            ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 9),
            ('RIGHTPADDING', (0, 0), (-1, -1), 9),
        ]))

        # Tabla combinada de dos columnas
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

    # Construir PDF oficial
    doc.build(story, canvasmaker=UserGuideNumberedCanvas)
    print(f"[OK] Documento PDF compilado con éxito en: {dest_path}")


if __name__ == "__main__":
    # 1. En Desktop / Capturas_Responsive_470x900 / Presentacion_Capturas_PWA.pdf
    pdf_capturas = os.path.join(DESKTOP_CAPT_DIR, "Presentacion_Capturas_PWA.pdf")
    generar_guia_usuario_pdf(pdf_capturas)

    # 2. En Desktop / Manual_Usuario_PWA_Control_Horario.pdf
    pdf_manual = os.path.join(DESKTOP_DIR, "Manual_Usuario_PWA_Control_Horario.pdf")
    generar_guia_usuario_pdf(pdf_manual)

    # 3. En repositorio local
    proj_capt_dir = os.path.join(SCRIPT_DIR, "Capturas_Responsive_470x900")
    if os.path.isdir(proj_capt_dir):
        generar_guia_usuario_pdf(os.path.join(proj_capt_dir, "Presentacion_Capturas_PWA.pdf"))

    print("\n[FINALIZADO] Todos los PDFs han sido generados y actualizados satisfactoriamente.")
