"""
    .SYNOPSIS
        Gestor de ventanas para UltraShare.
    
    .DESCRIPTION
        Este módulo, escrito en Python, se encarga de la interacción a bajo nivel con la API de Windows
        para enumerar, mover, redimensionar y gestionar las ventanas del escritorio.
        
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
    Clase encargada de gestionar las ventanas del sistema operativo Windows.
    Permite enumerar ventanas visibles, obtener la ventana activa y redimensionarlas.
    """

    def __init__(self):
        self.user32 = ctypes.windll.user32
        self.user32.SetProcessDPIAware() # Asegurar que somos DPI-Aware para coordenadas correctas

    def get_open_windows(self):
        """
        Devuelve una lista de tuplas (hwnd, título) de todas las ventanas visibles y con título.
        """
        windows = []

        def enum_handler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title:
                    # Filtros opcionales: Evitar Program Manager, etc.
                    if title != "Program Manager": 
                        windows.append((hwnd, title))
        
        win32gui.EnumWindows(enum_handler, None)
        return windows

    def get_active_window(self):
        """
        Devuelve el handler (hwnd) y el título de la ventana actualmente activa (en foco).
        """
        hwnd = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(hwnd)
        return hwnd, title

    def set_window_pos(self, hwnd, x, y, width, height):
        """
        Mueve y redimensiona una ventana especificada por su hwnd.
        
        Args:
            hwnd: Handle de la ventana.
            x (int): Posición X absoluta.
            y (int): Posición Y absoluta.
            width (int): Ancho deseado.
            height (int): Alto deseado.
        """
        try:
            # Flags: SWP_NOZORDER (no cambiar orden Z), SWP_SHOWWINDOW (asegurar que se muestre)
            # SWP_NOACTIVATE podría ser útil si no queremos robar el foco, pero generalmente queremos verla.
            flags = win32con.SWP_NOZORDER | win32con.SWP_SHOWWINDOW
            
            # Restaurar si está minimizada antes de mover
            if win32gui.IsIconic(hwnd):
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

            win32gui.SetWindowPos(hwnd, 0, x, y, width, height, flags)
            return True
        except Exception as e:
            print(f"Error al mover la ventana {hwnd}: {e}")
            return False

    def bring_to_front(self, hwnd):
        """Trae la ventana al frente."""
        try:
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
        except Exception:
            pass

    def get_window_rect(self, hwnd):
        """Devuelve (x, y, width, height) de la ventana."""
        try:
            rect = win32gui.GetWindowRect(hwnd)
            x = rect[0]
            y = rect[1]
            w = rect[2] - x
            h = rect[3] - y
            return x, y, w, h
        except Exception:
            return None
