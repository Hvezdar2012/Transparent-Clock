from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QColorDialog, QVBoxLayout, QWidget, QPushButton, QSlider, QInputDialog, QHBoxLayout, QMessageBox, QDialog
from PyQt6.QtGui import QFont, QColor, QIcon, QPixmap
from PyQt6.QtCore import Qt, QTimer, QTime
import sys
import os
import base64
import winreg

REG_PATH = r"Software\\TransparentClock"

# Base64 kódy ikon
lock_svg_base64 = "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciICB2aWV3Qm94PSIwIDAgNTAgNTAiIHdpZHRoPSIyNTBweCIgaGVpZ2h0PSIyNTBweCI+PHBhdGggZD0iTSAyNSAzIEMgMTguMzYzMjgxIDMgMTMgOC4zNjMyODEgMTMgMTUgTCAxMyAyMCBMIDkgMjAgQyA3LjMwMDc4MSAyMCA2IDIxLjMwMDc4MSA2IDIzIEwgNiA0NyBDIDYgNDguNjk5MjE5IDcuMzAwNzgxIDUwIDkgNTAgTCA0MSA1MCBDIDQyLjY5OTIxOSA1MCA0NCA0OC42OTkyMTkgNDQgNDcgTCA0NCAyMyBDIDQ0IDIxLjMwMDc4MSA0Mi42OTkyMTkgMjAgNDEgMjAgTCAzNyAyMCBMIDM3IDE1IEMgMzcgOC4zNjMyODEgMzEuNjM2NzE5IDMgMjUgMyBaIE0gMjUgNSBDIDMwLjU2NjQwNiA1IDM1IDkuNDMzNTk0IDM1IDE1IEwgMzUgMjAgTCAxNSAyMCBMIDE1IDE1IEMgMTUgOS40MzM1OTQgMTkuNDMzNTk0IDUgMjUgNSBaIE0gMjUgMzAgQyAyNi42OTkyMTkgMzAgMjggMzEuMzAwNzgxIDI4IDMzIEMgMjggMzMuODk4NDM4IDI3LjYwMTU2MyAzNC42ODc1IDI3IDM1LjE4NzUgTCAyNyAzOCBDIDI3IDM5LjEwMTU2MyAyNi4xMDE1NjMgNDAgMjUgNDAgQyAyMy44OTg0MzggNDAgMjMgMzkuMTAxNTYzIDIzIDM4IEwgMjMgMzUuMTg3NSBDIDIyLjM5ODQzOCAzNC42ODc1IDIyIDMzLjg5ODQzOCAyMiAzMyBDIDIyIDMxLjMwMDc4MSAyMy4zMDA3ODEgMzAgMjUgMzAgWiIvPjwvc3ZnPg=="
unlock_png_base64 = "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciICB2aWV3Qm94PSIwIDAgNTAgNTAiIHdpZHRoPSIyNTBweCIgaGVpZ2h0PSIyNTBweCI+PHBhdGggZD0iTSAyMi43ODEyNSAwIEMgMjEuNjA1NDY5IC0wLjAwMzkwNjI1IDIwLjQwNjI1IDAuMTY0MDYzIDE5LjIxODc1IDAuNTMxMjUgQyAxMi45MDIzNDQgMi40OTIxODggOS4yODkwNjMgOS4yNjk1MzEgMTEuMjUgMTUuNTkzNzUgTCAxMS4yNSAxNS42NTYyNSBDIDExLjUwNzgxMyAxNi4zNjcxODggMTIuMTk5MjE5IDE4LjYxNzE4OCAxMi42MjUgMjAgTCA5IDIwIEMgNy4zNTU0NjkgMjAgNiAyMS4zNTU0NjkgNiAyMyBMIDYgNDcgQyA2IDQ4LjY0NDUzMSA3LjM1NTQ2OSA1MCA5IDUwIEwgNDEgNTAgQyA0Mi42NDQ1MzEgNTAgNDQgNDguNjQ0NTMxIDQ0IDQ3IEwgNDQgMjMgQyA0NCAyMS4zNTU0NjkgNDIuNjQ0NTMxIDIwIDQxIDIwIEwgMTQuNzUgMjAgQyAxNC40NDE0MDYgMTkuMDA3ODEzIDEzLjUxMTcxOSAxNi4wNzQyMTkgMTMuMTI1IDE1IEwgMTMuMTU2MjUgMTUgQyAxMS41MTk1MzEgOS43MjI2NTYgMTQuNSA0LjEwOTM3NSAxOS43ODEyNSAyLjQ2ODc1IEMgMjUuMDUwNzgxIDAuODMyMDMxIDMwLjY5NTMxMyAzLjc5Njg3NSAzMi4zNDM3NSA5LjA2MjUgQyAzMi4zNDM3NSA5LjA2NjQwNiAzMi4zNDM3NSA5LjA4OTg0NCAzMi4zNDM3NSA5LjA5Mzc1IEMgMzIuNTcwMzEzIDkuODg2NzE5IDMzLjY1NjI1IDEzLjQwNjI1IDMzLjY1NjI1IDEzLjQwNjI1IEMgMzMuNzQ2MDk0IDEzLjc2NTYyNSAzNC4wMjczNDQgMTQuMDUwNzgxIDM0LjM4NjcxOSAxNC4xMzY3MTkgQyAzNC43NSAxNC4yMjY1NjMgMzUuMTI4OTA2IDE0LjEwOTM3NSAzNS4zNzUgMTMuODMyMDMxIEMgMzUuNjIxMDk0IDEzLjU1MDc4MSAzNS42OTUzMTMgMTMuMTYwMTU2IDM1LjU2MjUgMTIuODEyNSBDIDM1LjU2MjUgMTIuODEyNSAzNC40MzM1OTQgOS4xNzE4NzUgMzQuMjUgOC41MzEyNSBMIDM0LjI1IDguNSBDIDMyLjc4MTI1IDMuNzYxNzE5IDI4LjYwMTU2MyAwLjU0Mjk2OSAyMy45Mzc1IDAuMDYyNSBDIDIzLjU1MDc4MSAwLjAyMzQzNzUgMjMuMTcxODc1IDAgMjIuNzgxMjUgMCBaIE0gOSAyMiBMIDQxIDIyIEMgNDEuNTU0Njg4IDIyIDQyIDIyLjQ0NTMxMyA0MiAyMyBMIDQyIDQ3IEMgNDIgNDcuNTU0Njg4IDQxLjU1NDY4OCA0OCA0MSA0OCBMIDkgNDggQyA4LjQ0NTMxMyA0OCA4IDQ3LjU1NDY4OCA4IDQ3IEwgOCAyMyBDIDggMjIuNDQ1MzEzIDguNDQ1MzEzIDIyIDkgMjIgWiBNIDI1IDMwIEMgMjMuMzAwNzgxIDMwIDIyIDMxLjMwMDc4MSAyMiAzMyBDIDIyIDMzLjg5ODQzOCAyMi4zOTg0MzggMzQuNjg3NSAyMyAzNS4xODc1IEwgMjMgMzggQyAyMyAzOS4xMDE1NjMgMjMuODk4NDM4IDQwIDI1IDQwIEMgMjYuMTAxNTYzIDQwIDI3IDM5LjEwMTU2MyAyNyAzOCBMIDI3IDM1LjE4NzUgQyAyNy42MDE1NjMgMzQuNjg3NSAyOCAzMy44OTg0MzggMjggMzMgQyAyOCAzMS4zMDA3ODEgMjYuNjk5MjE5IDMwIDI1IDMwIFoiLz48L3N2Zz4="

def load_icon_from_base64(base64_string):
    pixmap = QPixmap()
    pixmap.loadFromData(base64.b64decode(base64_string))
    return QIcon(pixmap)

def save_setting(name, value):
    try:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH) as key:
            winreg.SetValueEx(key, name, 0, winreg.REG_SZ, str(value))
    except Exception as e:
        print(f"Chyba při zápisu do registru: {e}")

def load_setting(name, default):
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ) as key:
            value, _ = winreg.QueryValueEx(key, name)
            return value
    except FileNotFoundError:
        return default

class TransparentClock(QMainWindow):
    def mousePressEvent(self, event):
        if not self.movement_locked and event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if not self.movement_locked and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.drag_position)
            self.drag_position = event.globalPosition().toPoint()
            self.save_settings()

    def load_settings(self):
        self.text_color = load_setting("text_color", "#535353")
        self.font_size = int(load_setting("font_size", 28))
        self.opacity = float(load_setting("opacity", 1.0))
        self.position = {"x": int(load_setting("position_x", 50)), "y": int(load_setting("position_y", 50))}
        self.movement_locked = load_setting("movement_locked", "False") == "True"

    def save_settings(self):
        save_setting("text_color", self.text_color)
        save_setting("font_size", self.font_size)
        save_setting("opacity", self.opacity)
        save_setting("position_x", self.x())
        save_setting("position_y", self.y())
        save_setting("movement_locked", self.movement_locked)

    def change_text_color(self):
        color = QColorDialog.getColor()
        if not color.isValid():
            return
        self.text_color = color.name()
        self.label.setStyleSheet(f"color: {self.text_color}; background: transparent;")
        self.save_settings()

    def change_size(self):
        size, ok = QInputDialog.getInt(self, "Velikost textu", "Zadejte novou velikost:", value=self.font_size, min=10, max=100)
        if ok:
            self.font_size = size
            self.label.setFont(QFont("Arial", self.font_size))
            self.label.adjustSize()
            self.save_settings()

    def change_opacity(self, value):
        self.opacity = value / 100
        self.setWindowOpacity(self.opacity)
        self.save_settings()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hodiny")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.load_settings()

        self.label = QLabel(self)
        self.label.setFont(QFont("Arial", self.font_size))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.update_time()

        self.setCentralWidget(self.label)
        self.resize(200, 100)
        self.move(self.position["x"], self.position["y"])
        
        self.setWindowOpacity(self.opacity)  # Nastaví uloženou průhlednost
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.label.setStyleSheet(f"color: {self.text_color}; background: transparent;")

        self.label.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.label.customContextMenuRequested.connect(self.show_settings)
        
    def update_time(self):
        current_time = QTime.currentTime().toString("HH:mm:ss")
        self.label.setText(current_time)
    
    def show_settings(self, pos):
        if hasattr(self, "settings_window") and self.settings_window.isVisible():
            return  # Pokud je okno nastavení už otevřené, neotevírej další
        
        if not hasattr(self, 'settings_window'):
            self.settings_window = QWidget()
            self.settings_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, False)
        else:
            self.settings_window.showNormal()
            return
        self.settings_window.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.settings_window.setWindowTitle("Nastavení")
        self.settings_window.setFixedSize(250, 250)


        layout = QVBoxLayout()

        # Vytvoření titulkové lišty
        title_bar = QWidget(self.settings_window)
        title_bar.setFixedHeight(50)
        title_bar.setStyleSheet("background-color: #333; color: white; padding: 5px;")

        self.title_label = QLabel("Nastavení", title_bar)  # 🟢 OPRAVA: Správná definice
        self.title_label.setStyleSheet("color: white; font-weight: bold;")

        lock_layout = QHBoxLayout()
        self.lock_button = QPushButton()
        self.update_lock_icon()
        self.lock_button.clicked.connect(self.toggle_lock)
        self.lock_button.setFixedSize(32, 32)  # Velikost ikonky
        layout.addLayout(lock_layout)

        hide_button = QPushButton("X", title_bar)
        hide_button.setStyleSheet("color: pink;")
        hide_button.setFixedSize(32, 32)
        hide_button.clicked.connect(self.settings_window.hide)

        title_layout = QHBoxLayout()
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()
        title_layout.addWidget(self.lock_button)
        title_layout.addWidget(hide_button)
        title_bar.setLayout(title_layout)

        layout.addWidget(title_bar)  # Přidá vlastní titulkovou lištu
        
        btn_color = QPushButton("Změnit barvu textu")
        btn_color.clicked.connect(self.change_text_color)
        layout.addWidget(btn_color)

        btn_size = QPushButton("Změnit velikost písma")
        btn_size.clicked.connect(self.change_size)
        layout.addWidget(btn_size)

        slider_alpha = QSlider(Qt.Orientation.Horizontal)
        slider_alpha.setMinimum(10)
        slider_alpha.setMaximum(100)
        slider_alpha.setValue(int(self.opacity * 100))
        slider_alpha.valueChanged.connect(self.change_opacity)
        layout.addWidget(slider_alpha)
        
        btn_exit = QPushButton("Vypnout hodiny")
        btn_exit.clicked.connect(self.confirm_exit)
        layout.addWidget(btn_exit)

        self.settings_window.setLayout(layout)
        self.settings_window.show()
    
    def confirm_exit(self):
        msg = QDialog(self)
        msg.setFixedSize(200, 50)
        msg.setWindowTitle("Opravdu chcete vypnout hodiny?")
        
        layout = QHBoxLayout()

        no = QPushButton("Zrušit")
        yes = QPushButton("Vypnout")

        no.clicked.connect(msg.close)
        yes.clicked.connect(QApplication.quit)

        layout.addWidget(no)
        layout.addWidget(yes)

        msg.setLayout(layout)
        msg.show()
    
    def toggle_lock(self):
        self.movement_locked = not self.movement_locked
        self.update_lock_icon()
        self.save_settings()
    
    def update_lock_icon(self):
        if self.movement_locked:
            self.lock_button.setIcon(load_icon_from_base64(lock_svg_base64))  # Zamčená ikona
        else:
            self.lock_button.setIcon(load_icon_from_base64(unlock_png_base64))  # Odemčená ikona
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    clock = TransparentClock()
    clock.show()
    sys.exit(app.exec())