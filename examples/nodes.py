import sys
import random
from PyQt4.QtGui import QApplication
from giza.widgets import NodeView, Node, NodeConnector
import time
if __name__ == "__main__":
    app = QApplication(sys.argv)

    nodeViewWidget = NodeView()
    '''
    nodeRange = 1000
    for x in range(10):
        node = Node()
        node.setPos(random.random() * nodeRange - nodeRange / 2,
                    random.random() * nodeRange - nodeRange / 2)
        nodeViewWidget.scene().addItem(node)
    '''
    
    node1 = Node()
    node1.setPos(0, 0)
    
    node2 = Node()
    node2.setPos(400, 100)
    
    nodeViewWidget.scene().addItem(node1)
    nodeViewWidget.scene().addItem(node2)
    
    '''connector = NodeConnector(node1.port, node2.port)
    nodeViewWidget.scene().addItem(connector)
    
    def lol():
        print time.time()
    nodeViewWidget.scene().changed.connect(connector.updatePath)
    '''
    nodeViewWidget.setWindowTitle("NodeView")
    nodeViewWidget.show()
    sys.exit(app.exec_())