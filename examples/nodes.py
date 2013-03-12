import sys
from PyQt4.QtGui import QApplication
from giza.widgets import NodeView
from giza.nodetypes.input import ColorInputNode, NumberInputNode
from giza.nodetypes.convert import MixNode
import random


if __name__ == "__main__":
    app = QApplication(sys.argv)

    nodeViewWidget = NodeView()
    
    nodeRange = 1000
    for x in range(4):
        node = MixNode()
        node.setPos(random.random() * nodeRange - nodeRange / 2,
                    random.random() * nodeRange - nodeRange / 2)
        nodeViewWidget.scene().addItem(node)
    for x in range(4):
        node = ColorInputNode()
        node.setPos(random.random() * nodeRange - nodeRange / 2,
                    random.random() * nodeRange - nodeRange / 2)
        nodeViewWidget.scene().addItem(node)
    for x in range(4):
        node = NumberInputNode()
        node.setPos(random.random() * nodeRange - nodeRange / 2,
                    random.random() * nodeRange - nodeRange / 2)
        nodeViewWidget.scene().addItem(node)
    
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