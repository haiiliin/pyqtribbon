===========
User Manual
===========

Instantiating a Ribbon Bar
--------------------------

:py:class:`~ribbon.ribbonbar.RibbonBar` is the main class for creating a ribbon bar. 

To begin with, you have to initialize your PyQt application.

Using the RibbonBar
~~~~~~~~~~~~~~~~~~~

:py:class:`~ribbon.ribbonbar.RibbonBar` is  a class that implements a ribbon bar, you can use it to create a ribbon bar.

.. literalinclude:: tutorial-ribbonbar.py
    :language: python

It would be rendered as follows:

.. image:: _images/example.png
    :align: center
    :width: 100%

Using the RibbonMainWindow
~~~~~~~~~~~~~~~~~~~~~~~~~~

Alternatively, you can use the :py:class:`~ribbon.mainwindow.RibbonMainWindow` which is a QMainWindow that has a ribbon bar.

.. literalinclude:: tutorial-mainwindow.py
    :language: python

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
    RibbonBar.addApplicationOptionAction

Setup Title
~~~~~~~~~~~

.. currentmodule:: ribbon.ribbonbar

.. autosummary::

    RibbonBar.title
    RibbonBar.setTitle

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

Manage Categories
~~~~~~~~~~~~~~~~~

.. currentmodule:: ribbon.ribbonbar

.. autosummary::

    RibbonBar.categories
    RibbonBar.addCategory
    RibbonBar.addNormalCategory
    RibbonBar.addContextCategory
    RibbonBar.showContextCategory
    RibbonBar.hideContextCategory
    RibbonBar.removeCategory
    RibbonBar.setCurrentCategory

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
    RibbonCategory.removePanel
    RibbonCategory.takePanel
    RibbonCategory.panel
    RibbonCategory.panels

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
    RibbonPanel.removeWidget
    RibbonPanel.widget
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
