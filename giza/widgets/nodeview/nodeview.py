import sys
from PyQt4.QtGui import QGraphicsView, QApplication, QPainter

from nodeviewscene import NodeViewScene

class NodeView(QGraphicsView):
    def __init__(self):
        super(NodeView, self).__init__()
        
        # self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setRenderHint(QPainter.Antialiasing)
        self.setScene(NodeViewScene())