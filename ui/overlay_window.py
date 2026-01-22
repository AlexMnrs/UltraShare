"""
    .SYNOPSIS
        Ventana de superposición (Overlay) para definir la región de compartición.
    
    .DESCRIPTION
        Implementa una ventana semitransparente (o con color key) que marca el área
        de la pantalla que se va a compartir. Permite redimensionar y arrastrar.
        
    .NOTES
        File Name:  overlay_window.py
        Author:     Alex Monrás
        Created:    2026-01-22
        Version:    1.0.0
"""

import customtkinter as ctk
import tkinter as tk
import ctypes
import win32gui
import win32con

class OverlayWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title("UltraShare Overlay")
        
        # Configuración inicial de geometría
        self.geometry("800x600+100+100")
        
        # Quitar bordes nativos para look custom
        self.overrideredirect(True)
        
        # Color para transparencia (Chroma Key)
        # Usamos un color muy oscuro pero no negro absoluto para evitar conflictos
        self.transparent_color = "#000001" 
        self.config(bg=self.transparent_color)
        self.attributes("-transparentcolor", self.transparent_color)
        self.attributes("-topmost", True)
        
        # Frame Borde (El contenedor visual)
        self.border_color = "#00E5FF" # Cyan eléctrico
        self.border_width = 4
        
        # Este frame actúa como el borde visible.
        # Dentro pondremos otro frame que sea el "agujero" transparente.
        self.main_frame = ctk.CTkFrame(self, fg_color=self.border_color, corner_radius=0, border_width=0)
        self.main_frame.pack(fill="both", expand=True)
        
        # El "agujero"
        self.inner_frame = ctk.CTkFrame(self.main_frame, fg_color=self.transparent_color, corner_radius=0)
        self.inner_frame.pack(fill="both", expand=True, padx=self.border_width, pady=self.border_width)
        
        # Header / Grip para mover la ventana
        self.header_height = 30
        self.header = ctk.CTkFrame(self.inner_frame, 
                                   fg_color=self.border_color, 
                                   height=self.header_height, 
                                   corner_radius=0)
        self.header.pack(side="top", fill="x")
        
        self.label_title = ctk.CTkLabel(self.header, text="UltraShare Region", text_color="#000000", font=("Roboto", 12, "bold"))
        self.label_title.place(relx=0.5, rely=0.5, anchor="center")
        
        # Grip Events
        self.header.bind("<ButtonPress-1>", self.start_move)
        self.header.bind("<B1-Motion>", self.do_move)
        self.label_title.bind("<ButtonPress-1>", self.start_move)
        self.label_title.bind("<B1-Motion>", self.do_move)
        
        # Resize Grip (Esquina inferior derecha)
        self.grip_size = 20
        self.resize_grip = ctk.CTkFrame(self.inner_frame, 
                                        width=self.grip_size, 
                                        height=self.grip_size, 
                                        fg_color=self.border_color, 
                                        corner_radius=2)
        self.resize_grip.place(relx=1.0, rely=1.0, anchor="se")
        self.resize_grip.bind("<ButtonPress-1>", self.start_resize)
        self.resize_grip.bind("<B1-Motion>", self.do_resize)
        
        # Variables de estado para Drag & Drop
        self.x = 0
        self.y = 0
        
        # Referencia a la ventana capturada
        self.attached_hwnd = None
        
    def start_move(self, event):
        self.x = event.x
        self.y = event.y
        
        # Validar si la ventana adjunta sigue estando sincronizada
        if self.attached_hwnd and self.master and hasattr(self.master, 'wm'):
            # Geometría actual esperada del contenido
            cx, cy, cw, ch = self.get_region_geometry()
            
            # Geometría real de la ventana
            win_rect = self.master.wm.get_window_rect(self.attached_hwnd)
            
            if win_rect:
                wx, wy, ww, wh = win_rect
                
                # Tolerancia en píxeles (ej. 20px)
                tolerance = 20
                
                # Comprobar si hay divergencia significativa en posición
                if abs(wx - cx) > tolerance or abs(wy - cy) > tolerance:
                    print("Ventana desvinculada por movimiento manual externo.")
                    self.attached_hwnd = None
            else:
                # La ventana quizás se cerró
                self.attached_hwnd = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")
        
        # Sincronizar movimiento de ventana adjunta
        if self.attached_hwnd and self.master and hasattr(self.master, 'wm'):
            # Recalcular nuevas coordenadas absolutas de la región de contenido
            content_x = x + self.border_width
            content_y = y + self.border_width + self.header_height
            # Reutilizar el ancho/alto actuales
            content_w = self.winfo_width() - (self.border_width * 2)
            content_h = self.winfo_height() - (self.border_width * 2) - self.header_height
            
            self.master.wm.set_window_pos(self.attached_hwnd, content_x, content_y, content_w, content_h)

    def start_resize(self, event):
        self.x = event.x
        self.y = event.y
        
    def do_resize(self, event):
        # Calcular nueva geometría
        # event.x es relativo al widget grip, hay que tener cuidado.
        # Mejor usar winfo_pointerx
        
        current_width = self.winfo_width()
        current_height = self.winfo_height()
        
        # Simplificación: usar el delta del mouse
        # Al ser un grip interno, es un poco trick.
        # Vamos a usar coordenadas globales para ser más robustos en resize.
        pass # Implementación en siguiente iteración si es complejo, 
             # pero intentemos simple:
             
        # El evento viene del grip.
        dx = event.x - self.x 
        dy = event.y - self.y
        
        new_width = current_width + dx
        new_height = current_height + dy
        
        if new_width > 100 and new_height > 100:
            self.geometry(f"{new_width}x{new_height}")

    def get_region_geometry(self):
        """Retorna (x, y, width, height) globales de la zona transparente (inner content)."""
        # Ajustamos por el borde y el header
        # x, y son top-left de la ventana
        win_x = self.winfo_x()
        win_y = self.winfo_y()
        
        # El contenido útil empieza después del borde y el header?
        # En mi diseño el header está DENTRO del inner_frame arriba.
        # El área "compartible" sería debajo del header.
        
        content_x = win_x + self.border_width
        content_y = win_y + self.border_width + self.header_height
        content_w = self.winfo_width() - (self.border_width * 2)
        content_h = self.winfo_height() - (self.border_width * 2) - self.header_height
        
        return (content_x, content_y, content_w, content_h)

    def set_size(self, w, h):
        self.geometry(f"{w}x{h}")
