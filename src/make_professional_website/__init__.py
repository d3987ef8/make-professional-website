from pathlib import Path
import os

def get_file_directory_path(file):
    return Path(os.path.os.path.realpath(file)).parent

class Module:
    def get_output_files(self, globals, content):
        raise Exception("Classes must override Module.get_output_files.")
