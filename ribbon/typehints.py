import typing


class PyQtSignalType(typing.Protocol):
    """This is a protocol for the pyqt signal type."""
    def connect(self, slot): ...
    def disconnect(self, slot): ...
    def emit(self, *args): ...


class PyQtActionType(typing.Protocol):
    """This is a protocol for the pyqt action type."""
    triggered: PyQtSignalType
