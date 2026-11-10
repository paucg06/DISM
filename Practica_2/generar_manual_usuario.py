# -*- coding: utf-8 -*-
"""
========================================================================================
MANUAL DE USUARIO · CONTROL HORARIO PWA IONIC
========================================================================================
Generador del manual en PDF (ReportLab).

Asignatura : DISM - Dispositivos e Infraestructuras de Sistemas Multimedia
Entrega    : Entrega 2: Ionic & REST
Autor      : Pau Cremades García
Institución: Universidad de Alicante (UA)

Uso:
    pip install reportlab
    python generar_manual_usuario.py            # genera y copia a las rutas habituales
    python generar_manual_usuario.py salida.pdf # genera solo en la ruta indicada

Las capturas se buscan en «Capturas_Responsive_470x900» junto al script. Si falta alguna,
se dibuja un marcador en su lugar y el PDF se genera igualmente.
========================================================================================
"""

import os
import re
import sys
import shutil
import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    PageBreak, NextPageTemplate, KeepTogether, CondPageBreak, Flowable, HRFlowable
)
from reportlab.platypus.tableofcontents import TableOfContents

# ----------------------------------------------------------------------------------------
# RUTAS
# ----------------------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(SCRIPT_DIR, "Capturas_Responsive_470x900")
if not os.path.isdir(IMG_DIR):
    IMG_DIR = r"C:\Users\paucr\Desktop\Practica_Compilada\Capturas_Responsive_470x900"

DESKTOP_DIR = r"C:\Users\paucr\Desktop\Practica_Compilada"
DESKTOP_CAPT_DIR = os.path.join(DESKTOP_DIR, "Capturas_Responsive_470x900")

# ----------------------------------------------------------------------------------------
# METADATOS DEL DOCUMENTO
# ----------------------------------------------------------------------------------------
APP_NAME = "Control Horario"
DOC_TITLE = "Manual de Usuario"
AUTHOR = "Pau Cremades García"
SUBJECT = "DISM — Dispositivos e Infraestructuras de Sistemas Multimedia"
UNIVERSITY = "Universidad de Alicante (UA)"
CURSO = "2026-2027"
VERSION = "1.0"
FECHA = "10/11/2026"

PAGE_W, PAGE_H = A4
MX = 40                      # margen horizontal
CW = PAGE_W - 2 * MX         # ancho útil (515 pt)

# ----------------------------------------------------------------------------------------
# PALETA
# ----------------------------------------------------------------------------------------
C_NAVY = colors.HexColor("#0F172A")
C_BLUE = colors.HexColor("#2563EB")
C_GREEN = colors.HexColor("#16A34A")
C_GRAY_BG = colors.HexColor("#F8FAFC")
C_BORDER = colors.HexColor("#CBD5E1")
C_TEXT = colors.HexColor("#1E293B")
C_MUTED = colors.HexColor("#64748B")
C_DANGER = colors.HexColor("#DC2626")
C_AMBER = colors.HexColor("#D97706")
C_BLUE_BG = colors.HexColor("#EFF6FF")
C_GREEN_BG = colors.HexColor("#F0FDF4")
C_AMBER_BG = colors.HexColor("#FFFBEB")
C_SLATE = colors.HexColor("#334155")


def hx(c):
    """Color de ReportLab -> '#rrggbb' (para etiquetas <font> y <a>)."""
    return "#%02x%02x%02x" % tuple(int(round(v * 255)) for v in (c.red, c.green, c.blue))


# ========================================================================================
# ELEMENTOS GRÁFICOS PERSONALIZADOS
# ========================================================================================
PH_SIDE, PH_TOP, PH_BOT = 7, 17, 11


def phone_height(w):
    return (w - 2 * PH_SIDE) * 900.0 / 470.0 + PH_TOP + PH_BOT


def draw_phone(c, x, y, w, img_path=None, label=""):
    """Dibuja un marco de smartphone con la captura recortada a su pantalla."""
    h = phone_height(w)
    c.saveState()
    c.setFillColor(C_BORDER)
    c.setFillAlpha(0.55)
    c.roundRect(x + 2.5, y - 3, w, h, 16, fill=1, stroke=0)
    c.setFillAlpha(1)
    c.setFillColor(C_NAVY)
    c.setStrokeColor(C_SLATE)
    c.setLineWidth(0.8)
    c.roundRect(x, y, w, h, 16, fill=1, stroke=1)
    c.setFillColor(C_SLATE)
    c.roundRect(x + w / 2 - 14, y + h - 11, 28, 3.6, 1.8, fill=1, stroke=0)
    sx, sy, sw, sh = x + PH_SIDE, y + PH_BOT, w - 2 * PH_SIDE, h - PH_TOP - PH_BOT
    c.saveState()
    p = c.beginPath()
    p.roundRect(sx, sy, sw, sh, 8)
    c.clipPath(p, stroke=0, fill=0)
    if img_path and os.path.isfile(img_path):
        c.drawImage(ImageReader(img_path), sx, sy, sw, sh, mask="auto")
    else:
        c.setFillColor(C_GRAY_BG)
        c.rect(sx, sy, sw, sh, fill=1, stroke=0)
        c.setFillColor(C_MUTED)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(sx + sw / 2, sy + sh / 2 + 4, "Captura no disponible")
        c.setFont("Helvetica", 6.5)
        c.drawCentredString(sx + sw / 2, sy + sh / 2 - 8, label)
    c.restoreState()
    c.restoreState()


class PhoneFrame(Flowable):
    def __init__(self, img_path, width=160, label=""):
        super().__init__()
        self.img_path, self.w, self.label = img_path, width, label
        self.h = phone_height(width)

    def wrap(self, aw, ah):
        return self.w + 5, self.h + 5

    def draw(self):
        draw_phone(self.canv, 1, 4, self.w, self.img_path, self.label)


class NumBadge(Flowable):
    """Círculo de color con un número (pasos numerados)."""
    def __init__(self, n, color, size=14):
        super().__init__()
        self.n, self.color, self.size = n, color, size

    def wrap(self, aw, ah):
        return self.size, self.size

    def draw(self):
        c, s = self.canv, self.size
        c.setFillColor(self.color)
        c.circle(s / 2, s / 2, s / 2, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawCentredString(s / 2, s / 2 - 2.6, str(self.n))


class TocMarker(Flowable):
    """Marcador invisible: registra entrada de índice, marcador PDF y sección de cabecera."""
    def __init__(self, level, text, key, section=None, toc=True):
        super().__init__()
        self.level, self.text, self.key, self.section, self.toc = level, text, key, section, toc

    def wrap(self, aw, ah):
        return 0, 0

    def draw(self):
        pass


class NavMap(Flowable):
    """Diagrama de navegación de la aplicación."""
    def __init__(self, width=CW, height=250):
        super().__init__()
        self.width, self.height = width, height

    def wrap(self, aw, ah):
        return self.width, self.height

    def draw(self):
        c = self.canv

        def box(x, y, w, h, fill, text, txt=colors.white, stroke=None, size=8):
            c.setFillColor(fill)
            c.setStrokeColor(stroke or fill)
            c.setLineWidth(1)
            c.roundRect(x, y, w, h, 6, fill=1, stroke=1)
            c.setFillColor(txt)
            c.setFont("Helvetica-Bold", size)
            lines = text.split("\n")
            ty = y + h / 2 + (len(lines) - 1) * 4.5 - 2.8
            for ln in lines:
                c.drawCentredString(x + w / 2, ty, ln)
                ty -= 9.5

        def line(x1, y1, x2, y2):
            c.setStrokeColor(C_MUTED)
            c.setLineWidth(1.1)
            c.line(x1, y1, x2, y2)

        # conectores
        line(283, 205, 283, 188)
        line(149, 188, 417, 188)
        line(149, 188, 149, 169)
        line(417, 188, 417, 169)
        line(149, 135, 149, 118)
        line(48, 118, 250, 118)
        for kx in (48, 149, 250):
            line(kx, 118, kx, 100)
        line(417, 135, 417, 118)
        line(365, 118, 466, 118)
        for kx in (365, 466):
            line(kx, 118, kx, 100)

        box(213, 205, 140, 34, C_NAVY, "Inicio de sesión")
        box(64, 135, 170, 34, C_GREEN, "Panel del Administrador")
        box(332, 135, 170, 34, C_BLUE, "Portal del Empleado")
        for kx, t in ((0, "Gestión de\nUsuarios"), (101, "Gestión de\nTrabajos"), (202, "Gestión de\nFichajes")):
            box(kx, 60, 96, 40, C_GREEN_BG, t, txt=C_NAVY, stroke=C_GREEN, size=7.5)
        for kx, t in ((317, "Registrar\nFichaje"), (418, "Consulta de\nFichajes")):
            box(kx, 60, 96, 40, C_BLUE_BG, t, txt=C_NAVY, stroke=C_BLUE, size=7.5)
        box(0, 8, self.width, 30, C_GRAY_BG,
            "Cerrar sesión  ·  disponible en la barra superior de cualquier pantalla",
            txt=C_MUTED, stroke=C_BORDER, size=7.5)


# ========================================================================================
# CANVAS (numeración «Página X de Y» y cabecera/pie) Y PLANTILLAS DE PÁGINA
# ========================================================================================
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []
        self.page_kind = "body"
        self.section_name = ""

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            if self.page_kind == "body":
                self.draw_chrome(total)
            super().showPage()
        super().save()

    def draw_chrome(self, total):
        self.saveState()
        self.setStrokeColor(C_BORDER)
        self.setLineWidth(0.6)
        self.setFillColor(C_NAVY)
        self.setFont("Helvetica-Bold", 8)
        self.drawString(MX, 806, "CONTROL HORARIO")
        self.setFillColor(C_MUTED)
        self.setFont("Helvetica", 8)
        self.drawRightString(PAGE_W - MX, 806, self.section_name)
        self.line(MX, 798, PAGE_W - MX, 798)
        self.setFillColor(C_BLUE)
        self.rect(MX, 797.2, 36, 1.8, fill=1, stroke=0)
        self.line(MX, 42, PAGE_W - MX, 42)
        self.setFillColor(C_MUTED)
        self.setFont("Helvetica", 8)
        self.drawString(MX, 29, f"{DOC_TITLE}  ·  Práctica 2 DISM")
        self.setFillColor(C_NAVY)
        self.setFont("Helvetica-Bold", 8)
        self.drawRightString(PAGE_W - MX, 29, f"Página {self._pageNumber} de {total}")
        self.restoreState()


def on_body(c, doc):
    c.page_kind = "body"


def _chip(c, x, y, text, fill, h=22):
    font_name = "Helvetica-Bold"
    font_size = 8
    tw = stringWidth(text, font_name, font_size)
    w = tw + 28
    c.setFillColor(fill)
    c.roundRect(x, y, w, h, h / 2.0, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont(font_name, font_size)
    ty = y + (h / 2.0) - 2.8
    c.drawCentredString(x + w / 2.0, ty, text)
    return w


def on_cover(c, doc):
    c.page_kind = "cover"
    W, H = A4
    c.saveState()
    c.setFillColor(C_NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#172554"))
    p = c.beginPath(); p.moveTo(W * 0.38, H); p.lineTo(W, H); p.lineTo(W, H * 0.28); p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#1E3A8A"))
    p = c.beginPath(); p.moveTo(W * 0.66, H); p.lineTo(W, H); p.lineTo(W, H * 0.64); p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setFillColor(C_BLUE); c.setFillAlpha(0.10)
    c.circle(W - 40, 120, 170, fill=1, stroke=0)
    c.setFillAlpha(1)
    c.setFillColor(C_BLUE); c.rect(0, H - 8, W / 2, 8, fill=1, stroke=0)
    c.setFillColor(C_GREEN); c.rect(W / 2, H - 8, W / 2, 8, fill=1, stroke=0)

    t = c.beginText(48, H - 62)
    t.setFont("Helvetica-Bold", 8.5); t.setFillColor(colors.HexColor("#93C5FD")); t.setCharSpace(2)
    t.textOut("DISM  ·  ENTREGA 2  ·  IONIC & REST")
    c.drawText(t)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 48)
    c.drawString(48, 600, "Manual de")
    c.drawString(48, 546, "Usuario")
    c.setFillColor(colors.HexColor("#93C5FD"))
    c.setFont("Helvetica-Bold", 21)
    c.drawString(48, 503, APP_NAME)
    c.setFillColor(C_GREEN); c.rect(48, 484, 56, 4, fill=1, stroke=0)

    desc = Paragraph(
        "Guía oficial de uso y operación de la aplicación de registro de jornada laboral. "
        "Incluye el acceso unificado, la gestión integral del administrador y la operativa "
        "diaria del empleado, con capturas y explicación de cada pantalla.",
        ParagraphStyle("cd", fontName="Helvetica", fontSize=10.5, leading=16,
                       textColor=colors.HexColor("#CBD5E1")))
    _, dh = desc.wrapOn(c, 285, 200)
    desc.drawOn(c, 48, 466 - dh)
    w1 = _chip(c, 48, 372, "PERFIL ADMINISTRADOR", C_GREEN)
    _chip(c, 48 + w1 + 12, 372, "PERFIL EMPLEADO", C_BLUE)

    c.saveState()
    c.translate(447, 440)
    c.rotate(-5)
    draw_phone(c, -84, -162, 168, os.path.join(IMG_DIR, "01_Login_Inicio.png"), "01_Login_Inicio.png")
    c.restoreState()

    c.setStrokeColor(C_SLATE); c.setLineWidth(0.8); c.line(48, 160, W - 48, 160)

    def info(x, y, label, value):
        tt = c.beginText(x, y)
        tt.setFont("Helvetica-Bold", 7); tt.setFillColor(colors.HexColor("#93C5FD")); tt.setCharSpace(1.6)
        tt.textOut(label)
        c.drawText(tt)
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 10)
        c.drawString(x, y - 16, value)

    info(48, 136, "AUTOR", AUTHOR)
    info(230, 136, "ASIGNATURA", "DISM")
    info(392, 136, "UNIVERSIDAD", "Universidad de Alicante")
    info(48, 86, "VERSIÓN", VERSION)
    info(230, 86, "FECHA", FECHA)
    info(392, 86, "CURSO", CURSO)
    c.restoreState()


def make_divider(part):
    def _cb(c, doc):
        c.page_kind = "divider"
        W, H = A4
        c.saveState()
        c.setFillColor(colors.HexColor(part["bg"]))
        c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setFillColor(colors.white); c.setFillAlpha(0.07)
        c.setFont("Helvetica-Bold", 330)
        c.drawRightString(W - 24, H - 340, part["num"])
        c.setFillAlpha(1)
        c.setFillColor(colors.HexColor(part["accent"])); c.rect(0, 0, 10, H, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#CBD5E1")); c.setFont("Helvetica", 8)
        c.drawString(56, 36, f"{DOC_TITLE}  ·  {APP_NAME}")
        c.restoreState()
    return _cb


class ManualDoc(BaseDocTemplate):
    def __init__(self, filename):
        super().__init__(filename, pagesize=A4, leftMargin=MX, rightMargin=MX,
                         topMargin=62, bottomMargin=56,
                         title=f"{DOC_TITLE} · {APP_NAME}", author=AUTHOR,
                         subject=SUBJECT, creator="generar_manual_usuario.py",
                         keywords="PWA, Ionic, Control Horario, Manual de Usuario")
        body = Frame(MX, 56, CW, 724, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="body")
        cover = Frame(MX, 40, CW, 40, id="cover")
        tpls = [PageTemplate(id="Cover", frames=[cover], onPage=on_cover),
                PageTemplate(id="Body", frames=[body], onPage=on_body)]
        for p in PARTS:
            fr = Frame(56, 90, 460, 390, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="div" + p["num"])
            tpls.append(PageTemplate(id="Div" + p["num"], frames=[fr], onPage=make_divider(p)))
        self.addPageTemplates(tpls)

    def afterFlowable(self, fl):
        if isinstance(fl, TocMarker):
            self.canv.bookmarkPage(fl.key)
            if fl.section:
                self.canv.section_name = fl.section
            if fl.level is not None:
                if fl.toc:
                    self.notify("TOCEntry", (fl.level, fl.text, self.page, fl.key))
                self.canv.addOutlineEntry(fl.text, fl.key, fl.level, 0)


# ========================================================================================
# PARTES DEL MANUAL
# ========================================================================================
PARTS = [
    {"num": "1", "name": "Acceso y Seguridad", "ids": (1, 3), "bg": "#0F172A", "accent": "#60A5FA",
     "desc": "Cómo identificarse en la aplicación, qué ocurre cuando las credenciales no son correctas "
             "y cómo se accede de forma segura al entorno de cada perfil."},
    {"num": "2", "name": "Panel del Administrador", "ids": (4, 12), "bg": "#14532D", "accent": "#86EFAC",
     "desc": "Herramientas para gestionar el personal, el catálogo de proyectos y la auditoría de fichajes, "
             "incluida la geolocalización de cada jornada."},
    {"num": "3", "name": "Portal del Empleado", "ids": (13, 19), "bg": "#1E3A8A", "accent": "#93C5FD",
     "desc": "Operativa diaria del trabajador: registrar entradas, trabajar en varias tareas en paralelo, "
             "finalizar turnos, consultar el historial y cerrar sesión."},
]


def part_for(sid):
    n = int(sid)
    for p in PARTS:
        if p["ids"][0] <= n <= p["ids"][1]:
            return p
    return PARTS[0]


# ========================================================================================
# DATOS DE CADA PANTALLA (contenido original, sin cambios)
# ========================================================================================
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
            "<b>Nombre de usuario:</b> Espacio para introducir el identificador de cuenta asignado.",
            "<b>Contraseña:</b> Clave privada de seguridad protegida por caracteres enmascarados.",
            "<b>Acceder al sistema:</b> Valida las credenciales y da acceso al entorno de trabajo."
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
            "<b>Aviso de error:</b> Notificación emergente roja indicando credenciales incorrectas.",
            "<b>Contraseña:</b> Permite reescribir la clave sin recargar la página."
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
            "<b>Aviso de bienvenida:</b> Notificación emergente verde con saludo personalizado.",
            "<b>Redirección:</b> Conduce automáticamente al panel correspondiente según el rol."
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
            "<b>Gestión de usuarios:</b> Conduce a la administración y mantenimiento de la plantilla.",
            "<b>Gestión de trabajos:</b> Da acceso al catálogo de tareas y proyectos de la empresa.",
            "<b>Gestión de fichajes:</b> Conduce a la auditoría horaria, mapa Leaflet y borrado de turnos.",
            "<b>Cerrar sesión:</b> Desconecta la cuenta activa y limpia el almacenamiento de sesión."
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
            "<b>Lista de usuarios:</b> Al pulsar sobre cualquier empleado se abre su modal de edición.",
            "<b>Eliminar usuario:</b> Abre el diálogo de confirmación para dar de baja al trabajador.",
            "<b>Añadir nuevo usuario:</b> Abre el formulario modal para registrar un nuevo integrante."
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
            "<b>ID Usuario:</b> Identificador numérico protegido para preservar el historial previo.",
            "<b>Nombre, usuario y clave:</b> Permiten actualizar la información personal y restablecer la contraseña.",
            "<b>Rol:</b> Permite conmutar los permisos del usuario entre Administrador o Empleado.",
            "<b>Actualizar usuario:</b> Guarda inmediatamente todos los cambios en la base de datos.",
            "<b>Cerrar:</b> Descarta cualquier modificación y regresa a la vista de lista."
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
            "<b>ID Usuario:</b> Código numérico obligatorio que representará al nuevo empleado.",
            "<b>Nombre completo:</b> Nombre y apellidos del trabajador para consultas y reportes.",
            "<b>Nombre de usuario:</b> Identificador que empleará para acceder a la aplicación.",
            "<b>Contraseña:</b> Clave de seguridad establecida para la cuenta.",
            "<b>Rol:</b> Asigna si el usuario operará como Administrador o como Empleado.",
            "<b>Crear usuario:</b> Valida los campos y persiste el nuevo registro en el sistema.",
            "<b>Cerrar:</b> Cancela el registro y cierra la ventana modal."
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
            "<b>Lista de proyectos:</b> Al pulsar sobre cualquier trabajo se abre su modal de edición.",
            "<b>Eliminar trabajo:</b> Permite suprimir una tarea que ya no esté en curso previa confirmación.",
            "<b>Crear nuevo trabajo:</b> Abre el formulario modal para dar de alta una nueva actividad."
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
            "<b>ID Trabajo:</b> Identificador numérico asociado a la tarea o proyecto.",
            "<b>Nombre del trabajo:</b> Denominación descriptiva de la actividad laboral.",
            "<b>Guardar trabajo:</b> Actualiza el nombre del proyecto en todo el sistema corporativo.",
            "<b>Cerrar:</b> Cierra el formulario modal sin aplicar modificaciones."
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
            "<b>ID Trabajo:</b> Código numérico asignado a la nueva actividad empresarial.",
            "<b>Nombre del trabajo:</b> Título descriptivo de la tarea o proyecto a incorporar.",
            "<b>Guardar trabajo:</b> Registra la tarea y la habilita de inmediato para los empleados.",
            "<b>Cerrar:</b> Descarta el formulario y regresa al catálogo general."
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
            "<b>Filtrar por empleado:</b> Permite consultar los turnos de un trabajador o de toda la plantilla.",
            "<b>Fecha inicio y fin:</b> Selectores de fecha con icono de calendario adaptativo claro y oscuro.",
            "<b>Aplicar filtros:</b> Refresca la auditoría de turnos según los criterios seleccionados.",
            "<b>Ver mapa de fichaje:</b> Abre la ventana modal interactiva con el visor Leaflet y chincheta GPS.",
            "<b>Eliminar fichaje:</b> Permite al administrador borrar registros erróneos previa confirmación."
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
            "<b>Mapa Leaflet:</b> Permite zoom y desplazamiento sobre la cartografía oficial OpenStreetMap.",
            "<b>Marcador GPS:</b> Señaliza la posición exacta y muestra los datos del turno en un globo emergente.",
            "<b>Cerrar:</b> Cierra el visor de mapa y devuelve a la tabla de fichajes."
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
            "<b>Registrar fichaje:</b> Conduce al área de inicio de turnos y gestión de tareas en paralelo.",
            "<b>Consulta de fichajes:</b> Da acceso al historial individual de horas y jornadas del trabajador.",
            "<b>Cerrar sesión:</b> Cierra la sesión activa y retorna a la pantalla de login de forma segura."
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
            "<b>Seleccionar trabajo:</b> Permite escoger el proyecto al que se imputarán las horas del turno.",
            "<b>Fichar entrada:</b> Registra la hora, captura el GPS y genera la tarjeta activa debajo."
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
            "<b>Fichaje en curso:</b> Muestra el estado activo, el proyecto asignado y la hora de inicio.",
            "<b>Finalizar fichaje:</b> Concluye la actividad del turno específico y registra la hora de salida."
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
            "<b>Contador de activos:</b> Indica dinámicamente el número total de turnos abiertos en paralelo.",
            "<b>Turnos independientes:</b> Cada tarea dispone de sus propios datos y su propio botón de finalización."
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
            "<b>Aviso de finalización:</b> Notificación emergente verde confirmando el cierre de la jornada.",
            "<b>Cierre de recuadro:</b> El turno finalizado se retira de la vista de forma inmediata."
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
            "<b>Filtros de fecha:</b> Acotan la búsqueda cronológica mediante selector adaptativo claro y oscuro.",
            "<b>Historial de jornadas:</b> Muestra entrada, salida, proyecto y total de horas calculadas."
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
            "<b>Cerrar sesión:</b> Limpia de inmediato la memoria de sesión activa del navegador.",
            "<b>Retorno al login:</b> Devuelve a la pantalla de acceso limpia sin credenciales retenidas."
        ],
        "comportamiento": "Garantiza que ningún usuario posterior pueda acceder a la cuenta anterior sin volver a introducir la clave correspondiente, preservando la confidencialidad de los datos."
    }
]


# ========================================================================================
# CONTENIDO AMPLIADO POR PANTALLA: PASO A PASO + RECUADRO DESTACADO
#   tipos de recuadro:  tip = Consejo · warn = Atención · note = Nota
# ========================================================================================
EXTRAS = {
    "01": (["Abra la aplicación desde el navegador o desde el icono de la PWA instalada.",
            "Escriba su nombre de usuario y su contraseña.",
            "Pulse «Acceder al Sistema» y espere unos instantes a la validación."],
           ("tip", "Si instala la PWA en la pantalla de inicio, accederá a la aplicación en un solo toque, igual que con una app nativa.")),
    "02": (["Fíjese en el mensaje rojo que aparece en la parte inferior.",
            "Revise mayúsculas, minúsculas y el idioma del teclado.",
            "Corrija la contraseña y vuelva a pulsar «Acceder al Sistema»."],
           ("warn", "Si el error persiste, no siga probando contraseñas: pida al administrador que restablezca su clave desde la gestión de usuarios.")),
    "03": (["Introduzca credenciales válidas.",
            "Espere al aviso verde de bienvenida.",
            "La aplicación le llevará automáticamente a su panel."],
           ("note", "El color del panel indica con qué perfil ha entrado: verde para administración y azul para empleado.")),
    "04": (["Inicie sesión con una cuenta de administrador.",
            "Revise las tres tarjetas: Usuarios, Trabajos y Fichajes.",
            "Pulse la tarjeta del módulo con el que desea trabajar."],
           ("warn", "Cierre la sesión de administrador cuando no la use: concede control total sobre el personal y los registros.")),
    "05": (["Entre en «Gestión de Usuarios».",
            "Localice al trabajador; la etiqueta de color indica su rol.",
            "Pulse la fila para editar o la papelera para eliminar."],
           ("warn", "Eliminar a un trabajador tiene impacto en la organización: lea con atención la ventana de confirmación antes de aceptar.")),
    "06": (["Pulse la fila del empleado en la lista.",
            "Modifique nombre, usuario, clave o rol.",
            "Pulse «Actualizar Usuario» para guardar los cambios."],
           ("note", "El ID de usuario está bloqueado a propósito para no romper el vínculo con el historial de fichajes.")),
    "07": (["Pulse «Añadir Nuevo Usuario» al final de la lista.",
            "Rellene ID, nombre completo, usuario, contraseña y rol.",
            "Pulse «Crear Usuario»."],
           ("tip", "Elija nombres de usuario cortos y fáciles de recordar, y entregue la contraseña inicial por un canal seguro.")),
    "08": (["Entre en «Gestión de Trabajos».",
            "Consulte el catálogo con su identificador (#ID).",
            "Pulse un proyecto para editarlo o «Crear Nuevo Trabajo» para añadir otro."],
           ("tip", "Mantenga el catálogo limpio: elimine las tareas finalizadas para que los empleados no tengan que buscar entre opciones obsoletas.")),
    "09": (["Pulse el proyecto en el catálogo.",
            "Cambie el nombre en el campo correspondiente.",
            "Pulse «Guardar Trabajo»."],
           ("note", "El cambio de nombre se refleja en los selectores de fichaje de toda la plantilla.")),
    "10": (["Pulse «Crear Nuevo Trabajo».",
            "Indique el ID numérico y un nombre descriptivo.",
            "Pulse «Guardar Trabajo»."],
           ("tip", "Use nombres descriptivos y homogéneos (por ejemplo, «Soporte Técnico»): los informes de horas serán más claros.")),
    "11": (["Entre en «Gestión de Fichajes».",
            "Elija empleado y rango de fechas y pulse «Aplicar Filtros».",
            "Revise las tarjetas; abra el mapa o elimine registros erróneos."],
           ("warn", "El borrado de un fichaje es definitivo. Verifique empleado, fecha y horas antes de confirmar.")),
    "12": (["Pulse «Ver Mapa de Fichaje» en la tarjeta deseada.",
            "Mueva y amplíe el mapa; toque la chincheta para ver empleado y hora.",
            "Pulse «Cerrar» para volver a la auditoría."],
           ("note", "La ubicación es la que capturó el dispositivo del empleado al fichar; su precisión depende del GPS y de los permisos del dispositivo.")),
    "13": (["Inicie sesión con su cuenta de empleado.",
            "Lea el saludo personalizado de la parte superior.",
            "Pulse «Registrar Fichaje» o «Consulta de Fichajes»."],
           ("tip", "Desde este menú llega en un toque a las dos tareas de cada día: fichar y revisar sus horas.")),
    "14": (["Entre en «Registrar Fichaje».",
            "Despliegue «Seleccionar Trabajo» y elija el proyecto.",
            "Pulse «Fichar Entrada» y acepte el permiso de ubicación si se solicita."],
           ("warn", "Conceda el permiso de ubicación del navegador: la aplicación captura su posición GPS al fichar y el administrador puede consultarla.")),
    "15": (["Compruebe que aparece la tarjeta «Fichaje en Curso» con la insignia amarilla.",
            "Verifique que el proyecto y la hora de inicio son correctos.",
            "Cuando termine la tarea, pulse «Finalizar Fichaje»."],
           ("tip", "Antes de finalizar, confirme que el proyecto mostrado es el correcto: así sus horas se imputan donde corresponde.")),
    "16": (["Con un turno abierto, seleccione otra tarea en la tarjeta superior.",
            "Pulse de nuevo «Fichar Entrada».",
            "Gestione cada tarjeta por separado con su botón «Finalizar Fichaje»."],
           ("note", "El contador de la cabecera le indica en todo momento cuántas tareas tiene abiertas.")),
    "17": (["Pulse «Finalizar Fichaje» en la tarjeta de la tarea concluida.",
            "Espere el aviso verde de confirmación.",
            "Compruebe en su historial que el turno consta como completado."],
           ("tip", "Finalice cada turno en cuanto termine la tarea para que el cómputo de horas sea exacto.")),
    "18": (["Entre en «Consulta de Fichajes».",
            "Indique «Fecha Inicio» y «Fecha Fin» para acotar el periodo.",
            "Revise las tarjetas: proyecto, entrada, salida y total de horas."],
           ("tip", "Revise su historial al cierre de cada semana; si detecta un registro erróneo, avise al administrador, que puede eliminarlo.")),
    "19": (["Pulse el icono de salida de la esquina superior derecha.",
            "Espere a volver a la pantalla de inicio de sesión.",
            "Compruebe que los campos de acceso aparecen vacíos."],
           ("warn", "En dispositivos compartidos, cierre siempre la sesión al terminar para proteger su cuenta.")),
}

CALL = {
    "tip": ("CONSEJO", C_BLUE, C_BLUE_BG),
    "warn": ("ATENCIÓN", C_AMBER, C_AMBER_BG),
    "note": ("NOTA", C_SLATE, C_GRAY_BG),
}


# ========================================================================================
# ESTILOS
# ========================================================================================
def make_styles():
    base = getSampleStyleSheet()["Normal"]

    def ps(name, **kw):
        return ParagraphStyle(name, parent=base, **kw)

    S = {}
    S["body"] = ps("body", fontName="Helvetica", fontSize=9.5, leading=14.5, textColor=C_TEXT,
                   alignment=TA_JUSTIFY, spaceAfter=6)
    S["bullet"] = ps("bullet", fontName="Helvetica", fontSize=9.5, leading=14, textColor=C_TEXT,
                     leftIndent=14, bulletIndent=2, spaceAfter=2.5)
    S["h1"] = ps("h1", fontName="Helvetica-Bold", fontSize=23, leading=27, textColor=C_NAVY, spaceAfter=3)
    S["h1_sub"] = ps("h1sub", fontName="Helvetica", fontSize=10.5, leading=14, textColor=C_MUTED, spaceAfter=4)
    S["h2"] = ps("h2", fontName="Helvetica-Bold", fontSize=12.5, leading=16, textColor=C_NAVY,
                 spaceBefore=14, spaceAfter=5)
    S["h3"] = ps("h3", fontName="Helvetica-Bold", fontSize=7.8, leading=10, spaceBefore=7, spaceAfter=2.5)
    S["cell"] = ps("cell", fontName="Helvetica", fontSize=8.6, leading=12, textColor=C_TEXT)
    S["cell_b"] = ps("cellb", fontName="Helvetica", fontSize=8.9, leading=12.8, textColor=C_TEXT)
    S["cell_h"] = ps("cellh", fontName="Helvetica-Bold", fontSize=8, leading=10.5, textColor=colors.white)
    S["cell_c"] = ps("cellc", fontName="Helvetica", fontSize=8.6, leading=12, textColor=C_TEXT, alignment=TA_CENTER)
    S["call"] = ps("call", fontName="Helvetica", fontSize=8.8, leading=12.6, textColor=C_TEXT)
    S["call_h"] = ps("callh", fontName="Helvetica-Bold", fontSize=7.8, leading=11)
    S["num"] = ps("num", fontName="Helvetica-Bold", fontSize=22, leading=26, textColor=colors.white, alignment=TA_CENTER)
    S["screen_title"] = ps("stitle", fontName="Helvetica-Bold", fontSize=14.5, leading=18, textColor=C_NAVY)
    S["screen_sub"] = ps("ssub", fontName="Helvetica", fontSize=8, leading=11, textColor=C_MUTED)
    S["badge"] = ps("badge", fontName="Helvetica-Bold", fontSize=7.4, leading=9.5, textColor=colors.white, alignment=TA_CENTER)
    S["nav_l"] = ps("navl", fontName="Helvetica", fontSize=8, leading=10, alignment=TA_LEFT)
    S["nav_c"] = ps("navc", fontName="Helvetica-Bold", fontSize=8, leading=10, alignment=TA_CENTER)
    S["nav_r"] = ps("navr", fontName="Helvetica", fontSize=8, leading=10, alignment=TA_RIGHT)
    S["toc0"] = ps("toc0", fontName="Helvetica-Bold", fontSize=10.5, leading=14, textColor=C_NAVY,
                   leftIndent=0, spaceBefore=5)
    S["toc1"] = ps("toc1", fontName="Helvetica", fontSize=9.3, leading=12.8, textColor=C_TEXT,
                   leftIndent=20, spaceBefore=0)
    S["faq_q"] = ps("faqq", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=C_NAVY, spaceBefore=7, spaceAfter=1)
    return S


def P(text, style, **kw):
    return Paragraph(text, style, **kw)


def bullets(S, items):
    return [Paragraph(t, S["bullet"], bulletText="•") for t in items]


_EL = re.compile(r"^<b>(.*?)</b>\s*(.*)$", re.S)


def split_element(txt):
    m = _EL.match(txt)
    if not m:
        return "", txt
    name = m.group(1).rstrip(":").strip()
    desc = m.group(2).strip()
    name = re.sub(r"\s*\(.*?\)", "", name)
    name = re.sub(r"^(Campo|Botón(?:\s+\w+)?|Tarjeta|Icono|Desplegable|Selector(?:\s+\w+)?|Fila de|Notificación(?:\s+\w+)?)\s+", "", name, flags=re.I)
    name = name.replace("'", "").replace('"', '').strip()
    if name.lower().startswith("de "):
        name = name[3:].strip()
    return name, desc


def callout(S, kind, text, width=CW):
    label, col, bg = CALL[kind]
    t = Table([[P(f"<font color='{hx(col)}'>{label}</font>", S["call_h"]), P(text, S["call"])]],
              colWidths=[66, width - 66])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, 0), 3, col),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (0, 0), 10), ("LEFTPADDING", (1, 0), (1, 0), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ]))
    return t


def data_table(S, header, rows, widths, color=C_NAVY, zebra=True):
    data = [[P(h, S["cell_h"]) for h in header]]
    for r in rows:
        data.append([c if isinstance(c, Flowable) or isinstance(c, list) else P(str(c), S["cell"]) for c in r])
    t = Table(data, colWidths=widths, repeatRows=1)
    st = [("BACKGROUND", (0, 0), (-1, 0), color), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
          ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
          ("LINEBELOW", (0, 1), (-1, -1), 0.4, C_BORDER), ("BOX", (0, 0), (-1, -1), 0.6, C_BORDER)]
    if zebra:
        for i in range(2, len(data), 2):
            st.append(("BACKGROUND", (0, i), (-1, i), C_GRAY_BG))
    t.setStyle(TableStyle(st))
    return t


def section_head(S, num_text, title, subtitle, key, section):
    return [TocMarker(0, f"{num_text}{title}", key, section=section),
            P(f"{num_text}{title}", S["h1"]), P(subtitle, S["h1_sub"]),
            HRFlowable(width="100%", thickness=2, color=C_BLUE, spaceBefore=2, spaceAfter=12)]


# ========================================================================================
# FICHA DE UNA PANTALLA
# ========================================================================================
def screen_flowables(S, item, idx, total):
    sid, acc = item["id"], item["badge_color"]
    ah = hx(acc)
    part = part_for(sid)
    pasos, (ckind, ctext) = EXTRAS[sid]
    out = [TocMarker(1, f"{sid}. {item['title']}", f"scr_{sid}", section=f"Parte {part['num']}: {part['name']}")]

    head = Table([[P(sid, S["num"]),
                   [P(item["title"], S["screen_title"]),
                    P(f"Parte {part['num']}: {part['name']}", S["screen_sub"])],
                   P(item["badge"], S["badge"])]],
                 colWidths=[50, 327, 138], rowHeights=[48])
    head.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), acc), ("BACKGROUND", (2, 0), (2, 0), acc),
        ("BACKGROUND", (1, 0), (1, 0), C_GRAY_BG), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (0, 0), 0), ("RIGHTPADDING", (0, 0), (0, 0), 0),
        ("LEFTPADDING", (1, 0), (1, 0), 12), ("LEFTPADDING", (2, 0), (2, 0), 6), ("RIGHTPADDING", (2, 0), (2, 0), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("BOX", (0, 0), (-1, -1), 0.6, C_BORDER),
    ]))
    out += [head, Spacer(1, 12)]

    def h3(t):
        return P(f"<font color='{ah}'>{t}</font>", S["h3"])

    steps = Table([[NumBadge(i + 1, acc), P(s, S["cell_b"])] for i, s in enumerate(pasos)], colWidths=[21, 318])
    steps.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                               ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 2),
                               ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]))
    right = [h3("OBJETIVO"), P(item["objetivo"], S["cell_b"]),
             h3("CÓMO LLEGAR"), P(item["acceso"], S["cell_b"]),
             h3("PASO A PASO"), steps,
             h3("RESPUESTA DEL SISTEMA"), P(item["comportamiento"], S["cell_b"])]
    phone = PhoneFrame(os.path.join(IMG_DIR, item["file"]), 160, item["file"])
    two = Table([[phone, right]], colWidths=[178, 337])
    two.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                             ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 0),
                             ("BOTTOMPADDING", (0, 0), (-1, -1), 0), ("LEFTPADDING", (1, 0), (1, 0), 10)]))
    out += [two, Spacer(1, 12)]

    rows = [[P("ELEMENTO DE LA PANTALLA", S["cell_h"]), P("FUNCIÓN", S["cell_h"])]]
    for b in item["botones"]:
        n, d = split_element(b)
        rows.append([P(f"<b>{n}</b>", S["cell"]), P(d, S["cell"])])
    t = Table(rows, colWidths=[155, 360], repeatRows=1)
    st = [("BACKGROUND", (0, 0), (-1, 0), acc), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("TOPPADDING", (0, 0), (-1, -1), 4.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
          ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
          ("LINEBELOW", (0, 1), (-1, -1), 0.4, C_BORDER), ("BOX", (0, 0), (-1, -1), 0.6, C_BORDER)]
    for r in range(2, len(rows), 2):
        st.append(("BACKGROUND", (0, r), (-1, r), C_GRAY_BG))
    t.setStyle(TableStyle(st))
    out += [t, Spacer(1, 10), callout(S, ckind, ctext)]
    return out


# ========================================================================================
# PÁGINAS INTRODUCTORIAS
# ========================================================================================
def intro_flowables(S):
    out = []
    sec = "Introducción"
    # ---------------------------------------------------------------- 1. Presentación
    out += section_head(S, "1. ", "Presentación del manual", "Qué es esta guía y cómo aprovecharla", "sec_1", sec)
    out += [P(f"Este manual explica, pantalla a pantalla, cómo utilizar <b>{APP_NAME}</b>, una aplicación web "
              "progresiva (PWA) de registro de jornada laboral. Está dirigido a las personas que la usan a diario y "
              "se organiza según los dos perfiles existentes: el <b>Administrador</b>, que gestiona personal, "
              "proyectos y auditoría de fichajes, y el <b>Empleado</b>, que registra y consulta su propia jornada.", S["body"]),
            P("Cada una de las 19 pantallas se documenta en una ficha de una página con su captura, objetivo, ruta de "
              "acceso, paso a paso, descripción de elementos y comportamiento del sistema. Al final se incluyen guías "
              "rápidas por tarea, preguntas frecuentes, resolución de problemas y un glosario.", S["body"]),
            P("Qué encontrará en cada ficha", S["h2"])]
    out += bullets(S, ["<b>Objetivo:</b> para qué sirve la pantalla y qué problema resuelve.",
                       "<b>Cómo llegar:</b> la acción que conduce a ella.",
                       "<b>Paso a paso:</b> la secuencia recomendada para completar la tarea.",
                       "<b>Elementos de la pantalla:</b> cada botón o campo y su función.",
                       "<b>Respuesta del sistema:</b> qué verá y cómo reacciona la aplicación."])
    out.append(P("Convenciones del manual", S["h2"]))
    leg = [("Administrador", C_GREEN, "Pantallas y funciones del perfil de administración (tema verde)."),
           ("Empleado", C_BLUE, "Pantallas y funciones del portal del trabajador (tema azul)."),
           ("Acceso y seguridad", C_NAVY, "Inicio y cierre de sesión, y todo lo relativo a credenciales."),
           ("Error o acción destructiva", C_DANGER, "Mensajes de error y operaciones irreversibles, como eliminar.")]
    lt = Table([[P(f"<b>{n}</b>", S["cell_h"]), P(d, S["cell"])] for n, c, d in leg], colWidths=[140, 375])
    lt.setStyle(TableStyle([("BACKGROUND", (0, i), (0, i), c) for i, (n, c, d) in enumerate(leg)] + [
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6), ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, colors.white), ("BOX", (0, 0), (-1, -1), 0.6, C_BORDER)]))
    out += [lt, Spacer(1, 10),
            callout(S, "tip", "Los recuadros de <b>Consejo</b> recogen buenas prácticas para trabajar con más rapidez."), Spacer(1, 5),
            callout(S, "warn", "Los recuadros de <b>Atención</b> avisan de acciones con consecuencias o riesgos."), Spacer(1, 5),
            callout(S, "note", "Los recuadros de <b>Nota</b> aclaran detalles de funcionamiento.")]

    # ---------------------------------------------------------------- 2. Primeros pasos
    out += [PageBreak()]
    out += section_head(S, "2. ", "Primeros pasos", "Requisitos, instalación y permisos", "sec_2", sec)
    out.append(P("Requisitos", S["h2"]))
    out.append(data_table(S, ["REQUISITO", "DETALLE"], [
        ["<b>Dispositivo</b>", "Smartphone, tablet u ordenador."],
        ["<b>Navegador</b>", "Versión actual de Chrome, Edge, Safari o Firefox."],
        ["<b>Conexión</b>", "Acceso a Internet: la aplicación se comunica con el servidor para validar y guardar los datos."],
        ["<b>Ubicación</b>", "Permiso de geolocalización del navegador para poder fichar la entrada."],
        ["<b>Credenciales</b>", "Usuario y contraseña facilitados por el administrador de su organización."]], [120, 395]))
    out.append(P("Instalar la aplicación en su dispositivo", S["h2"]))
    out.append(P("Al ser una PWA, puede usarse directamente desde el navegador o instalarse en la pantalla de inicio "
                 "para abrirla como cualquier otra aplicación.", S["body"]))
    cards = [("Android (Chrome)", "Abra el menú del navegador (tres puntos) y elija «Instalar aplicación» o «Añadir a pantalla de inicio»."),
             ("iPhone / iPad (Safari)", "Pulse el botón Compartir y elija «Añadir a pantalla de inicio»."),
             ("Ordenador (Chrome / Edge)", "Pulse el icono de instalación de la barra de direcciones y confirme.")]
    ct = Table([[P(f"<b>{a}</b>", S["cell_h"]) for a, b in cards], [P(b, S["cell"]) for a, b in cards]],
               colWidths=[CW / 3.0] * 3)
    ct.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), C_BLUE), ("BACKGROUND", (0, 1), (-1, 1), C_BLUE_BG),
                            ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 6),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 7), ("LEFTPADDING", (0, 0), (-1, -1), 9),
                            ("RIGHTPADDING", (0, 0), (-1, -1), 9), ("LINEAFTER", (0, 0), (-2, -1), 3, colors.white),
                            ("BOX", (0, 0), (-1, -1), 0.6, C_BORDER)]))
    out += [ct, Spacer(1, 6),
            callout(S, "note", "Los nombres exactos de las opciones pueden variar ligeramente según el navegador y su versión.")]
    out.append(P("Permiso de ubicación", S["h2"]))
    out.append(P("Al fichar la entrada, la aplicación captura la posición GPS del dispositivo para que el administrador "
                 "pueda comprobar dónde se inició la jornada. Cuando el navegador lo solicite, pulse «Permitir». "
                 "Si lo denegó por error, puede reactivarlo desde los ajustes del sitio en el navegador.", S["body"]))

    out.append(P("Credenciales de demostración", S["h2"]))
    out.append(data_table(S, ["PERFIL", "USUARIO", "CONTRASEÑA"], [
        ["Administrador", "<b>admin</b>", "admin123"], ["Empleado", "<b>sergio</b>", "1234"]], [170, 170, 175]))
    out += [Spacer(1, 6), callout(S, "warn", "Son cuentas de prueba para la demostración. En un entorno real, el administrador debe "
                                          "sustituirlas por credenciales propias y robustas.")]

    # ---------------------------------------------------------------- 3. Perfiles
    out += [PageBreak()]
    out += section_head(S, "3. ", "Perfiles, permisos y navegación", "Qué puede hacer cada usuario y cómo se mueve por la aplicación", "sec_3", sec)
    out.append(P("Perfiles de acceso", S["h2"]))
    out.append(data_table(S, ["PERFIL", "IDENTIDAD", "ALCANCE FUNCIONAL PRINCIPAL"], [
        ["<b>Administrador</b>", f"<font color='{hx(C_GREEN)}'><b>Tema verde</b></font>",
         "Mantenimiento de personal y catálogo de trabajos, auditoría horaria con filtros de fecha, visor de mapa con chincheta GPS y borrado de turnos."],
        ["<b>Empleado</b>", f"<font color='{hx(C_BLUE)}'><b>Tema azul</b></font>",
         "Registro de entradas, tareas simultáneas en paralelo, cierre instantáneo de turnos y consulta del historial de horas."]],
        [100, 85, 330]))
    out.append(P("Permisos por perfil", S["h2"]))
    yes, no = "<font color='#16A34A'><b>Sí</b></font>", "<font color='#94A3B8'>—</font>"
    perm = [("Iniciar y cerrar sesión", yes, yes), ("Ver el listado de personal", yes, no),
            ("Alta, edición y baja de usuarios", yes, no), ("Gestionar el catálogo de trabajos", yes, no),
            ("Registrar entrada y salida propias", no, yes), ("Mantener varios fichajes en paralelo", no, yes),
            ("Consultar fichajes", "Todos los empleados", "Solo los propios"),
            ("Ver ubicación GPS en un mapa", yes, no), ("Eliminar fichajes", yes, no)]
    out.append(data_table(S, ["FUNCIÓN", "ADMINISTRADOR", "EMPLEADO"],
                          [[a, P(b, S["cell_c"]), P(c, S["cell_c"])] for a, b, c in perm], [255, 130, 130]))
    out.append(P("Mapa de navegación", S["h2"]))
    out += [NavMap(), Spacer(1, 6)]
    return out


# ========================================================================================
# ANEXOS
# ========================================================================================
def recipe(S, title, color, steps):
    rows = [[P(f"<b>{title}</b>", S["cell_h"]), ""]]
    rows += [[P(f"<font color='{hx(color)}'><b>{i + 1}</b></font>", S["cell_c"]), P(s, S["cell"])] for i, s in enumerate(steps)]
    t = Table(rows, colWidths=[28, CW - 28])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), color), ("SPAN", (0, 0), (1, 0)),
                           ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 4),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 4), ("LEFTPADDING", (0, 0), (-1, -1), 7),
                           ("LINEBELOW", (0, 1), (-1, -1), 0.4, C_BORDER), ("BOX", (0, 0), (-1, -1), 0.6, C_BORDER)]))
    return KeepTogether([t, Spacer(1, 9)])


def annex_flowables(S):
    out = [PageBreak()]
    sec = "Anexos"
    out += section_head(S, "Anexo A · ", "Guías rápidas por tarea", "Las operaciones más habituales, resumidas", "anx_a", sec)
    out += [recipe(S, "Administrador · Dar de alta a un empleado", C_GREEN, [
                "Inicie sesión como administrador y entre en «Gestión de Usuarios».",
                "Pulse «Añadir Nuevo Usuario».", "Rellene ID, nombre completo, usuario, contraseña y rol «Empleado».",
                "Pulse «Crear Usuario»: el empleado podrá iniciar sesión al instante."]),
            recipe(S, "Administrador · Crear un nuevo proyecto", C_GREEN, [
                "Entre en «Gestión de Trabajos» y pulse «Crear Nuevo Trabajo».",
                "Indique el ID numérico y el nombre del proyecto.",
                "Pulse «Guardar Trabajo»: aparecerá en el desplegable de fichaje de los empleados."]),
            recipe(S, "Administrador · Auditar fichajes de un periodo", C_GREEN, [
                "Entre en «Gestión de Fichajes».", "Seleccione empleado (o toda la plantilla) y las fechas de inicio y fin.",
                "Pulse «Aplicar Filtros» y revise horas totales por tarjeta.",
                "Use «Ver Mapa de Fichaje» para comprobar la ubicación o la papelera para borrar registros erróneos."]),
            recipe(S, "Empleado · Fichar una jornada", C_BLUE, [
                "Entre en «Registrar Fichaje» y elija el proyecto en «Seleccionar Trabajo».",
                "Pulse «Fichar Entrada» y acepte el permiso de ubicación.",
                "Al terminar, pulse «Finalizar Fichaje» en la tarjeta del turno en curso."]),
            recipe(S, "Empleado · Trabajar en varias tareas a la vez", C_BLUE, [
                "Fiche la primera tarea con normalidad.", "Seleccione otra tarea en la tarjeta superior y pulse de nuevo «Fichar Entrada».",
                "Compruebe el contador de turnos activos de la cabecera.",
                "Finalice cada tarea con el botón de su propia tarjeta; las demás siguen abiertas."]),
            recipe(S, "Empleado · Revisar mis horas", C_BLUE, [
                "Entre en «Consulta de Fichajes».", "Indique «Fecha Inicio» y «Fecha Fin».",
                "Lea las tarjetas: proyecto, entrada, salida y total de horas calculadas."])]

    out += [PageBreak()]
    out += section_head(S, "Anexo B · ", "Preguntas frecuentes", "Respuestas rápidas a las dudas más comunes", "anx_b", sec)
    faq = [("¿Puedo tener varias tareas abiertas a la vez?",
            "Sí. Como empleado puede iniciar tantos turnos en paralelo como necesite; cada uno se contabiliza de forma independiente y se finaliza por separado."),
           ("¿Qué hago si me equivoco de proyecto al fichar?",
            "Finalice el turno e informe al administrador: puede eliminar registros erróneos desde «Gestión de Fichajes». Después podrá fichar de nuevo en el proyecto correcto."),
           ("¿Quién puede ver mi ubicación?",
            "La posición se captura al fichar la entrada y puede consultarla el administrador desde el mapa de la auditoría de fichajes."),
           ("¿Cómo cambio mi contraseña?",
            "Las claves las gestiona el administrador desde la edición de usuarios. Solicítele el cambio."),
           ("¿Puedo borrar mis propios fichajes?",
            "No. Solo el administrador puede eliminar registros, siempre previa confirmación."),
           ("¿Qué significan «En Curso» y «Abierto»?",
            "Que el turno se ha iniciado y todavía no se ha finalizado. Al finalizarlo pasa a «Completado»."),
           ("¿Los cambios del administrador se ven de inmediato?",
            "Sí. Por ejemplo, un proyecto nuevo o renombrado aparece en el desplegable de fichaje de los empleados en tiempo real.")]
    for q, a in faq:
        out.append(KeepTogether([P(q, S["faq_q"]), P(a, S["body"])]))

    out += [PageBreak()]
    out += section_head(S, "Anexo C · ", "Resolución de problemas", "Síntomas frecuentes y cómo resolverlos", "anx_c", sec)
    out.append(data_table(S, ["SÍNTOMA", "CAUSA PROBABLE", "QUÉ HACER"], [
        ["<b>No puedo iniciar sesión</b>", "Usuario o contraseña incorrectos.",
         "Revise el usuario, mayúsculas y teclado. Si persiste, pida al administrador que restablezca su clave."],
        ["<b>No aparece el proyecto al fichar</b>", "No está creado en el catálogo.",
         "Solicite al administrador que lo cree en «Gestión de Trabajos»."],
        ["<b>El mapa no muestra la ubicación</b>", "Permiso de ubicación denegado o conexión inestable.",
         "Active la ubicación para el sitio en el navegador, compruebe la conexión y vuelva a fichar si es necesario."],
        ["<b>Las listas no cargan</b>", "Conexión a Internet inestable o caída.", "Compruebe la conexión y recargue la aplicación."],
        ["<b>Aparece un fichaje duplicado</b>", "Doble pulsación del botón.",
         "El administrador puede eliminar el duplicado desde «Gestión de Fichajes»."]],
        [150, 160, 205], color=C_AMBER))

    out += [Spacer(1, 14), CondPageBreak(260)]
    out += section_head(S, "Anexo D · ", "Glosario", "Términos utilizados en este manual", "anx_d", sec)
    out.append(data_table(S, ["TÉRMINO", "DEFINICIÓN"], [
        ["<b>PWA</b>", "Aplicación web progresiva: se usa desde el navegador y puede instalarse en la pantalla de inicio."],
        ["<b>Ionic</b>", "Marco de desarrollo con el que se ha construido la interfaz de la aplicación."],
        ["<b>API REST</b>", "Servicio con el que la aplicación intercambia datos de usuarios, trabajos y fichajes."],
        ["<b>Fichaje</b>", "Registro de una jornada o tarea: proyecto, hora de entrada, hora de salida y total de horas."],
        ["<b>Turno en curso</b>", "Fichaje iniciado que todavía no se ha finalizado (estado «Abierto»)."],
        ["<b>Toast</b>", "Aviso emergente breve en la parte inferior (verde: éxito; rojo: error)."],
        ["<b>Modal</b>", "Ventana emergente superpuesta que sirve para consultar o editar datos."],
        ["<b>Rol</b>", "Perfil que determina los permisos de una cuenta: Administrador o Empleado."],
        ["<b>Geolocalización</b>", "Coordenadas GPS capturadas por el dispositivo al fichar la entrada."],
        ["<b>Leaflet / OpenStreetMap</b>", "Visor de mapas interactivo y cartografía abierta usados para mostrar la ubicación."],
        ["<b>Panel</b>", "Pantalla principal de cada perfil, con tarjetas de acceso a los módulos."]], [140, 375]))
    return out


# ========================================================================================
# CONSTRUCCIÓN DEL DOCUMENTO
# ========================================================================================
def build_story(S):
    story = [Spacer(1, 1), NextPageTemplate("Body"), PageBreak()]

    # Índice
    story.append(TocMarker(0, "Índice de contenidos", "indice", section="Índice", toc=False))
    story += [P("Índice de contenidos", S["h1"]),
              P("Pulse sobre cualquier entrada para saltar directamente a ella.", S["h1_sub"]),
              HRFlowable(width="100%", thickness=2, color=C_BLUE, spaceBefore=2, spaceAfter=6)]
    toc = TableOfContents()
    toc.dotsMinLevel = 0
    toc.rightColumnWidth = 36
    toc.levelStyles = [S["toc0"], S["toc1"]]
    story += [toc, PageBreak()]

    story += intro_flowables(S)

    total = len(SCREENS_DATA)
    for part in PARTS:
        story += [NextPageTemplate("Div" + part["num"]), PageBreak()]
        acc = part["accent"]
        story.append(TocMarker(0, f"Parte {part['num']}: {part['name']}", f"part_{part['num']}",
                               section=f"Parte {part['num']}: {part['name']}"))
        story += [P(f"<font color='{acc}'>PARTE {part['num']}</font>",
                    ParagraphStyle("dl", fontName="Helvetica-Bold", fontSize=12, leading=16, textColor=colors.white, spaceAfter=6)),
                  P(part["name"], ParagraphStyle("dt", fontName="Helvetica-Bold", fontSize=34, leading=40, textColor=colors.white, spaceAfter=12)),
                  P(part["desc"], ParagraphStyle("dd", fontName="Helvetica", fontSize=11.5, leading=17,
                                                   textColor=colors.HexColor("#CBD5E1"), spaceAfter=22)),
                  P("EN ESTA PARTE", ParagraphStyle("dh", fontName="Helvetica-Bold", fontSize=8, leading=12,
                                                    textColor=colors.HexColor(acc), spaceAfter=5))]
        for it in SCREENS_DATA:
            if part["ids"][0] <= int(it["id"]) <= part["ids"][1]:
                story.append(P(f"<font color='{acc}'><b>{it['id']}</b></font>&nbsp;&nbsp;&nbsp;"
                               f"<a href='#scr_{it['id']}' color='white'>{it['title']}</a>",
                               ParagraphStyle("dli", fontName="Helvetica", fontSize=10.5, leading=17, textColor=colors.white)))
        story += [NextPageTemplate("Body"), PageBreak()]
        items = [(i, it) for i, it in enumerate(SCREENS_DATA) if part["ids"][0] <= int(it["id"]) <= part["ids"][1]]
        for k, (i, it) in enumerate(items):
            story += screen_flowables(S, it, i, total)
            if k < len(items) - 1:
                story.append(PageBreak())

    story += annex_flowables(S)
    return story


def generar_manual_pdf(dest_path):
    print(f"[PDF] Compilando el manual en: {dest_path}")
    S = make_styles()
    doc = ManualDoc(dest_path)
    doc.multiBuild(build_story(S), canvasmaker=NumberedCanvas)
    print(f"[OK] PDF generado: {dest_path}")


if __name__ == "__main__":
    nombre = "Manual_Usuario_PWA_Control_Horario.pdf"
    if len(sys.argv) > 1:
        generar_manual_pdf(sys.argv[1])
    else:
        principal = os.path.join(SCRIPT_DIR, nombre)
        generar_manual_pdf(principal)
        destinos = []
        if os.path.isdir(DESKTOP_DIR):
            destinos.append(os.path.join(DESKTOP_DIR, nombre))
        if os.path.isdir(DESKTOP_CAPT_DIR):
            destinos.append(os.path.join(DESKTOP_CAPT_DIR, "Presentacion_Capturas_PWA.pdf"))
        local = os.path.join(SCRIPT_DIR, "Capturas_Responsive_470x900")
        if os.path.isdir(local):
            destinos.append(os.path.join(local, "Presentacion_Capturas_PWA.pdf"))
        for d in destinos:
            if os.path.abspath(d) != os.path.abspath(principal):
                shutil.copyfile(principal, d)
                print(f"[COPIA] {d}")
        print("\n[FINALIZADO] Manual generado correctamente.")
