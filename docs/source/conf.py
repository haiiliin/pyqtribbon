# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import inspect
import os
import sys

import pyqtribbon

sys.path.insert(0, os.path.abspath("../../"))

# -- Project information -----------------------------------------------------

project = "pyqtribbon"
copyright = "2022, WANG Hailin"
author = "WANG Hailin"

# The full version, including alpha/beta/rc tags
release = version = pyqtribbon.__version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "hoverxref.extension",
    "sphinx.ext.autosummary",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.linkcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.githubpages",
    "sphinx_copybutton",
    "sphinx_codeautolink",
    "sphinx_toolbox.more_autodoc.overloads",
    "sphinx_qt_documentation",
    "sphinxcontrib.apidoc",
]

qt_documentation = "Qt5"
autodoc_typehints_format = "short"
numpydoc_show_inherited_class_members = False

# sphinx.ext.intersphinx configuration
intersphinx_mapping = {
    "jinjia2": ("https://jinja.palletsprojects.com/en/3.0.x/", None),
    "matplotlib": ("https://matplotlib.org/stable/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "pytest": ("https://pytest.org/en/stable/", None),
    "python": ("https://docs.python.org/3/", None),
    "readthedocs": ("https://docs.readthedocs.io/en/stable/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/", None),
}

# Hoverxref configuration
hoverxref_auto_ref = True
hoverxref_domains = ["py"]
hoverxref_roles = [
    "numref",
    "confval",
    "setting",
    "option",
    "doc",  # Documentation pages
    "term",  # Glossary terms
]
hoverxref_role_types = {
    "doc": "modal",  # for whole docs
    "mod": "modal",  # for Python Sphinx Domain
    "class": "tooltip",  # for Python Sphinx Domain
    "func": "tooltip",  # for Python Sphinx Domain
    "meth": "tooltip",  # for Python Sphinx Domain
    "attr": "tooltip",  # for Python Sphinx Domain
    "exc": "tooltip",  # for Python Sphinx Domain
    "obj": "tooltip",  # for Python Sphinx Domain
    "ref": "tooltip",  # for hoverxref_auto_ref config
    "confval": "tooltip",  # for custom object
    "term": "tooltip",  # for glossaries
    "numref": "tooltip",
}
hoverxref_intersphinx = [
    "numpy",
    "pytest",
    "python",
    "readthedocs",
]

# sphinxcontrib-apidoc configuration
apidoc_module_dir = "../../pyqtribbon"
apidoc_output_dir = "apidoc"
apidoc_excluded_paths = []
apidoc_separate_modules = True
apidoc_toc_file = False
apidoc_extra_args = ["-d 1"]

# sphinx.ext.autodoc configuration
autoclass_content = "both"


# linkcode source
def linkcode_resolve(domain: str, info: dict):
    """Resolve linkcode source
    Parameters
    ----------
    domain : str
        specifies the language domain the object is in
    info : dict[str, str | list[str]]
        a dictionary with the following keys guaranteed to be present (dependent on the domain)

        - py: module (name of the module), fullname (name of the object)
        - c: names (list of names for the object)
        - cpp: names (list of names for the object)
        - javascript: object (name of the object), fullname (name of the item)

    Returns
    -------
    source url of the object
    """
    if domain != "py":
        return None

    modname = info["module"]
    fullname = info["fullname"]

    filename = modname.replace(".", "/")
    baseurl = f"https://github.com/haiiliin/pyqtribbon/blob/main/{filename}.py"

    submod = sys.modules.get(modname)
    if submod is None:
        return baseurl

    obj = submod
    for part in fullname.split("."):
        try:
            obj = getattr(obj, part)
        except Exception:
            return baseurl
    try:
        source, lineno = inspect.getsourcelines(obj)
    except Exception:
        return baseurl

    return baseurl + f"#L{lineno}-L{lineno + len(source) - 1}"


# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
