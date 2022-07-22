import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyqtribbon",
    version="0.1.0",
    author="WANG Hailin",
    author_email="hailin.wang@connect.polyu.hk",
    description="PyQtRibbon is a Qt-based application framework for building user interfaces.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/haiiliin/pyqtribbon",
    include_package_data=True,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
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
        'styles/default.qss',
        'styles/debug.qss'
    ])],
    setup_requires=["cython", "numpy"],
    install_requires=['PyQt5', 'numpy']
)
