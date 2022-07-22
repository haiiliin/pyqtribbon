import os


def package_source_dir():
    """
    Returns the path to the source directory of the package.
    """
    return os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../')
