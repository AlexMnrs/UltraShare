"""
    .SYNOPSIS
        Panel de control principal de UltraShare.
    
    .DESCRIPTION
        Interfaz gráfica para configurar el comportamiento del overlay y realizar acciones
        como ajustar ventanas (Snapping) o cambiar la resolución.
        
    .NOTES
        File Name:  control_panel.py
        Author:     Alex Monrás
        Created:    2026-01-22
        Version:    1.0.0
"""

import customtkinter as ctk

class ControlPanel(ctk.CTk):
    def __init__(self, window_manager, overlay_window):
        super().__init__()
        
        self.wm = window_manager
        self.overlay = overlay_window
        
        self.title("UltraShare Control")
        self.geometry("400x550")
        self.resizable(False, False)
        
        # Grid Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=0) # Filas fijas
        
        # Header
        self.frame_header = ctk.CTkFrame(self, corner_radius=10)
        self.frame_header.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        self.lbl_title = ctk.CTkLabel(self.frame_header, text="UltraShare", font=("Outfit", 24, "bold"))
        self.lbl_title.pack(pady=10)
        self.lbl_subtitle = ctk.CTkLabel(self.frame_header, text="Ultra-Wide Screen Sharing Tool", text_color="gray")
        self.lbl_subtitle.pack(pady=(0, 10))

        # Sección de Tamaños
        self.frame_sizes = ctk.CTkFrame(self)
        self.frame_sizes.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.lbl_res = ctk.CTkLabel(self.frame_sizes, text="Resolución Objetivo:", font=("Roboto", 14, "bold"))
        self.lbl_res.pack(pady=10, padx=10, anchor="w")
        
        self.sizes = {
            "Teams Optimized (1280x720)": (1280, 720),
            "Full HD (1920x1080)": (1920, 1080),
            "Compact (800x600)": (800, 600)
        }
        
        self.combo_sizes = ctk.CTkComboBox(self.frame_sizes, values=list(self.sizes.keys()), command=self.on_size_change)
        self.combo_sizes.set("Teams Optimized (1280x720)")
        self.combo_sizes.pack(pady=10, padx=10, fill="x")
        
        # Sección de Snapping
        self.frame_snap = ctk.CTkFrame(self)
        self.frame_snap.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        self.lbl_snap = ctk.CTkLabel(self.frame_snap, text="Ajustar Ventana (Smart Snap):", font=("Roboto", 14, "bold"))
        self.lbl_snap.pack(pady=10, padx=10, anchor="w")
        
        self.btn_refresh = ctk.CTkButton(self.frame_snap, text="🔄 Refrescar Lista", command=self.refresh_windows)
        self.btn_refresh.pack(pady=(0, 10), padx=10, fill="x")
        
        self.combo_windows = ctk.CTkComboBox(self.frame_snap, values=[])
        self.combo_windows.pack(pady=10, padx=10, fill="x")
        
        self.btn_snap = ctk.CTkButton(self.frame_snap, text="SNAP! (Ajustar)", fg_color="#00E5FF", text_color="black", hover_color="#00B8D4", command=self.snap_window)
        self.btn_snap.pack(pady=10, padx=10, fill="x")

        # Footer / Info
        self.lbl_status = ctk.CTkLabel(self, text="Ready", text_color="gray")
        self.lbl_status.grid(row=3, column=0, pady=20)
        
        # Inicializar
        self.refresh_windows()

    def on_size_change(self, choice):
        w, h = self.sizes[choice]
        # Ajustamos el tamaño del overlay. 
        # IMPORTANTE: El overlay tiene bordes, set_size debería manejar el tamaño EXTERNO o INTERNO?
        # En overlay_window.py set_size usa geometry, que es externo.
        # Vamos a sumar los bordes para que el AREA UTIL sea w, h
        
        # Borde width * 2 (+ pad), Header height
        # overlay.border_width = 4
        # overlay.header_height = 30
        
        bv = self.overlay.border_width
        hh = self.overlay.header_height
        
        total_w = w + (bv * 2) 
        total_h = h + (bv * 2) + hh 
        
        self.overlay.set_size(total_w, total_h)
        self.lbl_status.configure(text=f"Región: {w}x{h}")

    def refresh_windows(self):
        windows = self.wm.get_open_windows()
        # Guardamos la lista completa para referencia
        self.current_windows = windows
        titles = [title for hwnd, title in windows]
        self.combo_windows.configure(values=titles)
        if titles:
            self.combo_windows.set(titles[0])
            
    def snap_window(self):
        selection = self.combo_windows.get()
        target_hwnd = None
        for hwnd, title in self.current_windows:
            if title == selection:
                target_hwnd = hwnd
                break
        
        if target_hwnd:
            self.wm.bring_to_front(target_hwnd)
            
            # Obtener geometría de la región útil
            ox, oy, ow, oh = self.overlay.get_region_geometry()
            
            # Ajustar ventana
            success = self.wm.set_window_pos(target_hwnd, ox, oy, ow, oh)
            if success:
                self.overlay.attached_hwnd = target_hwnd
                self.lbl_status.configure(text=f"Ajustado: {selection[:20]}...")
            else:
                self.lbl_status.configure(text="Error al ajustar")
