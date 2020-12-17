import os
import os.path
import sys
from django.conf import settings
import importlib.util
import psutil
engine_name = 'ANFIS_MATLAB'

def is_matlab_exist():
    if (os.path.isfile(settings.MATLAB_EXE) is False):
        raise Exception("we can't find matlab executable. \
            setting matlab path in file settings.py on variable MATLAB_EXE")

def is_matlab_engine_exist():
    matlab_package = importlib.util.find_spec('matlab')
    matlab_engine_package = importlib.util.find_spec('matlab.engine')

    if (matlab_package is None or matlab_engine_package is None):
        raise Exception("matlab engine is not installed.")

def is_matlab_running():
    running = 'MATLAB.exe' in (p.name() for p in psutil.process_iter())
    return running

def is_matlab_engine_running():
    import matlab.engine
    matlab_engines = matlab.engine.find_matlab()
    index_engine = False
    if (engine_name in matlab_engines):
        index_engine = matlab_engines.index(engine_name)

    return index_engine

def remove_temp_session():
    filename = os.path.join(settings.TEMP_DIR, engine_name)
    if (os.path.isfile(filename)):
        os.remove(filename)

def run_matlab():
    import subprocess

    command = "{} -nodesktop -nosplash -minimize -r \"matlab.engine.shareEngine('{}'); disp('Engine is shared');\"".format(settings.MATLAB_EXE, engine_name)
    subprocess.run(command)

def main():
    try:
        is_matlab_exist()
        is_matlab_engine_exist()
        if (is_matlab_engine_running() is False and is_matlab_running() is False):
            remove_temp_session()
            run_matlab()
    except Exception as e:
        raise e

