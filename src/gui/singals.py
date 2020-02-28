from PySide2.QtCore import Signal, QObject

class PcMoveSignal(QObject):
    sig = Signal(list, list, list)

class UserMoveSignal(QObject):
    sig = Signal(str)
