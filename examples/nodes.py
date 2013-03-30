import sys
from PyQt4.QtGui import QApplication
from giza.widgets import NodeView, Dial
from giza.nodetypes.input import ColorInputNode, ValueInputNode
from giza.nodetypes.convert import MixNode

import random


if __name__ == "__main__":
    app = QApplication(sys.argv)

    nodeViewWidget = NodeView()
    
    nodeRange = 1000
    for x in range(8):
        node = MixNode()
        node.setPos(random.random() * nodeRange - nodeRange / 2,
                    random.random() * nodeRange - nodeRange / 2)
        nodeViewWidget.scene().addItem(node)
    """for x in range(2):
        node = ColorInputNode()
        node.setPos(random.random() * nodeRange - nodeRange / 2,
                    random.random() * nodeRange - nodeRange / 2)
        nodeViewWidget.scene().addItem(node)
    for x in range(2):
        node = ValueInputNode()
        node.setPos(random.random() * nodeRange - nodeRange / 2,
                    random.random() * nodeRange - nodeRange / 2)
        nodeViewWidget.scene().addItem(node)"""
    
    node = MixNode()
    dial = Dial()
    node.setPos(0, 0)
    dial.setPos(0, 0)
    nodeViewWidget.scene().addItem(node)
    nodeViewWidget.scene().addItem(dial)
    #nodeViewWidget.scale(2, 2)
    '''
    for _ in range(1):
        node1 = MixNode()
        node1.setPos(0, 0)
        nodeViewWidget.scene().addItem(node1)
        
    node2 = ColorInputNode()
    node2.setPos(400, 100)
    
    node3 = MixNode()
    node3.setPos(200, 130)
    
    nodeViewWidget.scene().addItem(node2)
    nodeViewWidget.scene().addItem(node3)
    '''
    nodeViewWidget.setWindowTitle("NodeView")
    nodeViewWidget.show()
    sys.exit(app.exec_())