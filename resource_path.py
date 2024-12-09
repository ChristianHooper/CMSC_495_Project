import os
import sys

def resource_path(relative_path):
    """ Get the absolute path to a resource, works for development and PyInstaller executable """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)