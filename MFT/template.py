import pathlib
import subprocess
import platform
import sys
import importlib
import os

req_file = tdu.expandPath(ipar.ExtPython.Pyreqs)
lib_dir = tdu.expandPath(ipar.ExtPython.Libdir)

os.makedirs(lib_dir, exist_ok=True)

def install_libs():
    install_script_path = pathlib.Path(lib_dir).parents[0]

    win_file = install_script_path / "dep_install.cmd"
    mac_file = install_script_path / "dep_install.sh"

    # Windows template
    win_txt = f"""
    :: udpate pip
    python -m pip install --user --upgrade pip

    :: install from requirements file
    py -3.11 -m pip install -r "{req_file}" --target="{lib_dir}"

    :: keep the window open
    :: pause
    """

    mac_txt = f"""
    #!/bin/bash

    dep=$(dirname "$0")
    pythonDir=/python

    # change the current directory to where the script is run from
    dirname "$(readlink -f "$0")"

    # fix up pip with python3
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

    # Update pip
    python -m pip install --user --upgrade pip

    # Install requirements
    python -m pip install -r "{req_file}" --target="{lib_dir}"
    """

    with open(win_file, "w+") as f:
        f.write(win_txt)

    with open(mac_file, "w+") as f:
        f.write(mac_txt)

    # Call the install script for windows
    if platform.system() == "Windows":
        subprocess.call([win_file])
    elif platform.system() == "Darwin":
        subprocess.call([mac_file])

# Update TouchDesigner's python path
def add_to_sys_path():
    if lib_dir not in sys.path:
        sys.path.append(lib_dir)

def check_if_libs_are_installed():
    try:
        importlib.import_module("pymft")
        return True
    except ImportError:
        return False

add_to_sys_path()

installed = check_if_libs_are_installed()

if not installed:
    install_libs()
