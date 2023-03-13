from pathlib import Path

try:
    from ._version import version as default_version
except ImportError:
    default_version = "0.0.0-unknown"


def _get_version():
    """Return the version string used for __version__."""
    # Only shell out to a git subprocess if really needed, and not on a
    # shallow clone, such as those used by CI, as the latter would trigger
    # a warning from setuptools_scm.
    root = Path(__file__).resolve().parents[1]
    if (root / ".git").exists() and not (root / ".git/shallow").exists():
        try:
            import setuptools_scm

            return setuptools_scm.get_version(
                root=str(root),
                version_scheme="post-release",
                fallback_version=default_version,
            )
        except Exception:
            return default_version
    else:  # Get the version from the _version.py setuptools_scm file.
        return default_version


__version__ = _get_version()
