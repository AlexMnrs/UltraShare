# Progreso del Proyecto UltraShare

- [x] **Inicialización**
    - [x] Estructura del proyecto completada (`core`, `ui`).
    - [x] Dependencias instaladas (`customtkinter`, `pywin32`, etc).
- [x] **Core (Backend)**
    - [x] `WindowManager`: Enumeración y manejo de ventanas (Win32 API).
- [x] **UI (Frontend)**
    - [x] `OverlayWindow`: Marco transparente y redimensionable ("Always on Top").
    - [x] `ControlPanel`: Selector de resolución y herramienta de Snapping.
- [x] **Características**
    - [x] **Smart Snap**: Ajuste automático de ventanas a la región.
    - [x] **Smart Move**: Sincronización de movimiento overlay-ventana.
    - [x] **Auto Unsnap**: Desvinculación automática si la ventana se mueve externamente.
    - [x] **Presets**: Tamaños optimizados para Teams/FullHD.
- [x] **Empaquetado**
    - [x] Generar ejecutable con PyInstaller.
- [ ] **Empaquetado Avanzado** (Opcional)
    - [ ] Crear instalador .msi o setup.exe
    - [ ] Icono personalizado
