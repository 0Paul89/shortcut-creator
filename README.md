# Shortcut Creator

A modern GUI application for creating desktop shortcuts on Linux systems. This tool helps you easily create and manage desktop entries for your applications, AppImages, scripts, and other executables.

## Features

- Create desktop shortcuts with a modern, user-friendly interface
- Support for AppImages, Python scripts, shell scripts, and other executables
- Custom icon selection
- Application categorization
- Terminal mode option
- Desktop shortcut creation
- Real-time logging
- Automatic executable permission management

## Requirements

- Python 3.6 or later
- PyQt6
- Linux operating system

## Installation

1. Clone this repository:
```bash
git clone https://github.com/0Paul89/shortcut-creator.git
cd shortcut-creator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python3 shortcut-creator.py
```

### Creating a Shortcut

1. Click "Browse" to select your executable file (AppImage, script, etc.)
2. (Optional) Select an icon file
3. Enter the application name
4. (Optional) Add a description
5. Select appropriate categories
6. Choose additional options:
   - Run in terminal (for CLI applications)
   - Copy to Desktop
7. Click "Create Shortcut"

The shortcut will be created in `~/.local/share/applications/` and optionally on your desktop.
