import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyqtribbon",
    version="0.4.0",
    author="WANG Hailin",
    author_email="hailin.wang@connect.polyu.hk",
    description="PyQtRibbon is a Qt-based application framework for building user interfaces.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/haiiliin/pyqtribbon",
    include_package_data=True,
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    data_files=[('icons', [
        'icons/backward.png',
        'icons/down.png',
        'icons/forward.png',
        'icons/help.png',
        'icons/linking.png',
        'icons/max.png',
        'icons/min.png',
        'icons/more.png',
        'icons/python.png',
        'icons/redo.png',
        'icons/save.png',
        'icons/undo.png',
        'icons/up.png',
    ]), ('styles', [
        'styles/base.qss',
        'styles/default.qss',
        'styles/debug.qss'
    ])],
    install_requires=['PyQt5', 'numpy'],
)
