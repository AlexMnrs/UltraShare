"""
    .SYNOPSIS
        Punto de entrada principal de UltraShare.
    
    .DESCRIPTION
        Inicializa la aplicación, el gestor de ventanas y las interfaces gráficas.
        
    .NOTES
        File Name:  main.py
        Author:     Alex Monrás
        Created:    2026-01-22
        Version:    1.0.0
"""

import customtkinter as ctk
from core.window_manager import WindowManager
from ui.control_panel import ControlPanel
from ui.overlay_window import OverlayWindow
import sys

# Configuración Global de Tema
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def main():
    print("Iniciando UltraShare...")
    
    # 1. Inicializar Core
    wm = WindowManager()
    
    # 2. Inicializar UI Principal (Control Panel es el Root)
    # Pasamos None al overlay inicialmente para romper dependencia circular
    app = ControlPanel(window_manager=wm, overlay_window=None)
    
    # 3. Inicializar Overlay (Toplevel dependiente de App)
    overlay = OverlayWindow(app)
    
    # 4. Inyección de dependencia cruzada
    app.overlay = overlay
    
    # Posicionar overlay por defecto si es necesario (on_size_change no se llama auto)
    # Forzamos un update inicial
    initial_size = "Teams Optimized (1280x720)"
    app.combo_sizes.set(initial_size)
    app.on_size_change(initial_size)
    
    # 5. Ejecutar Loop
    app.mainloop()

if __name__ == "__main__":
    main()
