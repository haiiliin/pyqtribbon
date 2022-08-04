===========
User Manual
===========

The RibbonScreenShotWindow Class
--------------------------------

The :py:class:`~ribbon.screenshotwindow.RibbonScreenShotWindow` class is just for taking a screenshot of the window, 
the window will be closed 0.1s after it is shown. It is just used for documenting the window.

.. autoclass:: ribbon.screenshotwindow.RibbonScreenShotWindow
    :members:

Instantiate a Ribbon Bar
--------------------------

:py:class:`~ribbon.ribbonbar.RibbonBar` is inherited from :py:class:`~PyQt5.QtWidgets.QMenuBar`,
you can use the `setMenuBar` method of :py:class:`~PyQt5.QtWidgets.QMainWindow` to set the ribbon bar as the main menu bar. 

.. code-block:: python

    ...
    from pyqtribbon import RibbonBar

    window = QtWidgets.QMainWindow()
    ribbon = RibbonBar()
    window.setMenuBar(ribbon)
    ...

Example
~~~~~~~

For example, using the following code,

.. exec_code::
    :filename: _screenshots/ribbonbar.py

You can get a window like this:

.. image:: _screenshots/ribbonbar.png
    :align: center
    :width: 100%

Customize Ribbon Bar
--------------------

General Setups
~~~~~~~~~~~~~~

.. currentmodule:: ribbon.ribbonbar

.. autosummary::

    RibbonBar.setRibbonStyle
    RibbonBar.ribbonHeight
    RibbonBar.setRibbonHeight
    RibbonBar.showRibbon
    RibbonBar.hideRibbon
    RibbonBar.ribbonVisible
    RibbonBar.setRibbonVisible

Setup Application Button
~~~~~~~~~~~~~~~~~~~~~~~~

.. currentmodule:: ribbon.ribbonbar

.. autosummary::

    RibbonBar.applicationOptionButton
    RibbonBar.setApplicationIcon
    RibbonBar.addFileMenu

Setup Title
~~~~~~~~~~~

.. currentmodule:: ribbon.ribbonbar

.. autosummary::

    RibbonBar.title
    RibbonBar.setTitle
    RibbonBar.addTitleWidget
    RibbonBar.insertTitleWidget
    RibbonBar.removeTitleWidget

Setup Category Tab Bar
~~~~~~~~~~~~~~~~~~~~~~

.. currentmodule:: ribbon.ribbonbar

.. autosummary::

    RibbonBar.tabBar
    RibbonBar.tabBarHeight
    RibbonBar.setTabBarHeight

Setup Quick Access Bar
~~~~~~~~~~~~~~~~~~~~~~

.. currentmodule:: ribbon.ribbonbar

.. autosummary::

    RibbonBar.quickAccessToolBar
    RibbonBar.addQuickAccessButton
    RibbonBar.setQuickAccessButtonHeight

Setup Right Tool Bar
~~~~~~~~~~~~~~~~~~~~

.. currentmodule:: ribbon.ribbonbar

.. autosummary::

    RibbonBar.rightToolBar
    RibbonBar.addRightToolButton
    RibbonBar.setRightToolBarHeight
    RibbonBar.setHelpButtonIcon
    RibbonBar.removeHelpButton
    RibbonBar.helpButtonClicked
    RibbonBar.collapseRibbonButton
    RibbonBar.setCollapseButtonIcon
    RibbonBar.removeCollapseButton

Example
~~~~~~~

For example, using the following code,

.. exec_code::
    :filename: _screenshots/ribbonbar-customize.py

You can get a window like this:

.. image:: _screenshots/ribbonbar-customize.png
    :align: center
    :width: 100%

Manage Categories
~~~~~~~~~~~~~~~~~

.. currentmodule:: ribbon.ribbonbar

.. autosummary::

    RibbonBar.categories
    RibbonBar.addCategory
    RibbonBar.addCategoriesBy
    RibbonBar.addNormalCategory
    RibbonBar.addContextCategory
    RibbonBar.addContextCategories
    RibbonBar.showContextCategory
    RibbonBar.hideContextCategory
    RibbonBar.removeCategory
    RibbonBar.setCurrentCategory
    RibbonBar.currentCategory
    RibbonBar.showCategoryByIndex

Customize Categories
--------------------

Setup Styles
~~~~~~~~~~~~

.. currentmodule:: ribbon.category

.. autosummary::

    RibbonCategory.categoryStyle
    RibbonCategory.setCategoryStyle

Manage Panels
~~~~~~~~~~~~~

.. currentmodule:: ribbon.category

.. autosummary::

    RibbonCategory.addPanel
    RibbonCategory.addPanelsBy
    RibbonCategory.removePanel
    RibbonCategory.takePanel
    RibbonCategory.panel
    RibbonCategory.panels

Example
~~~~~~~

For example, using the following code,

.. exec_code::
    :filename: _screenshots/category.py

You can get a window like this:

.. image:: _screenshots/category.png
    :align: center
    :width: 100%

Customize Panels
----------------

Setup Title Label
~~~~~~~~~~~~~~~~~

.. currentmodule:: ribbon.panel

.. autosummary::

    RibbonPanel.title
    RibbonPanel.setTitle

Setup Panel Option Button
~~~~~~~~~~~~~~~~~~~~~~~~~

.. currentmodule:: ribbon.panel

.. autosummary::

    RibbonPanel.panelOptionButton
    RibbonPanel.setPanelOptionToolTip
    RibbonPanel.panelOptionClicked

Add Widgets to Panels
~~~~~~~~~~~~~~~~~~~~~

.. currentmodule:: ribbon.panel

.. autosummary::

    RibbonPanel.addWidget
    RibbonPanel.addWidgetsBy
    RibbonPanel.removeWidget
    RibbonPanel.widget
    RibbonPanel.widgets
    RibbonPanel.addSmallWidget
    RibbonPanel.addMediumWidget
    RibbonPanel.addLargeWidget
    RibbonPanel.addButton
    RibbonPanel.addSmallButton
    RibbonPanel.addMediumButton
    RibbonPanel.addLargeButton
    RibbonPanel.addToggleButton
    RibbonPanel.addSmallToggleButton
    RibbonPanel.addMediumToggleButton
    RibbonPanel.addLargeToggleButton
    RibbonPanel.addComboBox
    RibbonPanel.addFontComboBox
    RibbonPanel.addLineEdit
    RibbonPanel.addTextEdit
    RibbonPanel.addPlainTextEdit
    RibbonPanel.addLabel
    RibbonPanel.addProgressBar
    RibbonPanel.addSlider
    RibbonPanel.addSpinBox
    RibbonPanel.addDoubleSpinBox
    RibbonPanel.addDateEdit
    RibbonPanel.addTimeEdit
    RibbonPanel.addDateTimeEdit
    RibbonPanel.addTableWidget
    RibbonPanel.addTreeWidget
    RibbonPanel.addListWidget
    RibbonPanel.addCalendarWidget
    RibbonPanel.addSeparator
    RibbonPanel.addHorizontalSeparator
    RibbonPanel.addVerticalSeparator
    RibbonPanel.addGallery

Example
~~~~~~~

For example, using the following code,

.. exec_code::
    :filename: _screenshots/panel.py

You can get a window like this:

.. image:: _screenshots/panel.png
    :align: center
    :width: 100%

A Complete Example
------------------

The following code snippet is a complete example.

.. literalinclude:: tutorial-ribbonbar.py
    :language: python

It would be rendered as follows:

.. image:: _images/example.png
    :align: center
    :width: 100%
