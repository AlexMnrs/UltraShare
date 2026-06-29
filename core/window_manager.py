"""
    .SYNOPSIS
        Window manager for UltraShare.
    
    .DESCRIPTION
        Handles low-level Windows API interaction for listing, moving, resizing,
        and managing desktop windows.
        
    .NOTES
        File Name:  window_manager.py
        Author:     Alex Monrás
        Created:    2026-01-22
        Version:    1.0.0
"""

import win32gui
import win32con
import ctypes
from ctypes import wintypes
import platform

class WindowManager:
    """
    Manages visible Windows desktop windows and exposes helper methods for
    positioning selected windows inside the UltraShare overlay region.
    """

    def __init__(self):
        self.user32 = ctypes.windll.user32
        self.user32.SetProcessDPIAware()

    def get_open_windows(self):
        """
        Return a list of (hwnd, title) tuples for visible windows with a title.
        """
        windows = []

        def enum_handler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title:
                    if title != "Program Manager": 
                        windows.append((hwnd, title))
        
        win32gui.EnumWindows(enum_handler, None)
        return windows

    def get_active_window(self):
        """
        Return the hwnd and title for the currently focused window.
        """
        hwnd = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(hwnd)
        return hwnd, title

    def set_window_pos(self, hwnd, x, y, width, height):
        """
        Move and resize a window by hwnd.
        
        Args:
            hwnd: Window handle.
            x (int): Absolute X position.
            y (int): Absolute Y position.
            width (int): Target width.
            height (int): Target height.
        """
        try:
            flags = win32con.SWP_NOZORDER | win32con.SWP_SHOWWINDOW
            
            if win32gui.IsIconic(hwnd):
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

            win32gui.SetWindowPos(hwnd, 0, x, y, width, height, flags)
            return True
        except Exception as e:
            print(f"Error moving window {hwnd}: {e}")
            return False

    def bring_to_front(self, hwnd):
        """Bring a window to the foreground."""
        try:
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
        except Exception:
            pass

    def get_window_rect(self, hwnd):
        """Return (x, y, width, height) for a window."""
        try:
            rect = win32gui.GetWindowRect(hwnd)
            x = rect[0]
            y = rect[1]
            w = rect[2] - x
            h = rect[3] - y
            return x, y, w, h
        except Exception:
            return None
