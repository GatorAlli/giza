from PyQt4.QtGui import (QGraphicsItem, QColor, QPen, QBrush, 
                         QGraphicsDropShadowEffect)
from PyQt4.QtCore import QRectF

class Node(QGraphicsItem):
    def __init__(self):
        super(Node, self).__init__(self)
        
        self.normalBorderColor = QColor(15, 15, 15, 255*.25)
        self.selectedBorderColor = QColor(255, 255, 255, 255*.4)
        
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(20)
        self.shadow.setOffset(0, 0)
        self.setGraphicsEffect(self.shadow)
        
        self.pen = QPen()
        self.pen.setWidth(1)
        self.brush = QBrush(QColor(120, 120, 120, 255*.75))

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSelectedHasChanged:
            self.setSelected(value)
        return QGraphicsItem.itemChange(self, change, value)
    
    def setSelected(self, selected):
        if selected.toBool():
            self.shadow.setColor(QColor(100, 100 ,100, 255))
            self.setBorderColor(self.selectedBorderColor)
        else:
            self.shadow.setColor(QColor(0, 0 ,0, 255))
            self.setBorderColor(self.normalBorderColor)
            
    def boundingRect(self):
        return QRectF(0, 0, 150, 200)
    
    def paint(self, painter, option, widget):
        width, height = self.boundingRect().width(), self.boundingRect().height()
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        
        painter.drawRoundedRect(1, 1, width - 1, height - 1, 4, 4)
    
    def setBorderColor(self, borderColor):
        self.pen.setColor(borderColor)
        