import os
import sys


def interpreter_dir():
    """Return the path to the interpreter directory.

    :return: The path to the interpreter directory.
    """
    return os.path.dirname(sys.executable)


def data_file_path(filename):
    """Return the path to a data file.

    :param filename: The filename of the data file.
    :return: The path to the data file.
    """
    if os.path.exists(filename):
        return filename
    elif os.path.exists(os.path.join(interpreter_dir(), filename)):
        return os.path.join(interpreter_dir(), filename)
    else:
        return None
