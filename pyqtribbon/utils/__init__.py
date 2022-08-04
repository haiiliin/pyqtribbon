# coding:utf-8
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


if sys.platform == "win32":
    from .win32_utils import WindowsMoveResize as MoveResize
elif sys.platform == "darwin":
    from .mac_utils import MacMoveResize as MoveResize
else:
    from .linux_utils import LinuxMoveResize as MoveResize


def startSystemMove(window, globalPos):
    """ resize window

    Parameters
    ----------
    window: QWidget
        window

    globalPos: QPoint
        the global point of mouse release event
    """
    MoveResize.startSystemMove(window, globalPos)


def starSystemResize(window, globalPos, edges):
    """ resize window

    Parameters
    ----------
    window: QWidget
        window

    globalPos: QPoint
        the global point of mouse release event

    edges: `Qt.Edges`
        window edges
    """
    MoveResize.starSystemResize(window, globalPos, edges)
