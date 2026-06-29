"""
    .SYNOPSIS
        Overlay window used to define the sharing region.
    
    .DESCRIPTION
        Implements a transparent always-on-top frame that marks the screen area to
        share. The frame can be moved and resized.
        
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
        
        # Initial geometry
        self.geometry("800x600+100+100")
        
        # Remove native borders for a custom frame.
        self.overrideredirect(True)
        
        # Chroma key transparency color. Use a near-black color to avoid conflicts
        # with true black UI elements.
        self.transparent_color = "#000001" 
        self.config(bg=self.transparent_color)
        self.attributes("-transparentcolor", self.transparent_color)
        self.attributes("-topmost", True)
        
        # Visible border frame
        self.border_color = "#00E5FF"
        self.border_width = 4
        
        # The outer frame creates the visible border. The inner frame is transparent.
        self.main_frame = ctk.CTkFrame(self, fg_color=self.border_color, corner_radius=0, border_width=0)
        self.main_frame.pack(fill="both", expand=True)
        
        self.inner_frame = ctk.CTkFrame(self.main_frame, fg_color=self.transparent_color, corner_radius=0)
        self.inner_frame.pack(fill="both", expand=True, padx=self.border_width, pady=self.border_width)
        
        # Header / drag handle
        self.header_height = 30
        self.header = ctk.CTkFrame(self.inner_frame, 
                                   fg_color=self.border_color, 
                                   height=self.header_height, 
                                   corner_radius=0)
        self.header.pack(side="top", fill="x")
        
        self.label_title = ctk.CTkLabel(self.header, text="UltraShare Region", text_color="#000000", font=("Roboto", 12, "bold"))
        self.label_title.place(relx=0.5, rely=0.5, anchor="center")
        
        # Drag events
        self.header.bind("<ButtonPress-1>", self.start_move)
        self.header.bind("<B1-Motion>", self.do_move)
        self.label_title.bind("<ButtonPress-1>", self.start_move)
        self.label_title.bind("<B1-Motion>", self.do_move)
        
        # Resize grip in the bottom-right corner
        self.grip_size = 20
        self.resize_grip = ctk.CTkFrame(self.inner_frame, 
                                        width=self.grip_size, 
                                        height=self.grip_size, 
                                        fg_color=self.border_color, 
                                        corner_radius=2)
        self.resize_grip.place(relx=1.0, rely=1.0, anchor="se")
        self.resize_grip.bind("<ButtonPress-1>", self.start_resize)
        self.resize_grip.bind("<B1-Motion>", self.do_resize)
        
        # Drag state
        self.x = 0
        self.y = 0
        
        # Currently attached target window
        self.attached_hwnd = None
        
    def start_move(self, event):
        self.x = event.x
        self.y = event.y
        
        # Validate whether the attached window is still aligned with the region.
        if self.attached_hwnd and self.master and hasattr(self.master, 'wm'):
            cx, cy, cw, ch = self.get_region_geometry()
            
            win_rect = self.master.wm.get_window_rect(self.attached_hwnd)
            
            if win_rect:
                wx, wy, ww, wh = win_rect
                
                tolerance = 20
                
                if abs(wx - cx) > tolerance or abs(wy - cy) > tolerance:
                    print("Window detached after external manual movement.")
                    self.attached_hwnd = None
            else:
                self.attached_hwnd = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")
        
        # Keep the attached target window aligned while moving the overlay.
        if self.attached_hwnd and self.master and hasattr(self.master, 'wm'):
            content_x = x + self.border_width
            content_y = y + self.border_width + self.header_height
            content_w = self.winfo_width() - (self.border_width * 2)
            content_h = self.winfo_height() - (self.border_width * 2) - self.header_height
            
            self.master.wm.set_window_pos(self.attached_hwnd, content_x, content_y, content_w, content_h)

    def start_resize(self, event):
        self.x = event.x
        self.y = event.y
        
    def do_resize(self, event):
        # Calculate new geometry.
        
        current_width = self.winfo_width()
        current_height = self.winfo_height()
        
        # The event comes from the resize grip.
        dx = event.x - self.x 
        dy = event.y - self.y
        
        new_width = current_width + dx
        new_height = current_height + dy
        
        if new_width > 100 and new_height > 100:
            self.geometry(f"{new_width}x{new_height}")

    def get_region_geometry(self):
        """Return global (x, y, width, height) for the transparent content region."""
        win_x = self.winfo_x()
        win_y = self.winfo_y()
        
        content_x = win_x + self.border_width
        content_y = win_y + self.border_width + self.header_height
        content_w = self.winfo_width() - (self.border_width * 2)
        content_h = self.winfo_height() - (self.border_width * 2) - self.header_height
        
        return (content_x, content_y, content_w, content_h)

    def set_size(self, w, h):
        self.geometry(f"{w}x{h}")
