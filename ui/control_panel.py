"""
    .SYNOPSIS
        Main UltraShare control panel.
    
    .DESCRIPTION
        Graphical interface for configuring the overlay and snapping windows into
        the selected sharing region.
        
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
        
        # Grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=0)
        
        # Header
        self.frame_header = ctk.CTkFrame(self, corner_radius=10)
        self.frame_header.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        self.lbl_title = ctk.CTkLabel(self.frame_header, text="UltraShare", font=("Outfit", 24, "bold"))
        self.lbl_title.pack(pady=10)
        self.lbl_subtitle = ctk.CTkLabel(self.frame_header, text="Ultrawide screen sharing helper", text_color="gray")
        self.lbl_subtitle.pack(pady=(0, 10))

        # Target size section
        self.frame_sizes = ctk.CTkFrame(self)
        self.frame_sizes.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.lbl_res = ctk.CTkLabel(self.frame_sizes, text="Target resolution:", font=("Roboto", 14, "bold"))
        self.lbl_res.pack(pady=10, padx=10, anchor="w")
        
        self.sizes = {
            "Teams Optimized (1280x720)": (1280, 720),
            "Full HD (1920x1080)": (1920, 1080),
            "Compact (800x600)": (800, 600)
        }
        
        self.combo_sizes = ctk.CTkComboBox(self.frame_sizes, values=list(self.sizes.keys()), command=self.on_size_change)
        self.combo_sizes.set("Teams Optimized (1280x720)")
        self.combo_sizes.pack(pady=10, padx=10, fill="x")
        
        # Snapping section
        self.frame_snap = ctk.CTkFrame(self)
        self.frame_snap.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        self.lbl_snap = ctk.CTkLabel(self.frame_snap, text="Smart Snap window:", font=("Roboto", 14, "bold"))
        self.lbl_snap.pack(pady=10, padx=10, anchor="w")
        
        self.btn_refresh = ctk.CTkButton(self.frame_snap, text="Refresh window list", command=self.refresh_windows)
        self.btn_refresh.pack(pady=(0, 10), padx=10, fill="x")
        
        self.combo_windows = ctk.CTkComboBox(self.frame_snap, values=[])
        self.combo_windows.pack(pady=10, padx=10, fill="x")
        
        self.btn_snap = ctk.CTkButton(self.frame_snap, text="Snap selected window", fg_color="#00E5FF", text_color="black", hover_color="#00B8D4", command=self.snap_window)
        self.btn_snap.pack(pady=10, padx=10, fill="x")

        # Footer / status
        self.lbl_status = ctk.CTkLabel(self, text="Ready", text_color="gray")
        self.lbl_status.grid(row=3, column=0, pady=20)
        
        self.refresh_windows()

    def on_size_change(self, choice):
        w, h = self.sizes[choice]
        # set_size applies the external window size, so include border and header
        # dimensions to keep the usable sharing area at the selected resolution.
        
        # Border width * 2 (+ pad), header height
        # overlay.border_width = 4
        # overlay.header_height = 30
        
        bv = self.overlay.border_width
        hh = self.overlay.header_height
        
        total_w = w + (bv * 2) 
        total_h = h + (bv * 2) + hh 
        
        self.overlay.set_size(total_w, total_h)
        self.lbl_status.configure(text=f"Region: {w}x{h}")

    def refresh_windows(self):
        windows = self.wm.get_open_windows()
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
            
            ox, oy, ow, oh = self.overlay.get_region_geometry()
            
            success = self.wm.set_window_pos(target_hwnd, ox, oy, ow, oh)
            if success:
                self.overlay.attached_hwnd = target_hwnd
                self.lbl_status.configure(text=f"Snapped: {selection[:20]}...")
            else:
                self.lbl_status.configure(text="Snap failed")
