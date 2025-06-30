#!/usr/bin/env python3
"""
Shortcut Creator
A modern GUI tool to create desktop shortcuts for applications on Linux
"""

import sys
import os
import stat
import subprocess
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog, QComboBox,
    QCheckBox, QTextEdit, QMessageBox, QFrame, QGroupBox,
    QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class ModernLineEdit(QLineEdit):
    """Custom styled line edit widget"""
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(35)
        self.setStyleSheet("""
            QLineEdit {
                padding: 5px 10px;
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                background: white;
                font-size: 14px;
            }
            QLineEdit:focus { border: 2px solid #2196F3; }
        """)

class ModernButton(QPushButton):
    """Custom styled button widget"""
    def __init__(self, text, primary=False, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(35)
        if primary:
            self.setStyleSheet("""
                QPushButton { background-color: #2196F3; color: white; border: none; border-radius: 5px; padding: 5px 15px; font-size: 14px; font-weight: bold; }
                QPushButton:hover { background-color: #1976D2; }
                QPushButton:pressed { background-color: #1565C0; }
            """)
        else:
            self.setStyleSheet("""
                QPushButton { background-color: #f5f5f5; color: #333; border: 1px solid #ddd; border-radius: 5px; padding: 5px 15px; font-size: 14px; }
                QPushButton:hover { background-color: #e0e0e0; }
                QPushButton:pressed { background-color: #d0d0d0; }
            """)

class ModernComboBox(QComboBox):
    """Custom styled combobox widget"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(35)
        self.setStyleSheet("""
            QComboBox { padding: 5px 10px; border: 2px solid #e0e0e0; border-radius: 5px; background: white; font-size: 14px; }
            QComboBox:focus { border: 2px solid #2196F3; }
        """)

class ModernCheckBox(QCheckBox):
    """Custom styled checkbox widget"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QCheckBox { font-size: 14px; spacing: 8px; }
            QCheckBox::indicator { width: 18px; height: 18px; border: 2px solid #e0e0e0; border-radius: 3px; }
            QCheckBox::indicator:checked { background-color: #2196F3; border-color: #2196F3; }
            QCheckBox::indicator:hover { border-color: #2196F3; }
        """)

class ShortcutCreator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shortcut Creator")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("""
            QMainWindow { background-color: #fafafa; }
            QLabel { font-size: 14px; color: #333; }
            QGroupBox { font-size: 14px; font-weight: bold; border: 1px solid #ddd; border-radius: 5px; margin-top: 1em; padding-top: 10px; }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }
        """)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        title = QLabel("Shortcut Creator")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size:24px; font-weight:bold; color:#1976D2;")
        main_layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        main_layout.addWidget(scroll)
        form = QWidget(); fl = QVBoxLayout(form); fl.setSpacing(15)
        scroll.setWidget(form)

        # Application Details
        grp = QGroupBox("Application Details"); gl = QVBoxLayout(grp)
        ep = QHBoxLayout(); self.executable_path = ModernLineEdit("Select executable file...")
        be = ModernButton("Browse"); be.clicked.connect(self.browse_executable)
        ep.addWidget(self.executable_path); ep.addWidget(be); gl.addLayout(ep)
        ip = QHBoxLayout(); self.interpreter_path = ModernLineEdit("Interpreter (optional)")
        bi = ModernButton("Browse"); bi.clicked.connect(self.browse_interpreter)
        ip.addWidget(self.interpreter_path); ip.addWidget(bi); gl.addLayout(ip)
        ic = QHBoxLayout(); self.icon_path = ModernLineEdit("Select icon file (optional)...")
        bi2 = ModernButton("Browse"); bi2.clicked.connect(self.browse_icon)
        ic.addWidget(self.icon_path); ic.addWidget(bi2); gl.addLayout(ic)
        self.app_name = ModernLineEdit("Application name..."); gl.addWidget(self.app_name)
        self.comment = ModernLineEdit("Description (optional)..."); gl.addWidget(self.comment)
        self.categories = ModernComboBox(); self.categories.addItems([
            'Application','Development','TextEditor','Graphics','Internet','Multimedia','Office','Game','System','Utility'
        ]); gl.addWidget(self.categories)
        fl.addWidget(grp)

        # Options
        og = QGroupBox("Options"); ol = QVBoxLayout(og)
        self.terminal = ModernCheckBox("Run in terminal"); ol.addWidget(self.terminal)
        self.desktop_copy = ModernCheckBox("Also copy to Desktop"); ol.addWidget(self.desktop_copy)
        fl.addWidget(og)

        # Log
        lg = QGroupBox("Log"); ll = QVBoxLayout(lg)
        self.log_text = QTextEdit(); self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet(
            "QTextEdit{background:white;border:1px solid #ddd;border-radius:5px;padding:10px;"
            "font-family:monospace;font-size:13px;}"
        )
        ll.addWidget(self.log_text); fl.addWidget(lg)

        # Buttons
        bl = QHBoxLayout()
        cbtn = ModernButton("Create Shortcut", primary=True); cbtn.clicked.connect(self.create_shortcut)
        clbtn = ModernButton("Clear All"); clbtn.clicked.connect(self.clear_all)
        exbtn = ModernButton("Exit"); exbtn.clicked.connect(self.close)
        bl.addWidget(cbtn); bl.addWidget(clbtn); bl.addWidget(exbtn)
        main_layout.addLayout(bl)

    def log(self, msg):
        self.log_text.append(msg)
        self.log_text.verticalScrollBar().setValue(self.log_text.verticalScrollBar().maximum())

    def browse_executable(self):
        d = os.path.expanduser("~") if not self.executable_path.text() else os.path.dirname(self.executable_path.text())
        f, _ = QFileDialog.getOpenFileName(
            self, "Select Executable File", d,
            "Executable files (*.AppImage *.py *.sh);;All files (*.*)"
        )
        if f:
            self.executable_path.setText(f)
            if not self.app_name.text():
                self.app_name.setText(Path(f).stem.replace('.AppImage', '').replace('_', ' ').replace('-', ' ').title())

    def browse_interpreter(self):
        d = os.path.expanduser("~")
        f, _ = QFileDialog.getOpenFileName(
            self, "Select Interpreter", d,
            "All files (*.*)"
        )
        if f:
            self.interpreter_path.setText(f)

    def browse_icon(self):
        d = os.path.dirname(self.executable_path.text()) if self.executable_path.text() else os.path.expanduser("~")
        f, _ = QFileDialog.getOpenFileName(
            self, "Select Icon File", d,
            "Image files (*.png *.jpg *.svg *.ico);;All files (*.*)"
        )
        if f:
            self.icon_path.setText(f)

    def clear_all(self):
        for w in [self.executable_path, self.interpreter_path, self.icon_path, self.app_name, self.comment]: w.clear()
        self.categories.setCurrentIndex(0)
        self.terminal.setChecked(False)
        self.desktop_copy.setChecked(False)
        self.log_text.clear()

    def validate_inputs(self):
        if not self.executable_path.text(): QMessageBox.critical(self, "Error", "Select an executable"); return False
        if not os.path.exists(self.executable_path.text()): QMessageBox.critical(self, "Error", "Executable not found"); return False
        if not self.app_name.text(): QMessageBox.critical(self, "Error", "Enter application name"); return False
        if self.icon_path.text() and not os.path.exists(self.icon_path.text()): QMessageBox.critical(self, "Error", "Icon not found"); return False
        return True

    def create_shortcut(self):
        if not self.validate_inputs(): return
        try:
            self.log("Starting shortcut creation...")
            exe = self.executable_path.text()
            if not os.access(exe, os.X_OK): os.chmod(exe, os.stat(exe).st_mode | stat.S_IEXEC); self.log("Made executable")
            interp = self.interpreter_path.text().strip()
            name = self.app_name.text().strip(); fn = name.lower().replace(' ', '-') + '.desktop'
            cmd = f"{interp + ' ' if interp else ''}{exe}"
            content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name={name}
Comment={self.comment.text() or name}
Exec={cmd}
Terminal={'true' if self.terminal.isChecked() else 'false'}
Categories={self.categories.currentText()};
StartupNotify=true"""
            if self.icon_path.text(): content += f"\nIcon={self.icon_path.text()}"
            apps_dir = Path.home() / '.local' / 'share' / 'applications'; apps_dir.mkdir(parents=True, exist_ok=True)
            desktop_path = apps_dir / fn; self.log(f"Writing desktop file: {desktop_path}")
            desktop_path.write_text(content)
            desktop_path.chmod(desktop_path.stat().st_mode | stat.S_IEXEC)
            self.log("Desktop file permissions set")
            try: subprocess.run(['update-desktop-database', str(apps_dir)], check=True); self.log("Updated desktop database")
            except: self.log("Warning: update-desktop-database failed")
            if self.desktop_copy.isChecked():
                desk = Path.home() / 'Desktop'
                if desk.exists():
                    copy_path = desk / fn; copy_path.write_text(content); copy_path.chmod(copy_path.stat().st_mode | stat.S_IEXEC)
                    self.log(f"Copied shortcut to desktop: {copy_path}")
                else:
                    self.log("Warning: Desktop directory not found")
            self.log("✅ Shortcut created successfully")
            QMessageBox.information(self, "Success", f"Shortcut for '{name}' created.")
        except Exception as e:
            self.log(f"❌ Error: {e}")
            QMessageBox.critical(self, "Error", str(e))


def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Arial", 10))
    window = ShortcutCreator(); window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
