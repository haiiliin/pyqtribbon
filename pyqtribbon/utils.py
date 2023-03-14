import os


def DataFile(filename):
    """Return the path to a data file.

    :param filename: The filename of the data file.
    :return: The path to the data file.
    """
    return os.path.join(os.path.dirname(__file__), filename)
