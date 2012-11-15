from PyQt4.QtGui import QGraphicsScene, QColor, QBrush
from PyQt4 import QtCore

class NodeViewScene(QGraphicsScene):
    def __init__(self):
        super(NodeViewScene, self).__init__()
        
        backgroundBrush = QBrush(QColor(0, 0, 0, 20))
        backgroundBrush.setStyle(QtCore.Qt.CrossPattern)
        self.setBackgroundBrush(backgroundBrush)