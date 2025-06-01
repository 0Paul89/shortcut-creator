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
    QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont, QPalette, QColor

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
            QLineEdit:focus {
                border: 2px solid #2196F3;
            }
        """)

class ModernButton(QPushButton):
    """Custom styled button widget"""
    def __init__(self, text, primary=False, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(35)
        if primary:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 5px 15px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
                QPushButton:pressed {
                    background-color: #1565C0;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #f5f5f5;
                    color: #333;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    padding: 5px 15px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
            """)

class ModernComboBox(QComboBox):
    """Custom styled combobox widget"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(35)
        self.setStyleSheet("""
            QComboBox {
                padding: 5px 10px;
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                background: white;
                font-size: 14px;
            }
            QComboBox:focus {
                border: 2px solid #2196F3;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
        """)

class ModernCheckBox(QCheckBox):
    """Custom styled checkbox widget"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #e0e0e0;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                background-color: #2196F3;
                border-color: #2196F3;
            }
            QCheckBox::indicator:hover {
                border-color: #2196F3;
            }
        """)

class ShortcutCreator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shortcut Creator")
        self.setMinimumSize(800, 600)
        
        # Set application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #fafafa;
            }
            QLabel {
                font-size: 14px;
                color: #333;
            }
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-top: 1em;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("Shortcut Creator")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #1976D2;
            margin-bottom: 10px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Create scroll area for the form
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        main_layout.addWidget(scroll_area)
        
        # Create form widget
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(15)
        scroll_area.setWidget(form_widget)
        
        # Executable file selection
        exec_group = QGroupBox("Application Details")
        exec_layout = QVBoxLayout(exec_group)
        
        exec_path_layout = QHBoxLayout()
        self.executable_path = ModernLineEdit(placeholder="Select executable file...")
        browse_exec_btn = ModernButton("Browse")
        browse_exec_btn.clicked.connect(self.browse_executable)
        exec_path_layout.addWidget(self.executable_path)
        exec_path_layout.addWidget(browse_exec_btn)
        exec_layout.addLayout(exec_path_layout)
        
        # Icon file selection
        icon_path_layout = QHBoxLayout()
        self.icon_path = ModernLineEdit(placeholder="Select icon file (optional)...")
        browse_icon_btn = ModernButton("Browse")
        browse_icon_btn.clicked.connect(self.browse_icon)
        icon_path_layout.addWidget(self.icon_path)
        icon_path_layout.addWidget(browse_icon_btn)
        exec_layout.addLayout(icon_path_layout)
        
        # App name
        self.app_name = ModernLineEdit(placeholder="Application name...")
        exec_layout.addWidget(self.app_name)
        
        # Description
        self.comment = ModernLineEdit(placeholder="Description (optional)...")
        exec_layout.addWidget(self.comment)
        
        # Categories
        self.categories = ModernComboBox()
        self.categories.addItems([
            'Application', 'Development', 'TextEditor', 'Graphics', 'Internet',
            'Multimedia', 'Office', 'Game', 'System', 'Utility'
        ])
        exec_layout.addWidget(self.categories)
        
        form_layout.addWidget(exec_group)
        
        # Options
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout(options_group)
        
        self.terminal = ModernCheckBox("Run in terminal")
        self.desktop_copy = ModernCheckBox("Also copy to Desktop")
        options_layout.addWidget(self.terminal)
        options_layout.addWidget(self.desktop_copy)
        
        form_layout.addWidget(options_group)
        
        # Log area
        log_group = QGroupBox("Log")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
                font-family: monospace;
                font-size: 13px;
            }
        """)
        log_layout.addWidget(self.log_text)
        
        form_layout.addWidget(log_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        create_btn = ModernButton("Create Shortcut", primary=True)
        create_btn.clicked.connect(self.create_shortcut)
        
        clear_btn = ModernButton("Clear All")
        clear_btn.clicked.connect(self.clear_all)
        
        exit_btn = ModernButton("Exit")
        exit_btn.clicked.connect(self.close)
        
        button_layout.addWidget(create_btn)
        button_layout.addWidget(clear_btn)
        button_layout.addWidget(exit_btn)
        
        main_layout.addLayout(button_layout)
        
    def log(self, message):
        """Add message to log area"""
        self.log_text.append(message)
        # Scroll to bottom
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )
        
    def browse_executable(self):
        """Browse for executable file"""
        initial_dir = os.path.expanduser("~")
        if self.executable_path.text():
            initial_dir = os.path.dirname(self.executable_path.text())
            
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Executable File",
            initial_dir,
            "Executable files (*.AppImage *.py *.sh);;AppImage files (*.AppImage);;Python scripts (*.py);;Shell scripts (*.sh);;All files (*.*)"
        )
        
        if filename:
            self.executable_path.setText(filename)
            # Auto-fill app name if empty
            if not self.app_name.text():
                app_name = Path(filename).stem.replace('.AppImage', '').replace('-', ' ').replace('_', ' ').title()
                self.app_name.setText(app_name)
                
    def browse_icon(self):
        """Browse for icon file"""
        initial_dir = os.path.expanduser("~")
        if self.executable_path.text():
            initial_dir = os.path.dirname(self.executable_path.text())
        elif self.icon_path.text():
            initial_dir = os.path.dirname(self.icon_path.text())
            
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Icon File",
            initial_dir,
            "Image files (*.png *.jpg *.jpeg *.gif *.bmp *.svg *.ico);;All files (*.*)"
        )
        
        if filename:
            self.icon_path.setText(filename)
            
    def clear_all(self):
        """Clear all fields"""
        self.executable_path.clear()
        self.icon_path.clear()
        self.app_name.clear()
        self.comment.clear()
        self.categories.setCurrentIndex(0)
        self.terminal.setChecked(False)
        self.desktop_copy.setChecked(False)
        self.log_text.clear()
        
    def validate_inputs(self):
        """Validate user inputs"""
        if not self.executable_path.text():
            QMessageBox.critical(self, "Error", "Please select an executable file")
            return False
            
        if not os.path.exists(self.executable_path.text()):
            QMessageBox.critical(self, "Error", "Executable file does not exist")
            return False
            
        if not self.app_name.text():
            QMessageBox.critical(self, "Error", "Please enter an application name")
            return False
            
        if self.icon_path.text() and not os.path.exists(self.icon_path.text()):
            QMessageBox.critical(self, "Error", "Icon file does not exist")
            return False
            
        return True
        
    def create_shortcut(self):
        """Create the desktop shortcut"""
        if not self.validate_inputs():
            return
            
        try:
            self.log("Starting desktop shortcut creation...")
            
            # Make executable file executable
            executable_path = self.executable_path.text()
            self.log(f"Making executable: {executable_path}")
            
            if not os.access(executable_path, os.X_OK):
                os.chmod(executable_path, os.stat(executable_path).st_mode | stat.S_IEXEC)
                self.log("File made executable")
            else:
                self.log("File is already executable")
            
            # Create desktop entry content
            app_name = self.app_name.text()
            desktop_filename = app_name.lower().replace(' ', '-') + '.desktop'
            
            desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name={app_name}
Comment={self.comment.text() or app_name}
Exec={executable_path}
Terminal={'true' if self.terminal.isChecked() else 'false'}
Categories={self.categories.currentText()};
StartupNotify=true"""

            if self.icon_path.text():
                desktop_content += f"\nIcon={self.icon_path.text()}"
                
            # Ensure applications directory exists
            apps_dir = Path.home() / '.local' / 'share' / 'applications'
            apps_dir.mkdir(parents=True, exist_ok=True)
            
            # Write desktop file
            desktop_file_path = apps_dir / desktop_filename
            self.log(f"Creating desktop file: {desktop_file_path}")
            
            with open(desktop_file_path, 'w') as f:
                f.write(desktop_content)
                
            # Make desktop file executable
            current_permissions = os.stat(desktop_file_path).st_mode
            os.chmod(desktop_file_path, current_permissions | stat.S_IEXEC | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            self.log("Desktop file made executable")
            
            # Verify it's executable
            if os.access(desktop_file_path, os.X_OK):
                self.log("✅ Desktop file executable permissions verified")
            else:
                self.log("⚠️ Warning: Desktop file may not be executable")
            
            # Update desktop database
            try:
                subprocess.run(['update-desktop-database', str(apps_dir)], 
                             check=True, capture_output=True, text=True)
                self.log("Desktop database updated")
            except subprocess.CalledProcessError as e:
                self.log(f"Warning: Could not update desktop database: {e}")
            except FileNotFoundError:
                self.log("Warning: update-desktop-database not found, shortcut may not appear immediately")
                
            # Copy to desktop if requested
            if self.desktop_copy.isChecked():
                desktop_dir = Path.home() / 'Desktop'
                if desktop_dir.exists():
                    desktop_copy_path = desktop_dir / desktop_filename
                    with open(desktop_copy_path, 'w') as f:
                        f.write(desktop_content)
                    # Make desktop copy executable too
                    current_permissions = os.stat(desktop_copy_path).st_mode
                    os.chmod(desktop_copy_path, current_permissions | stat.S_IEXEC | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
                    self.log(f"Desktop shortcut created and made executable: {desktop_copy_path}")
                else:
                    self.log("Warning: Desktop directory not found, skipping desktop copy")
                    
            self.log("✅ Desktop shortcut created successfully!")
            self.log(f"Application '{app_name}' should now appear in your application menu")
            
            QMessageBox.information(self, "Success", f"Desktop shortcut for '{app_name}' created successfully!")
            
        except Exception as e:
            error_msg = f"Error creating desktop shortcut: {str(e)}"
            self.log(f"❌ {error_msg}")
            QMessageBox.critical(self, "Error", error_msg)

def main():
    app = QApplication(sys.argv)
    
    # Set application-wide font
    app.setFont(QFont("Arial", 10))
    
    window = ShortcutCreator()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
