
import os 
import shutil
import time
from winotify import Notification
import pyshortcuts
import sys
from contextlib import suppress # for hiding splash screen

STARTUP_NAME = "BumoAutostart.lnk"
USER_HOME = os.getenv("userprofile")
AUTO_START_DIR = os.path.join(USER_HOME, r"AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup")
GCODE_DIR = os.path.join(USER_HOME, r"Desktop\GCode")
ICON_FILE_NAME = "data\splash.png"
SPEED_S = 2

new_path = r"C:\ankommen"
latest_file = None 
latest_mod_time = 0

def running_as_exe():
    return getattr(sys, 'frozen', False)

def get_exe_path():
    application_path = "unknown"
    if running_as_exe():
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)
    return application_path

def create_shortcut_pyshortcuts(dest_file_path, name, folder=None, icon=None, description=None):
    pyshortcuts.make_shortcut(
        script=dest_file_path,
        name=name,
        folder=folder,  # "Desktop" or "StartMenu" on Windows
        icon=icon,
        description=description
    )
    print(f"Shortcut '{name}' created.")

def get_files_and_mod_times(directory_path):
    files = {}
    for fn in os.listdir(directory_path):
        file_path = os.path.join(directory_path, fn)
        if os.path.isfile(file_path):
            try: 
                mod_time = os.path.getmtime(file_path)
                files[fn] = mod_time
            except OSError as _:
                pass
    return files

def create_dirs():
    try: 
        os.mkdir(GCODE_DIR)
    except FileExistsError:
        " "


def copy_file(latest_file):
    shutil.copy(f"{latest_file}", f"{new_path}")

def show_notification():
    toast = Notification(app_id = "Bumotec 2",
                        title = "",
                        msg = f"GCode was sent successfully",
                        duration = "short",
                        icon = os.path.join(get_exe_path(), ICON_FILE_NAME)
    )
    toast.show()




def autoInstall():
    create_shortcut_pyshortcuts(get_exe_path(), STARTUP_NAME, AUTO_START_DIR)

def startup():
    create_dirs()

    if running_as_exe():
        autoInstall()
        print("auto installed in startup")
        with suppress(ModuleNotFoundError):
            import pyi_splash
            pyi_splash.close()
    
    return get_files_and_mod_times(GCODE_DIR)

def should_copy_file(already_copied_files, file_name, last_mode_time) -> bool:
    should_copy = False
    try:
        mod_time = already_copied_files[file_name]
        if last_mode_time > mod_time:
            should_copy = True
    except Exception as _:
        should_copy = True
        print("new file - copying")
    return should_copy

if __name__ == "__main__":
    already_copied_files = startup()
    while True:
        files = get_files_and_mod_times(GCODE_DIR)
        for file_name in files:
            mod_time = files[file_name]
            if should_copy_file(already_copied_files, file_name, mod_time):
                copy_file(os.path.join(GCODE_DIR, file_name))
                show_notification()
                already_copied_files[file_name] = mod_time

        time.sleep(SPEED_S)


