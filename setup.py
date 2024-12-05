from setuptools import setup

APP = ['audit_mac.py']  # Remplacez 'audit.py' par le nom de votre script
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['psutil', 'platform', 'tkinter', 'reportlab'],
    'includes': ['socket', 'os', 'subprocess', 'time'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
