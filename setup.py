# setup.py for py2app
from setuptools import setup

APP = ['src/EyeCare.py']
# Note: py2app uses the first entry in APP to name the .app bundle if not specified otherwise
# But we can try to force the bundle name by renaming the main script or using a different setup.
# Actually, py2app usually names the bundle based on the main script's filename (main.py -> main.app).
# To get EyeCare.app, the main script should be EyeCare.py or we can rename it after build.
DATA_FILES = ['assets']
OPTIONS = {
    'argv_option': False,
    'iconfile': 'assets/bg.icns',
    'plist': {
        'CFBundleName': 'EyeCare',
        'CFBundleDisplayName': '20-20-20 Eye Care',
        'CFBundleIdentifier': 'com.yourname.eyecare',
        'CFBundleVersion': '0.1.0',
        'CFBundleShortVersionString': '0.1.0',
        'NSAppleScriptEnabled': False,
        'LSUIElement': True, # This is critical for menubar apps to hide the dock icon
        'CFBundleIconFile': 'bg.icns',
    },
    'packages': ['rumps', 'tkinter'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app.main': OPTIONS},
)
