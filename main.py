"""
==========================================================
  SERVER MAKER  v1.4
  Servidor web ligero para PCs modestas (2 GB RAM).
  · Idiomas: Español · English · Português
  · Estilos: AERO · MINIMAL
  · Modos:   CLARO · OSCURO
  · Barra de URL generada (servermaker.com/[Carpeta])
  · Nombre del servidor personalizable
  Solo librería estándar · Python 3.14 / IDLE
==========================================================
"""

import os
import socket
import threading
import webbrowser
import http.server
import tkinter as tk
from tkinter import filedialog, messagebox, font as tkfont
from datetime import datetime
from functools import partial


# ==========================================================
#  TRADUCCIONES
# ==========================================================
IDIOMAS = {
    "ES": {
        "titulo_app":       "Server Maker",
        "subtitulo":        "Servidor ligero · v1.4",
        "nombre_defecto":   "Mi Servidor",
        "lbl_nombre":       "NOMBRE DEL SERVIDOR",
        "lbl_carpeta":      "CARPETA A COMPARTIR",
        "lbl_host":         "HOST",
        "lbl_puerto":       "PUERTO",
        "lbl_url":          "ENLACE PARA COMPARTIR",
        "ip_local":         "IP local:",
        "btn_elegir":       "Examinar",
        "btn_iniciar":      "▶   Iniciar",
        "btn_detener":      "■   Detener",
        "btn_abrir":        "🌍  Abrir en navegador",
        "log_titulo":       "REGISTRO",
        "estado_detenido":  "●  Detenido",
        "estado_activo":    "●  Activo en http://{ip}:{puerto}",
        "listo":            "Server Maker iniciado. Listo para arrancar.",
        "err_titulo":       "Error",
        "err_carpeta":      "Selecciona una carpeta válida.",
        "err_puerto":       "El puerto debe estar entre 1 y 65535.",
        "err_puerto_inv":   "Puerto inválido.",
        "err_puerto_tit":   "Error al abrir el puerto",
        "err_puerto_msg":   "No se pudo iniciar en {host}:{puerto}\n\n{e}",
        "log_iniciado":     "Servidor «{nombre}» iniciado · {host}:{puerto}",
        "log_raiz":         "Carpeta raíz: {carpeta}",
        "log_pista":        "Pulsa Detener para liberar el puerto.",
        "log_detenido":     "Servidor detenido.",
        "log_aviso":        "Aviso al cerrar: {e}",
        "log_lang":         "Idioma cambiado a Español.",
        "log_estilo":       "Estilo cambiado a {estilo}.",
        "log_modo":         "Modo cambiado a {modo}.",
        "url_copiado":      "✓  Copiado",
        "url_copiar":       "📋",
        "modo_claro":       "Claro",
        "modo_oscuro":      "Oscuro",
    },
    "EN": {
        "titulo_app":       "Server Maker",
        "subtitulo":        "Lightweight server · v1.4",
        "nombre_defecto":   "My Server",
        "lbl_nombre":       "SERVER NAME",
        "lbl_carpeta":      "FOLDER TO SHARE",
        "lbl_host":         "HOST",
        "lbl_puerto":       "PORT",
        "lbl_url":          "SHAREABLE LINK",
        "ip_local":         "Local IP:",
        "btn_elegir":       "Browse",
        "btn_iniciar":      "▶   Start",
        "btn_detener":      "■   Stop",
        "btn_abrir":        "🌍  Open in browser",
        "log_titulo":       "LOG",
        "estado_detenido":  "●  Stopped",
        "estado_activo":    "●  Running at http://{ip}:{puerto}",
        "listo":            "Server Maker started. Ready to launch.",
        "err_titulo":       "Error",
        "err_carpeta":      "Please select a valid folder.",
        "err_puerto":       "Port must be between 1 and 65535.",
        "err_puerto_inv":   "Invalid port.",
        "err_puerto_tit":   "Error opening port",
        "err_puerto_msg":   "Could not start on {host}:{puerto}\n\n{e}",
        "log_iniciado":     "Server «{nombre}» started · {host}:{puerto}",
        "log_raiz":         "Root folder: {carpeta}",
        "log_pista":        "Press Stop to free the port.",
        "log_detenido":     "Server stopped.",
        "log_aviso":        "Warning while closing: {e}",
        "log_lang":         "Language changed to English.",
        "log_estilo":       "Style changed to {estilo}.",
        "log_modo":         "Mode changed to {modo}.",
        "url_copiado":      "✓  Copied",
        "url_copiar":       "📋",
        "modo_claro":       "Light",
        "modo_oscuro":      "Dark",
    },
    "PT": {
        "titulo_app":       "Server Maker",
        "subtitulo":        "Servidor leve · v1.4",
        "nombre_defecto":   "Meu Servidor",
        "lbl_nombre":       "NOME DO SERVIDOR",
        "lbl_carpeta":      "PASTA PARA COMPARTILHAR",
        "lbl_host":         "HOST",
        "lbl_puerto":       "PORTA",
        "lbl_url":          "LINK PARA COMPARTILHAR",
        "ip_local":         "IP local:",
        "btn_elegir":       "Escolher",
        "btn_iniciar":      "▶   Iniciar",
        "btn_detener":      "■   Parar",
        "btn_abrir":        "🌍  Abrir no navegador",
        "log_titulo":       "REGISTRO",
        "estado_detenido":  "●  Parado",
        "estado_activo":    "●  Ativo em http://{ip}:{puerto}",
        "listo":            "Server Maker iniciado. Pronto para arrancar.",
        "err_titulo":       "Erro",
        "err_carpeta":      "Selecione uma pasta válida.",
        "err_puerto":       "A porta deve estar entre 1 e 65535.",
        "err_puerto_inv":   "Porta inválida.",
        "err_puerto_tit":   "Erro ao abrir a porta",
        "err_puerto_msg":   "Não foi possível iniciar em {host}:{puerto}\n\n{e}",
        "log_iniciado":     "Servidor «{nombre}» iniciado · {host}:{puerto}",
        "log_raiz":         "Pasta raiz: {carpeta}",
        "log_pista":        "Pressione Parar para liberar a porta.",
        "log_detenido":     "Servidor parado.",
        "log_aviso":        "Aviso ao fechar: {e}",
        "log_lang":         "Idioma alterado para Português.",
        "log_estilo":       "Estilo alterado para {estilo}.",
        "log_modo":         "Modo alterado para {modo}.",
        "url_copiado":      "✓  Copiado",
        "url_copiar":       "📋",
        "modo_claro":       "Claro",
        "modo_oscuro":      "Escuro",
    },
}


# ==========================================================
#  TEMAS  (Estilo x Modo)
# ==========================================================
TEMAS = {
    # --------- AERO CLARO ---------
    "AERO_CLARO": {
        "fondo_top": "#f6fafe", "fondo_bot": "#d3e3f2", "gradiente_fondo": True,
        "header_top": "#4d8ec8", "header_bot": "#2c5a8f", "gradiente_header": True,
        "header_top1": "#9ec8e8", "header_top2": "#6ea8d5",
        "header_bot1": "#1c3f68", "header_bot2": "#b8cfe4",
        "titulo_fg": "#ffffff", "subtitulo_fg": "#cbdcf0",
        "label_fg": "#6a7b8d",
        "entry_bg": "#ffffff", "entry_fg": "#2c3e50",
        "entry_border": "#b8cfe4", "entry_cursor": "#3a6ea5",
        "panel_bg": "#fbfdff", "panel_border": "#b8cfe4",
        "log_bg": "#fbfdff", "log_fg": "#3c5a7a", "log_sep": "#e2ecf5",
        "url_bg": "#eaf3fb", "url_border": "#b8cfe4",
        "url_icon_fg": "#3a6ea5", "url_base_fg": "#6a7b8d",
        "url_accent_fg": "#1f4f80", "url_hint_fg": "#3a6ea5",
        "sel_normal_bg": "#3d75b0", "sel_normal_fg": "#ffffff",
        "sel_normal_outline": "#7fb3dd",
        "sel_hover_bg": "#5d8cc5", "sel_hover_outline": "#a5cce9",
        "sel_active_bg": "#ffffff", "sel_active_fg": "#2c5a8f",
        "sel_active_outline": "#ffffff",
        "btn_iniciar": "#2f7d3a", "btn_iniciar_hover": "#3a9a48",
        "btn_detener": "#a03a3a", "btn_detener_hover": "#c04848",
        "btn_abrir":   "#3a6ea5", "btn_abrir_hover":   "#4a8ac5",
        "btn_elegir":  "#6c8ba8", "btn_elegir_hover":  "#7fa1bd",
        "btn_disabled_bg": "#c8d2dc", "btn_disabled_fg": "#eef2f6",
        "radius": 8, "radius_small": 6,
        "estado_activo": "#1e7a3a", "estado_detenido": "#a03a3a",
    },
    # --------- AERO OSCURO ---------
    "AERO_OSCURO": {
        "fondo_top": "#1a2332", "fondo_bot": "#0d1620", "gradiente_fondo": True,
        "header_top": "#1e3a5f", "header_bot": "#0d2440", "gradiente_header": True,
        "header_top1": "#3a6a9a", "header_top2": "#2a4a6a",
        "header_bot1": "#051020", "header_bot2": "#2a4a6a",
        "titulo_fg": "#eaf3fb", "subtitulo_fg": "#8ba5c5",
        "label_fg": "#7a90aa",
        "entry_bg": "#0d1620", "entry_fg": "#e0e8f0",
        "entry_border": "#2a3d52", "entry_cursor": "#5da5e0",
        "panel_bg": "#141c28", "panel_border": "#2a3d52",
        "log_bg": "#141c28", "log_fg": "#9bb5cc", "log_sep": "#1e2a3a",
        "url_bg": "#0f1e30", "url_border": "#2a4a6a",
        "url_icon_fg": "#5da5e0", "url_base_fg": "#7a90aa",
        "url_accent_fg": "#7fc5f5", "url_hint_fg": "#5da5e0",
        "sel_normal_bg": "#1e3a5f", "sel_normal_fg": "#8ba5c5",
        "sel_normal_outline": "#2a4a6a",
        "sel_hover_bg": "#2a4a6a", "sel_hover_outline": "#3a6a8a",
        "sel_active_bg": "#5da5e0", "sel_active_fg": "#0d1620",
        "sel_active_outline": "#5da5e0",
        "btn_iniciar": "#2a7d3a", "btn_iniciar_hover": "#3a9a48",
        "btn_detener": "#8a3030", "btn_detener_hover": "#b04040",
        "btn_abrir":   "#2a5a8a", "btn_abrir_hover":   "#3a7aad",
        "btn_elegir":  "#3a556b", "btn_elegir_hover":  "#4d6e88",
        "btn_disabled_bg": "#2a3d52", "btn_disabled_fg": "#5a6a7a",
        "radius": 8, "radius_small": 6,
        "estado_activo": "#4ac86a", "estado_detenido": "#e05a5a",
    },
    # --------- MINIMAL CLARO ---------
    "MINIMAL_CLARO": {
        "fondo_top": "#ffffff", "fondo_bot": "#ffffff", "gradiente_fondo": False,
        "header_top": "#ffffff", "header_bot": "#ffffff", "gradiente_header": False,
        "header_top1": None, "header_top2": None,
        "header_bot1": "#e4e4e4", "header_bot2": None,
        "titulo_fg": "#1a1a1a", "subtitulo_fg": "#999999",
        "label_fg": "#8a8a8a",
        "entry_bg": "#ffffff", "entry_fg": "#1a1a1a",
        "entry_border": "#d8d8d8", "entry_cursor": "#1a1a1a",
        "panel_bg": "#fafafa", "panel_border": "#e0e0e0",
        "log_bg": "#fafafa", "log_fg": "#333333", "log_sep": "#e8e8e8",
        "url_bg": "#f7f7f7", "url_border": "#e0e0e0",
        "url_icon_fg": "#666666", "url_base_fg": "#999999",
        "url_accent_fg": "#1a1a1a", "url_hint_fg": "#666666",
        "sel_normal_bg": "#f4f4f4", "sel_normal_fg": "#666666",
        "sel_normal_outline": "#e0e0e0",
        "sel_hover_bg": "#e6e6e6", "sel_hover_outline": "#d0d0d0",
        "sel_active_bg": "#1a1a1a", "sel_active_fg": "#ffffff",
        "sel_active_outline": "#1a1a1a",
        "btn_iniciar": "#1a1a1a", "btn_iniciar_hover": "#333333",
        "btn_detener": "#6b6b6b", "btn_detener_hover": "#808080",
        "btn_abrir":   "#4a4a4a", "btn_abrir_hover":   "#5e5e5e",
        "btn_elegir":  "#8a8a8a", "btn_elegir_hover":  "#a0a0a0",
        "btn_disabled_bg": "#e8e8e8", "btn_disabled_fg": "#b6b6b6",
        "radius": 4, "radius_small": 4,
        "estado_activo": "#1a7a3a", "estado_detenido": "#a03a3a",
    },
    # --------- MINIMAL OSCURO ---------
    "MINIMAL_OSCURO": {
        "fondo_top": "#1e1e1e", "fondo_bot": "#1e1e1e", "gradiente_fondo": False,
        "header_top": "#1e1e1e", "header_bot": "#1e1e1e", "gradiente_header": False,
        "header_top1": None, "header_top2": None,
        "header_bot1": "#333333", "header_bot2": None,
        "titulo_fg": "#ffffff", "subtitulo_fg": "#888888",
        "label_fg": "#888888",
        "entry_bg": "#2a2a2a", "entry_fg": "#e8e8e8",
        "entry_border": "#3a3a3a", "entry_cursor": "#ffffff",
        "panel_bg": "#252525", "panel_border": "#333333",
        "log_bg": "#252525", "log_fg": "#c0c0c0", "log_sep": "#333333",
        "url_bg": "#252525", "url_border": "#3a3a3a",
        "url_icon_fg": "#a0a0a0", "url_base_fg": "#808080",
        "url_accent_fg": "#ffffff", "url_hint_fg": "#a0a0a0",
        "sel_normal_bg": "#2a2a2a", "sel_normal_fg": "#a0a0a0",
        "sel_normal_outline": "#3a3a3a",
        "sel_hover_bg": "#3a3a3a", "sel_hover_outline": "#4a4a4a",
        "sel_active_bg": "#ffffff", "sel_active_fg": "#1e1e1e",
        "sel_active_outline": "#ffffff",
        "btn_iniciar": "#3a8a4a", "btn_iniciar_hover": "#4aa05a",
        "btn_detener": "#8a3a3a", "btn_detener_hover": "#a04a4a",
        "btn_abrir":   "#3a6a8a", "btn_abrir_hover":   "#4a7a9a",
        "btn_elegir":  "#5a5a5a", "btn_elegir_hover":  "#6a6a6a",
        "btn_disabled_bg": "#2f2f2f", "btn_disabled_fg": "#5a5a5a",
        "radius": 4, "radius_small": 4,
        "estado_activo": "#4ac86a", "estado_detenido": "#e05a5a",
    },
}


# ==========================================================
#  NÚCLEO DEL SERVIDOR
# ==========================================================
class Manejador(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=None, log_callback=None,
                 server_nombre="Server Maker", **kwargs):
        self.log_callback = log_callback
        self._server_nombre = server_nombre
        super().__init__(*args, directory=directory, **kwargs)

    def log_message(self, fmt, *args):
        if self.log_callback:
            self.log_callback("%s - %s" % (self.address_string(), fmt % args))

    def version_string(self):
        return f"{self._server_nombre} (ServerMaker/1.4)"


class ServidorLigero(http.server.ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True
    request_queue_size = 20


def obtener_ip_local():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


# ==========================================================
#  BOTÓN PRINCIPAL
# ==========================================================
class AeroButton:
    def __init__(self, app, x, y, w, h, comando,
                 color, hover, disabled_bg, disabled_fg,
                 fuente=("Segoe UI", 10, "bold"), radius=8):
        self.app = app
        self.canvas = app.canvas
        self.color = color
        self.hover = hover
        self.disabled_bg = disabled_bg
        self.disabled_fg = disabled_fg
        self.comando = comando
        self.disabled = False

        self.rect = app._round_rect(x, y, x + w, y + h, radius,
                                    fill=color, outline="")
        self.label = tk.Label(self.canvas, text="", bg=color, fg="white",
                              font=fuente, cursor="hand2", bd=0)
        app.canvas.create_window(x + w / 2, y + h / 2, window=self.label)

        self.label.bind("<Button-1>", self._click)
        self.label.bind("<Enter>", self._enter)
        self.label.bind("<Leave>", self._leave)

    def _click(self, e):
        if not self.disabled:
            self.comando()

    def _enter(self, e):
        if not self.disabled:
            self.canvas.itemconfig(self.rect, fill=self.hover)
            self.label.config(bg=self.hover)

    def _leave(self, e):
        if not self.disabled:
            self.canvas.itemconfig(self.rect, fill=self.color)
            self.label.config(bg=self.color)

    def config_texto(self, t):
        self.label.config(text=t)

    def set_habilitado(self, habilitado):
        self.disabled = not habilitado
        if habilitado:
            self.canvas.itemconfig(self.rect, fill=self.color)
            self.label.config(bg=self.color, fg="white", cursor="hand2")
        else:
            self.canvas.itemconfig(self.rect, fill=self.disabled_bg)
            self.label.config(bg=self.disabled_bg, fg=self.disabled_fg,
                              cursor="arrow")


# ==========================================================
#  APLICACIÓN
# ==========================================================
class ServerMakerApp:
    W, H = 860, 760
    HEADER_H = 116
    URL_BASE = "https://www.servermaker.com/"

    def __init__(self, root):
        self.root = root
        self.idioma = "ES"
        self.estilo = "AERO"      # AERO | MINIMAL
        self.modo = "CLARO"       # CLARO | OSCURO

        # Estado
        self.servidor = None
        self.hilo = None
        self.activo = False
        self.ultimo_puerto = None
        self.log_historial = []
        self._reset_url_timer = None

        # Referencias
        self.textos = {}
        self.btn_idioma = {}
        self.btn_estilo = {}
        self.btn_modo = {}
        self.url_widgets = {}     # icon, base, accent, hint

        # Variables
        self.var_nombre = tk.StringVar(value="Mi Servidor")
        self.var_carpeta = tk.StringVar(value=os.getcwd())
        self.var_host = tk.StringVar(value="0.0.0.0")
        self.var_puerto = tk.StringVar(value="8000")

        self._configurar_ventana()
        self._construir_interfaz()

        self.var_nombre.trace_add("write", lambda *a: self._actualizar_nombre())
        self.var_carpeta.trace_add("write", lambda *a: self._actualizar_url_bar())

        self._aplicar_idioma()
        self._actualizar_nombre()
        self._actualizar_url_bar()
        self._log(self.T("listo"))

    # ------------------------------------------------------
    def T(self, clave, **kw):
        txt = IDIOMAS[self.idioma].get(clave, clave)
        return txt.format(**kw) if kw else txt

    def _tema_key(self):
        return f"{self.estilo}_{self.modo}"

    @property
    def tema(self):
        return TEMAS[self._tema_key()]

    # ------------------------------------------------------
    def _configurar_ventana(self):
        self.root.title("Server Maker")
        self.root.resizable(False, False)
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - self.W) // 2
        y = max(0, (sh - self.H) // 2 - 40)
        self.root.geometry(f"{self.W}x{self.H}+{x}+{y}")

    # ------------------------------------------------------
    #  Helpers de dibujo
    # ------------------------------------------------------
    @staticmethod
    def _hex_to_rgb(c):
        c = c.lstrip('#')
        return int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)

    def _gradient(self, x1, y1, x2, y2, color1, color2):
        r1, g1, b1 = self._hex_to_rgb(color1)
        r2, g2, b2 = self._hex_to_rgb(color2)
        h = y2 - y1
        for i in range(h):
            t = i / max(h - 1, 1)
            r = int(r1 + (r2 - r1) * t)
            g = int(g1 + (g2 - g1) * t)
            b = int(b1 + (b2 - b1) * t)
            self.canvas.create_line(x1, y1 + i, x2, y1 + i,
                                    fill=f"#{r:02x}{g:02x}{b:02x}")

    def _round_rect(self, x1, y1, x2, y2, r, **kw):
        pts = [
            x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r,
            x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2,
            x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
        ]
        return self.canvas.create_polygon(pts, smooth=True, **kw)

    def _entry_redondeado(self, x, y, w, h, var, size=10):
        t = self.tema
        self._round_rect(x, y, x + w, y + h, t["radius_small"],
                         fill=t["entry_bg"], outline=t["entry_border"], width=1)
        e = tk.Entry(self.canvas, textvariable=var, bd=0,
                     bg=t["entry_bg"], fg=t["entry_fg"],
                     font=("Segoe UI", size),
                     insertbackground=t["entry_cursor"],
                     highlightthickness=0, relief="flat")
        self.canvas.create_window(x + 12, y + h / 2, window=e,
                                  anchor="w", width=w - 24)
        return e

    def _etiqueta(self, x, y, texto, size=8, bold=True):
        t = self.tema
        fuente = ("Segoe UI", size, "bold") if bold else ("Segoe UI", size)
        return self.canvas.create_text(x, y, text=texto, font=fuente,
                                       fill=t["label_fg"], anchor="w")

    # ------------------------------------------------------
    #  Selectores (idioma / estilo / modo)
    # ------------------------------------------------------
    def _crear_selector(self, items, x_right, y, w, h, callback,
                        es_activo, fuente_size=8):
        t = self.tema
        gap = 6
        total = len(items) * w + (len(items) - 1) * gap
        x_start = x_right - total
        resultado = {}
        for i, (ident, texto) in enumerate(items):
            x = x_start + i * (w + gap)
            activo = es_activo(ident)
            bg = t["sel_active_bg"] if activo else t["sel_normal_bg"]
            fg = t["sel_active_fg"] if activo else t["sel_normal_fg"]
            outline = (t["sel_active_outline"] if activo
                       else t["sel_normal_outline"])

            rect = self._round_rect(x, y, x + w, y + h, t["radius_small"],
                                    fill=bg, outline=outline, width=1)
            lbl = tk.Label(self.canvas, text=texto, bg=bg, fg=fg,
                           font=("Segoe UI", fuente_size, "bold"),
                           cursor="hand2", bd=0)
            self.canvas.create_window(x + w / 2, y + h / 2, window=lbl)

            def _click(e, id_=ident):
                callback(id_)

            def _enter(e, r=rect, l=lbl, act=activo):
                if not act:
                    self.canvas.itemconfig(r, fill=t["sel_hover_bg"],
                                           outline=t["sel_hover_outline"])
                    l.config(bg=t["sel_hover_bg"])

            def _leave(e, r=rect, l=lbl, act=activo):
                if not act:
                    self.canvas.itemconfig(r, fill=t["sel_normal_bg"],
                                           outline=t["sel_normal_outline"])
                    l.config(bg=t["sel_normal_bg"])

            lbl.bind("<Button-1>", _click)
            lbl.bind("<Enter>", _enter)
            lbl.bind("<Leave>", _leave)

            resultado[ident] = {"rect": rect, "label": lbl}
        return resultado

    # ------------------------------------------------------
    #  Construcción de la UI
    # ------------------------------------------------------
    def _construir_interfaz(self):
        if hasattr(self, "canvas") and self.canvas.winfo_exists():
            self.canvas.destroy()

        self.textos = {}
        self.btn_idioma = {}
        self.btn_estilo = {}
        self.btn_modo = {}
        self.url_widgets = {}

        t = self.tema
        W, H = self.W, self.H
        HEADER_H = self.HEADER_H

        self.canvas = tk.Canvas(self.root, width=W, height=H,
                                bg=t["fondo_top"],
                                highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)

        # Fondo
        if t["gradiente_fondo"]:
            self._gradient(0, 0, W, H, t["fondo_top"], t["fondo_bot"])
        else:
            self.canvas.create_rectangle(0, 0, W, H,
                                         fill=t["fondo_top"], outline="")

        # Cabecera
        if t["gradiente_header"]:
            self._gradient(0, 0, W, HEADER_H, t["header_top"], t["header_bot"])
        else:
            self.canvas.create_rectangle(0, 0, W, HEADER_H,
                                         fill=t["header_top"], outline="")
        for clave, y in (("header_top1", 1), ("header_top2", 2),
                         ("header_bot1", HEADER_H - 1),
                         ("header_bot2", HEADER_H)):
            if t[clave]:
                self.canvas.create_line(0, y, W, y, fill=t[clave], width=1)

        # Icono + título
        self.canvas.create_text(30, 34, text="🖥", anchor="w",
                                font=("Segoe UI Emoji", 22),
                                fill=t["titulo_fg"])
        self.canvas.create_text(72, 28, text="Server Maker", anchor="w",
                                font=("Segoe UI", 16, "bold"),
                                fill=t["titulo_fg"])
        self.textos["subtitulo"] = self.canvas.create_text(
            72, 56, text="", anchor="w",
            font=("Segoe UI", 9), fill=t["subtitulo_fg"]
        )

        # Selectores en cabecera
        self.btn_idioma = self._crear_selector(
            items=[("ES", "ES"), ("EN", "EN"), ("PT", "PT")],
            x_right=W - 30, y=16, w=38, h=24,
            callback=self._cambiar_idioma,
            es_activo=lambda c: c == self.idioma,
        )
        self.btn_estilo = self._crear_selector(
            items=[("AERO", "AERO"), ("MINIMAL", "MIN")],
            x_right=W - 30, y=48, w=65, h=24,
            callback=self._cambiar_estilo,
            es_activo=lambda c: c == self.estilo,
        )
        self.btn_modo = self._crear_selector(
            items=[("CLARO", "☀  CLARO"), ("OSCURO", "🌙  OSCURO")],
            x_right=W - 30, y=80, w=95, h=24,
            callback=self._cambiar_modo,
            es_activo=lambda c: c == self.modo,
        )

        # ---------------- Barra de URL ----------------
        y_url = HEADER_H + 14
        url_h = 46
        self._round_rect(30, y_url, W - 30, y_url + url_h, t["radius_small"],
                         fill=t["url_bg"], outline=t["url_border"], width=1)

        # Etiqueta superior
        self.textos["lbl_url"] = self.canvas.create_text(
            46, y_url - 2, text="", anchor="sw",
            font=("Segoe UI", 8, "bold"), fill=t["label_fg"]
        )

        # Icono 🔗
        icon = self.canvas.create_text(
            52, y_url + url_h / 2, text="🔗", anchor="w",
            font=("Segoe UI Emoji", 13), fill=t["url_icon_fg"]
        )
        # Base URL (fija)
        fnt_url = tkfont.Font(family="Segoe UI", size=11, weight="bold")
        x_base = 82
        base = self.canvas.create_text(
            x_base, y_url + url_h / 2, text=self.URL_BASE, anchor="w",
            font=fnt_url, fill=t["url_base_fg"]
        )
        ancho_base = fnt_url.measure(self.URL_BASE)

        # Carpeta (acento)
        fnt_carpeta = tkfont.Font(family="Segoe UI", size=11, weight="bold",
                                  underline=True)
        acc = self.canvas.create_text(
            x_base + ancho_base, y_url + url_h / 2, text="", anchor="w",
            font=fnt_carpeta, fill=t["url_accent_fg"]
        )
        # Hint 📋 a la derecha
        hint = self.canvas.create_text(
            W - 52, y_url + url_h / 2, text=self.T("url_copiar"), anchor="e",
            font=("Segoe UI Emoji", 12), fill=t["url_hint_fg"]
        )

        # Click para copiar
        for item in (icon, base, acc, hint):
            self.canvas.tag_bind(item, "<Button-1>", self._copiar_url)
        # Añadimos un rectángulo invisible de click-through ya cubierto por tag_bind
        self.canvas.tag_bind(self.canvas.find_all()[-1], "<Button-1>",
                             lambda e: None)

        self.url_widgets = {"icon": icon, "base": base, "accent": acc,
                            "hint": hint, "x_base": x_base,
                            "ancho_base": ancho_base,
                            "y": y_url + url_h / 2}

        # ---------------- Formulario ----------------
        y = y_url + url_h + 22
        self.textos["lbl_nombre"] = self._etiqueta(30, y, "")
        self.entry_nombre = self._entry_redondeado(
            30, y + 14, 470, 36, self.var_nombre)

        y += 72
        self.textos["lbl_carpeta"] = self._etiqueta(30, y, "")
        self.entry_carpeta = self._entry_redondeado(
            30, y + 14, 648, 36, self.var_carpeta)
        self.btn_elegir = AeroButton(
            self, W - 30 - 120, y + 14, 120, 36, self._elegir_carpeta,
            color=t["btn_elegir"], hover=t["btn_elegir_hover"],
            disabled_bg=t["btn_disabled_bg"], disabled_fg=t["btn_disabled_fg"],
            fuente=("Segoe UI", 9, "bold"), radius=t["radius_small"],
        )

        y += 72
        self.textos["lbl_host"] = self._etiqueta(30, y, "")
        self.entry_host = self._entry_redondeado(30, y + 14, 180, 36,
                                                  self.var_host)
        self.textos["lbl_puerto"] = self._etiqueta(230, y, "")
        self.entry_puerto = self._entry_redondeado(230, y + 14, 120, 36,
                                                    self.var_puerto)
        self.textos["lbl_ip"] = self.canvas.create_text(
            W - 30, y + 32, text="", anchor="e",
            font=("Segoe UI", 9), fill=t["label_fg"]
        )

        # ---------------- Botones principales ----------------
        y += 84
        self.btn_iniciar = AeroButton(
            self, 30, y, 175, 46, self.iniciar,
            color=t["btn_iniciar"], hover=t["btn_iniciar_hover"],
            disabled_bg=t["btn_disabled_bg"], disabled_fg=t["btn_disabled_fg"],
            radius=t["radius"],
        )
        self.btn_detener = AeroButton(
            self, 215, y, 145, 46, self.detener,
            color=t["btn_detener"], hover=t["btn_detener_hover"],
            disabled_bg=t["btn_disabled_bg"], disabled_fg=t["btn_disabled_fg"],
            radius=t["radius"],
        )
        self.btn_abrir = AeroButton(
            self, W - 30 - 210, y, 210, 46, self._abrir_navegador,
            color=t["btn_abrir"], hover=t["btn_abrir_hover"],
            disabled_bg=t["btn_disabled_bg"], disabled_fg=t["btn_disabled_fg"],
            radius=t["radius"],
        )

        # ---------------- Estado ----------------
        y += 62
        self.textos["lbl_estado"] = self.canvas.create_text(
            30, y, text="", anchor="w",
            font=("Segoe UI", 10, "bold"), fill=t["estado_detenido"]
        )

        # ---------------- Panel de log ----------------
        y += 24
        panel_h = H - y - 20
        self._round_rect(30, y, W - 30, y + panel_h, t["radius"],
                         fill=t["panel_bg"], outline=t["panel_border"], width=1)
        self.textos["lbl_log"] = self._etiqueta(46, y + 14, "")
        self.canvas.create_line(46, y + 26, W - 46, y + 26,
                                fill=t["log_sep"], width=1)

        self.txt_log = tk.Text(
            self.canvas, bd=0, bg=t["log_bg"], fg=t["log_fg"],
            font=("Consolas", 8), wrap="word", state="disabled",
            highlightthickness=0, relief="flat", padx=0, pady=0
        )
        self.canvas.create_window(46, y + 34, window=self.txt_log,
                                  anchor="nw",
                                  width=W - 92, height=panel_h - 44)

        if self.activo:
            self.btn_iniciar.set_habilitado(False)
            self.btn_detener.set_habilitado(True)

        self._refrescar_log()

    # ------------------------------------------------------
    #  Barra de URL dinámica
    # ------------------------------------------------------
    def _folder_slug(self):
        ruta = self.var_carpeta.get().strip()
        if not ruta:
            return "server"
        ruta = ruta.replace("\\", "/").rstrip("/")
        nombre = ruta.split("/")[-1] if ruta else "server"
        if not nombre:
            return "server"
        nombre = nombre.replace(" ", "_")
        limpio = "".join(c for c in nombre if c.isalnum() or c in "-_.")
        return limpio or "server"

    def _url_compartida(self):
        return self.URL_BASE + self._folder_slug()

    def _actualizar_url_bar(self):
        if not self.url_widgets:
            return
        try:
            self.canvas.itemconfig(self.url_widgets["accent"],
                                   text=self._folder_slug())
        except tk.TclError:
            pass

    def _copiar_url(self, _event=None):
        url = self._url_compartida()
        self.root.clipboard_clear()
        self.root.clipboard_append(url)
        # Feedback visual
        try:
            self.canvas.itemconfig(self.url_widgets["hint"],
                                   text=self.T("url_copiado"))
        except tk.TclError:
            return
        if self._reset_url_timer is not None:
            self.root.after_cancel(self._reset_url_timer)
        self._reset_url_timer = self.root.after(1600, self._reset_url_hint)

    def _reset_url_hint(self):
        self._reset_url_timer = None
        try:
            self.canvas.itemconfig(self.url_widgets["hint"],
                                   text=self.T("url_copiar"))
        except tk.TclError:
            pass

    # ------------------------------------------------------
    #  Cambios de preferencias
    # ------------------------------------------------------
    def _cambiar_idioma(self, cod):
        if cod == self.idioma:
            return
        self.idioma = cod
        self._aplicar_idioma()
        self._log(self.T("log_lang"))

    def _cambiar_estilo(self, cod):
        if cod == self.estilo:
            return
        self.estilo = cod
        self._reconstruir_y_refrescar()
        nombre = "Aero" if cod == "AERO" else "Minimal"
        self._log(self.T("log_estilo", estilo=nombre))

    def _cambiar_modo(self, cod):
        if cod == self.modo:
            return
        self.modo = cod
        self._reconstruir_y_refrescar()
        nombre = self.T("modo_claro") if cod == "CLARO" else self.T("modo_oscuro")
        self._log(self.T("log_modo", modo=nombre))

    def _reconstruir_y_refrescar(self):
        self._construir_interfaz()
        self._aplicar_idioma()
        self._actualizar_nombre()
        self._actualizar_url_bar()

    # ------------------------------------------------------
    def _actualizar_nombre(self):
        nombre = self.var_nombre.get().strip() or self.T("nombre_defecto")
        self.root.title(f"Server Maker · {nombre}")
        if "subtitulo" in self.textos:
            self.canvas.itemconfig(
                self.textos["subtitulo"],
                text=f"{self.T('subtitulo')}   ·   {nombre}"
            )

    def _aplicar_idioma(self):
        self.canvas.itemconfig(self.textos["lbl_nombre"],
                               text=self.T("lbl_nombre"))
        self.canvas.itemconfig(self.textos["lbl_carpeta"],
                               text=self.T("lbl_carpeta"))
        self.canvas.itemconfig(self.textos["lbl_host"],
                               text=self.T("lbl_host"))
        self.canvas.itemconfig(self.textos["lbl_puerto"],
                               text=self.T("lbl_puerto"))
        self.canvas.itemconfig(self.textos["lbl_url"],
                               text=self.T("lbl_url"))
        self.canvas.itemconfig(self.textos["lbl_ip"],
                               text=f"{self.T('ip_local')} {obtener_ip_local()}")
        self.canvas.itemconfig(self.textos["lbl_log"],
                               text=self.T("log_titulo"))

        self.btn_elegir.config_texto(self.T("btn_elegir"))
        self.btn_iniciar.config_texto(self.T("btn_iniciar"))
        self.btn_detener.config_texto(self.T("btn_detener"))
        self.btn_abrir.config_texto(self.T("btn_abrir"))

        # Refrescar textos de botones de modo
        try:
            self.btn_modo["CLARO"]["label"].config(text=f"☀  {self.T('modo_claro').upper()}")
            self.btn_modo["OSCURO"]["label"].config(text=f"🌙  {self.T('modo_oscuro').upper()}")
        except KeyError:
            pass

        # Resetear hint de URL
        if "hint" in self.url_widgets:
            try:
                self.canvas.itemconfig(self.url_widgets["hint"],
                                       text=self.T("url_copiar"))
            except tk.TclError:
                pass

        self._set_estado_visual()

    def _set_estado_visual(self):
        t = self.tema
        if self.activo and self.ultimo_puerto:
            texto = self.T("estado_activo",
                           ip=obtener_ip_local(), puerto=self.ultimo_puerto)
            color = t["estado_activo"]
        else:
            texto = self.T("estado_detenido")
            color = t["estado_detenido"]
        self.canvas.itemconfig(self.textos["lbl_estado"],
                               text=texto, fill=color)

    # ------------------------------------------------------
    #  Acciones
    # ------------------------------------------------------
    def _elegir_carpeta(self):
        carpeta = filedialog.askdirectory(
            initialdir=self.var_carpeta.get() or os.getcwd()
        )
        if carpeta:
            self.var_carpeta.set(carpeta)

    def _abrir_navegador(self):
        try:
            puerto = int(self.var_puerto.get())
        except ValueError:
            messagebox.showerror(self.T("err_titulo"),
                                 self.T("err_puerto_inv"))
            return
        webbrowser.open(f"http://127.0.0.1:{puerto}/")

    # ------------------------------------------------------
    #  Log
    # ------------------------------------------------------
    def _log_seguro(self, mensaje):
        self.root.after(0, self._log, mensaje)

    def _log(self, mensaje):
        hora = datetime.now().strftime("%H:%M:%S")
        self.log_historial.append(f"[{hora}] {mensaje}")
        if len(self.log_historial) > 500:
            self.log_historial = self.log_historial[-500:]
        self._refrescar_log()

    def _refrescar_log(self):
        if not hasattr(self, "txt_log") or not self.txt_log.winfo_exists():
            return
        self.txt_log.configure(state="normal")
        self.txt_log.delete("1.0", "end")
        if self.log_historial:
            self.txt_log.insert("end", "\n".join(self.log_historial) + "\n")
        self.txt_log.see("end")
        self.txt_log.configure(state="disabled")

    # ------------------------------------------------------
    #  Control del servidor
    # ------------------------------------------------------
    def iniciar(self):
        if self.activo:
            return

        carpeta = self.var_carpeta.get().strip()
        if not os.path.isdir(carpeta):
            messagebox.showerror(self.T("err_titulo"), self.T("err_carpeta"))
            return

        try:
            puerto = int(self.var_puerto.get())
            if not (1 <= puerto <= 65535):
                raise ValueError
        except ValueError:
            messagebox.showerror(self.T("err_titulo"), self.T("err_puerto"))
            return

        host = self.var_host.get().strip() or "0.0.0.0"
        nombre = self.var_nombre.get().strip() or self.T("nombre_defecto")

        manejador = partial(
            Manejador, directory=carpeta,
            log_callback=self._log_seguro, server_nombre=nombre,
        )

        try:
            self.servidor = ServidorLigero((host, puerto), manejador)
        except OSError as e:
            messagebox.showerror(
                self.T("err_puerto_tit"),
                self.T("err_puerto_msg", host=host, puerto=puerto, e=e)
            )
            return

        self.hilo = threading.Thread(target=self.servidor.serve_forever,
                                     daemon=True)
        self.hilo.start()
        self.activo = True
        self.ultimo_puerto = puerto

        self.btn_iniciar.set_habilitado(False)
        self.btn_detener.set_habilitado(True)
        self._set_estado_visual()

        self._log(self.T("log_iniciado",
                         nombre=nombre, host=host, puerto=puerto))
        self._log(self.T("log_raiz", carpeta=carpeta))
        self._log(self.T("log_pista"))

    def detener(self):
        if not self.activo or self.servidor is None:
            return
        try:
            self.servidor.shutdown()
            self.servidor.server_close()
        except Exception as e:
            self._log(self.T("log_aviso", e=e))
        finally:
            self.servidor = None
            self.hilo = None
            self.activo = False
            self.ultimo_puerto = None

        self.btn_iniciar.set_habilitado(True)
        self.btn_detener.set_habilitado(False)
        self._set_estado_visual()
        self._log(self.T("log_detenido"))

    def cerrar(self):
        if self.activo:
            self.detener()
        self.root.destroy()


# ==========================================================
#  MAIN
# ==========================================================
def main():
    root = tk.Tk()
    app = ServerMakerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.cerrar)
    root.mainloop()


if __name__ == "__main__":
    main()
