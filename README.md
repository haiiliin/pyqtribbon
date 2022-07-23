# pyqtribbon

PyQtRibbon is a Qt-based application framework for building user interfaces.

- Documentation: [pyqtribbon.haiiliin.com](https://pyqtribbon.haiiliin.com/).
- PyPI: [pypi.org/project/pyqtribbon](https://pypi.org/project/pyqtribbon/).
- Read the Docs: [readthedocs.org/projects/pyqribbon](https://readthedocs.org/projects/pyqribbon/).

## Installation

`pyqtribbon` is distribued to [PyPI](https://pypi.org/project/pyqtribbon/), you can use pip to install it:

```shell
pip install pyqtribbon
```

You can also install the package from source:
```shell
pip install git+https://github.com/haiiliin/pyqtribbon.git@main
```

## The Ribbon Bar

The ribbon is first introduced by Microsoft in the 2000's. It is a toolbar with a tabbed interface. According to [Microsoft](https://docs.microsoft.com/en-us/cpp/mfc/ribbon-designer-mfc?view=msvc-170):

- A ribbon is a user interface (UI) element that organizes commands into logical groups. These groups appear on separate tabs in a strip across the top of the window. The ribbon replaces the menu bar and toolbars. A ribbon can significantly improve application usability. For more information, see Ribbons. The following illustration shows a ribbon. A ribbon can significantly improve application usability. For more information, see [Ribbons](https://docs.microsoft.com/en-us/windows/win32/uxguide/cmd-ribbons). The following illustration shows a ribbon.
  
  ![ribbon_no_callouts](docs/source/_images/ribbon_no_callouts.png)

## Definitions of Ribbon Elements

- **Application button**: The button that appears on the upper-left corner of a ribbon. The Application button replaces the File menu and is visible even when the ribbon is minimized. When the button is clicked, a menu that has a list of commands is displayed.

- **Quick Access toolbar**: A small, customizable toolbar that displays frequently used commands.

- **Category**: The logical grouping that represents the contents of a ribbon tab.

- **Category Default button**: The button that appears on the ribbon when the ribbon is minimized. When the button is clicked, the category reappears as a menu.

- **Panel**: An area of the ribbon bar that displays a group of related controls. Every ribbon category contains one or more ribbon panels.

- **Ribbon elements**: Controls in the panels, for example, buttons and combo boxes. To see the various controls that can be hosted on a ribbon, see RibbonGadgets Sample: Ribbon Gadgets Application.

## Screenshots

![An Example](screenshots/main.png)
