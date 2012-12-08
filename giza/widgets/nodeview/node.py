from PyQt4.QtGui import (QGraphicsItem, QGraphicsPathItem, QColor, QPen, QBrush, 
                         QGraphicsDropShadowEffect, QFont, QRadialGradient,
                         QPainterPath)
from PyQt4.QtCore import QRectF, Qt, QPointF


class Node(QGraphicsItem):
    def __init__(self):
        super(Node, self).__init__()
        
        self.title = ""
        
        self.backgroundColor = QColor(120, 120, 120, 255*.9)
        self.normalBorderColor = QColor(15, 15, 15, 255*.25)
        self.selectedBorderColor = QColor(255, 255*.75, 0, 255*.4)
        self.textColor = QColor(30, 30, 30)
        self.headerSize = 14
        
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(20)
        self.shadow.setOffset(0, 0)
        self.setGraphicsEffect(self.shadow)
        
        self.pen = QPen()
        self.pen.setWidth(1)
        self.brush = QBrush(Qt.SolidPattern)
        self.font = QFont()
        self.font.setPointSize(10)
        
        #Ports
        self.ports = []
        
        #Random NodePorts
        self.port = NodePort()
        self.port.setParentItem(self)
        
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSelectedHasChanged:
            self.setSelected(value)
        if change == QGraphicsItem.ItemPositionChange:
            self.setSelected(value)
        return super(Node, self).itemChange(change, value)
    
    def setSelected(self, selected):
        if selected.toBool():
            self.shadow.setColor(QColor(100, 100, 100, 255))
        else:
            self.shadow.setColor(QColor(0, 0, 0, 255))
            
    def boundingRect(self):
        return QRectF(0, 0, 150, 200)
    
    def paint(self, painter, option, widget):
        width, height = self.boundingRect().width(), self.boundingRect().height()
        
        if self.isSelected():
            self.pen.setColor(self.selectedBorderColor)
        else:
            self.pen.setColor(self.normalBorderColor)
            
        painter.setPen(self.pen)
        painter.setFont(self.font)
        self.brush.setColor(self.backgroundColor)
        painter.setBrush(self.brush)
        painter.drawRoundedRect(0, 0, width, height, 4, 4)
        
        painter.setPen(self.textColor)
        painter.drawText(10, 20, "Dot Product")
    
    def addPort(self, port):
        self.ports.append(port)
        port.setParentItem(self)
        
    def removePort(self, port):
        self.ports.remove(port)
    
    def getInputPorts(self):
        return [port for port in self.ports 
                if port.getDirection() == NodePort.INPUT]
        
    def getOutputPorts(self):
        return [port for port in self.ports 
                if port.getDirection() == NodePort.OUTPUT]
        
    def setTitle(self, title):
        self.title = title
        

class NodeConnector(QGraphicsPathItem):
    def __init__(self, port1, port2):
        super(NodeConnector, self).__init__()
        
        self.port1 = port1
        self.port2 = port2
        
        self.setPen(QPen(Qt.black, 2))
        self.setZValue(-1)
        
        self.updateEndpoints()
        self.updatePath()
        
    def updateEndpoints(self):
        self.pos1 = self.port1.scenePos()
        self.pos2 = self.port2.scenePos()

    def updatePath(self):
        path = QPainterPath()
        path.moveTo(self.pos1)
        
        dx = self.pos2.x() - self.pos1.x()
        dy = self.pos2.y() - self.pos1.y()
        
        ctrl1 = QPointF(self.pos1.x() + dx * 0.25, self.pos1.y() + dy * 0)
        ctrl2 = QPointF(self.pos2.x() + dx * 0.75, self.pos2.y() + dy * 1)
        
        path.cubicTo(ctrl1, ctrl2, self.pos2)
        
        self.setPath(path)


class NodePort(QGraphicsItem):
    
    INPUT  = 0
    OUTPUT = 1
    
    Color  = 0
    Number = 1
    
    def __init__(self, portName, portType, portDirection=0):
        super(NodePort, self).__init__()
        
        self.name      = portName
        self.type      = portType
        self.direction = portDirection
        
        self.pen = QPen(QColor(30, 30, 30, 255*.25))
        self.pen.setWidth(1)
        
        gradient = QRadialGradient(6, 6, 6)
        gradient.setColorAt(0, QColor(255*.9, 255*.9, 255*.9))
        gradient.setColorAt(1, QColor(255*.80, 255*.80, 255*.80))
        self.brush = QBrush(gradient)

        self.setPos(-6, 80)
        
    def boundingRect(self):
        return QRectF(0, 0, 12, 12)
    
    def paint(self, painter, option, widget):
        width, height = self.boundingRect().width(), self.boundingRect().height()
        
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        
        painter.drawEllipse(0, 0, width, height)
        