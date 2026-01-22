# 📺 UltraShare

**Comparte pantalla de forma profesional en monitores Ultra-Wide.**

UltraShare soluciona el problema de los bordes negros y la visualización pequeña al compartir pantalla desde monitores 21:9 o 32:9. Crea una región virtual (overlay) de tamaño estándar (1080p, 720p) y permite "encajar" ventanas automáticamente dentro de ella para que tus espectadores vean exactamente lo que quieres, a pantalla completa y sin distracciones.

Ideal para:
- 🎥 Presentaciones en Microsoft Teams, Zoom o Google Meet sin bordes negros.
- 🖥️ Usuarios con monitores Ultrawide que quieren cuidar la experiencia del espectador.
- 🚀 Grabación de tutoriales o demos en resolución estándar.

---

## ✨ Características

- 🎯 **Región Persistente**: Marco visual "Always on Top" que delimita tu área de transmisión.
- 🧲 **Smart Snap**: Ajusta cualquier ventana al tamaño exacto de la región con un solo clic.
- 🔗 **Smart Move**: Al mover el marco, la ventana ajustada se mueve con él automáticamente como si estuviera pegada.
- 🛡️ **Auto Desvinculación**: Si mueves manualmente la ventana fuera del marco, UltraShare lo detecta y libera el vínculo.
- 📏 **Presets de Resolución**: Incluye tamaños optimizados como 1280x720 (Teams) y 1920x1080 (Full HD).

## 🛠️ Requisitos

- **Sistema Operativo**: Windows 10 / 11 (Requiere API Win32).
- **Lenguaje**: [Python 3.10+](https://www.python.org/)
- **Dependencias**: `customtkinter`, `pywin32`, `pillow` (ver requirements.txt).

## � Instalación

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/alexmnrs/UltraShare.git
   ```
2. **Navega al directorio**:
   ```bash
   cd UltraShare
   ```
3. **Instala dependencias**:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```

## 💻 Uso

1. **Ejecuta la aplicación**:
   ```bash
   # Desde código fuente
   python main.py
   
   # O si usas el ejecutable generado
   ./dist/UltraShare/UltraShare.exe
   ```

2. **Configura tu sesión**:
   - Selecciona el tamaño deseado en el Panel de Control (ej. "Teams Optimized").
   - Coloca la ventana que quieres compartir debajo del marco.
   - Selecciona la ventana en la lista y pulsa **"SNAP!"**.

3. **Comparte**:
   - En Teams/Zoom, comparte **solo la ventana** que has ajustado.

## ⚠️ Notas Importantes

- **Modo Administrador**: Algunas aplicaciones (como el Administrador de Tareas) pueden requerir que ejecutes UltraShare como administrador para poder manipularlas.
- **Multimonitor**: UltraShare funciona mejor si inicias la aplicación en el monitor donde vas a trabajar.

## 👨� Autor

**Alex Monrás**
*SysAdmin & Entusiasta del Desarrollo*

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

---
© 2026 Alex Monrás.
