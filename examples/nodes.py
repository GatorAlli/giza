import sys
import random
from PyQt4.QtGui import QApplication
from giza.widgets import NodeView, Node

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    nodeViewWidget = NodeView()
    
    nodeRange = 1000
    for x in range(10):
        node = Node()
        node.setPos(random.random() * nodeRange - nodeRange / 2,
                    random.random() * nodeRange - nodeRange / 2)
        nodeViewWidget.scene().addItem(node)
            
    nodeViewWidget.setWindowTitle("NodeView")
    nodeViewWidget.show()
    sys.exit(app.exec_())