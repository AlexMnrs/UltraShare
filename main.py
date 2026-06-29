"""
    .SYNOPSIS
        Main entry point for UltraShare.
    
    .DESCRIPTION
        Initializes the application, the window manager, and the graphical interfaces.
        
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

# Global theme settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def main():
    print("Starting UltraShare...")
    
    # 1. Initialize core services
    wm = WindowManager()
    
    # 2. Initialize the main UI. ControlPanel is the root window.
    # Pass None at first to avoid a circular dependency during construction.
    app = ControlPanel(window_manager=wm, overlay_window=None)
    
    # 3. Initialize the overlay as a top-level window owned by the app.
    overlay = OverlayWindow(app)
    
    # 4. Complete the cross-reference between both windows.
    app.overlay = overlay
    
    # Apply the default overlay size because the combo box callback is not fired automatically.
    initial_size = "Teams Optimized (1280x720)"
    app.combo_sizes.set(initial_size)
    app.on_size_change(initial_size)
    
    # 5. Start the UI loop.
    app.mainloop()

if __name__ == "__main__":
    main()
