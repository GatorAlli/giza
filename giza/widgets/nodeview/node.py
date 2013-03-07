from PyQt4.QtGui import (QGraphicsItem, QGraphicsPathItem, QColor, QPen, QBrush, 
                         QGraphicsDropShadowEffect, QFont, QRadialGradient,
                         QPainterPath)
from PyQt4.QtCore import QRectF, Qt, QPointF


class Node(QGraphicsItem):
    def __init__(self):
        super(Node, self).__init__()
        
        self.title = ""
        self.width, self.height = 150, 180
        
        self.backgroundColor = QColor(120, 120, 120, 255*.9)
        self.normalBorderColor = QColor(15, 15, 15, 255*.25)
        self.selectedBorderColor = QColor(255, 255*.75, 0, 255*.4)
        self.textColor = QColor(30, 30, 30)
        self.headerSize = 14
        
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
                
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
        
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSelectedHasChanged:
            self.setSelected(value)
        if change == QGraphicsItem.ItemPositionHasChanged:
            for port in self.getPorts():
                port.updateConnections()
        return super(Node, self).itemChange(change, value)
    
    def setSelected(self, selected):
        if selected.toBool():
            self.shadow.setColor(QColor(100, 100, 100, 255))
        else:
            self.shadow.setColor(QColor(0, 0, 0, 255))
            
    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)
    
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
        painter.drawText(10, 20, self.title)
    
    def addPort(self, port):
        self.ports.append(port)
        port.setParentItem(self)
        self.updatePorts()
        
    def removePort(self, port):
        self.ports.remove(port)
        self.updatePorts()
        
    def updatePorts(self):
        for i, port in enumerate(self.ports):
            port.width = self.width + 12 * 2 + 12
            port.setPos(0 - 12 - 6, 30 + i * 30)
    
    def getInputPorts(self):
        return [port for port in self.ports 
                if port.getDirection() == NodePort.INPUT]
        
    def getPorts(self):
        return self.ports
    
    def getOutputPorts(self):
        return [port for port in self.ports 
                if port.getDirection() == NodePort.OUTPUT]
        
    def getImmediateAncestors(self):
        ancestors = []
        for port in self.getInputPorts():
            for port in port.getConnectedPorts():
                ancestors.append(port.parentItem())
        return ancestors
    
    def getAllAncestors(self):
        ancestors = []
        for ancestor in self.getImmediateAncestors():
            if ancestor not in ancestors:
                ancestors.append(ancestor)
                ancestors.extend(ancestor.getAllAncestors())
        return ancestors
            
    def setTitle(self, title):
        self.title = title
    
    def mousePressEvent(self, event):
        return super(Node, self).mousePressEvent(event)
        
class NodeConnector(QGraphicsPathItem):
    def __init__(self, sourcePort=None, destinationPort=None):
        super(NodeConnector, self).__init__()
        
        self.lastPort = None
        self.points = None
        self.setValid(False)
        self.setActive(False)
        self.setSource(sourcePort)
        self.setDestination(destinationPort)
        
        self.setPen(QPen(QColor(30, 30, 30, 200), 2))
        self.setZValue(-1)
        
        self.updatePath()
        
    def getPoint(self, item):
        if isinstance(item, NodePort):
            point = item.scenePos() + item.getPortBoundingRect().center()
        else:
            point = item
        return point
    
    def updatePoints(self):
        source, destination = self.getSource(), self.getDestination()
        if source and destination:
            if self.startPoint is source:
                self.points = [self.getPoint(source), 
                               self.getPoint(destination)]
            else:
                self.points = [self.getPoint(destination),
                               self.getPoint(source)]
    
    def getPoints(self):
        return self.points

    def updatePath(self):
        points = self.getPoints()
        if points and points[0] and points[1]:
            pos1, pos2 = points[0], points[1]
            path = QPainterPath()
            path.moveTo(pos1)
            
            e = 0.5
            f = 1
            if self.startPoint.getDirection() is NodePort.INPUT:
                f = -1
                
            dx = pos2.x() - pos1.x()
            dy = pos2.y() - pos1.y()
                
            ctrl1 = QPointF(pos1.x() + abs(dx) * e * f, pos1.y())
            ctrl2 = QPointF(pos2.x() - abs(dx) * e * f, pos1.y() + dy)
            
            path.cubicTo(ctrl1, ctrl2, pos2)
            
            self.setPath(path)
    
    def isActive(self):
        return self.active
    
    def setActive(self, active):
        self.active = active
    
    def isValid(self):
        return self.valid
    
    def setValid(self, valid):
        self.valid = valid
        
    def setSource(self, source):
        self.source = source
    
    def getSource(self):
        return self.source
    
    def setDestination(self, destination):
        self.destination = destination
    
    def getDestination(self):
        return self.destination
    
    def setStartPoint(self, port):
        if port.getDirection() is NodePort.INPUT:
            self.setDestination(port)
        else:
            self.setSource(port)
        self.startPoint = port
        
    def setEndPoint(self, port):
        if isinstance(port, QPointF):
            self.setValid(False)
            
            if self.lastPort:
                self.lastPort.setHighlight(False)
                self.lastPort = None
                
            if self.startPoint.getDirection() is NodePort.INPUT:
                self.setSource(port)
            else:
                self.setDestination(port)
                
            self.updatePoints()
            
        elif self.isConnectionValid(self.startPoint, port):
            self.setValid(True)
            if self.startPoint.getDirection() is NodePort.INPUT:
                self.setSource(port)
            else:
                self.setDestination(port)
            port.setHighlight(True)
            self.lastPort = port
            self.updatePoints()
            
        else:
            self.setValid(False)
    
    def connectNodes(self):
        if self.isValid():
            source      = self.getSource()
            destination = self.getDestination()
            source.connectTo(destination, self)
            destination.removeConnections()
            destination.connectTo(source, self)
        else:
            self.delete()
    
    def isConnectionValid(self, port1, port2):
        valid = False
        if isinstance(port1, NodePort) and isinstance(port2, NodePort):
            cyclic = False
            if port1.getDirection() is NodePort.INPUT:
                cyclic = port1.parentItem() in port2.parentItem().getAllAncestors()
            else:
                cyclic = port2.parentItem() in port1.parentItem().getAllAncestors()
                
            valid = (port1 is not port2 and 
                isinstance(port1, NodePort) and isinstance(port2, NodePort) and
                port1.parentItem() is not port2.parentItem() and 
                port1.getDirection() is not port2.getDirection() and 
                not cyclic) # no two inputs on the same node one input dismatles the other, check blender
        return valid
        
    def delete(self):
        self.setParentItem(None)
        self.scene().removeItem(self)
    
class NodePort(QGraphicsItem):
    
    INPUT  = "input"
    OUTPUT = "output"
    
    COLOR  = {
        "color": "#ccc",
        "label": "Color"
    }
    VALUE  = {
        "color": "#356",
        "label": "Value"
    }
    PIXMAP = {
        "color": "#ff4",
        "label": "Image"
    }
    
    def __init__(self, portType=VALUE, direction=INPUT, label=None):
        super(NodePort, self).__init__()
        self.setAcceptHoverEvents(True)
                
        self.textColor = QColor(30, 30, 30)
        self.font = QFont()
        self.font.setPointSize(10)
        
        self.radius = 6
        self.padding = 12
        self.width, self.height = 150 + self.radius * 2 + self.padding * 2, 30
        self.connections = {}
        self.highlighted = False
                
        self.setLabel(label or portType["label"])
        self.setType(portType)
        self.setDirection(direction)
        
        self.pen = QPen(QColor(30, 30, 30, 255*.25))
        self.pen.setWidth(1)
        
        self.setColor(portType["color"])
    
    def setLabel(self, label):
        self.label = label
        
    def getLabel(self):
        return self.label
    
    def setType(self, portType):
        self.type = portType
    
    def getType(self):
        return self.type
    
    def setDirection(self, direction):
        self.direction = direction
        
    def getDirection(self):
        return self.direction
        
    def setColor(self, color):
        self.color  = QColor(color)
        darkerColor = self.color.darker(110)
        
        gradient = QRadialGradient(self.getPortBoundingRect().center(), 6)
        gradient.setColorAt(0, self.color)
        gradient.setColorAt(1, darkerColor)
        self.brush = QBrush(gradient)
        
        self.highlightBrush = QBrush(self.color.lighter(105))
        
    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)
    
    def mousePressEvent(self, event):
        self.connector = NodeConnector()
        self.connector.setStartPoint(self)
        self.scene().addItem(self.connector)
    
    def mouseMoveEvent(self, event):
        scenePos = event.scenePos()
        nodePort = self.scene().itemAt(scenePos)
        self.connector.setEndPoint(nodePort)
        
        if not self.connector.isValid():
            self.connector.setEndPoint(scenePos)
        
        self.connector.updatePath()
        
    def mouseReleaseEvent(self, event):
        self.connector.connectNodes()
        
    def hoverEnterEvent(self, event):
        self.setHighlight(True)
        
    def hoverLeaveEvent(self, event):
        self.setHighlight(False)
        
    def getPortBoundingRect(self):
        x = self.boundingRect().width() - self.radius * 2.0 - self.padding
        y = self.boundingRect().height() / 2.0 - self.radius
        
        if self.getDirection() is NodePort.INPUT:
            x = self.padding
        
        diameter = self.radius * 2
        return QRectF(x, y, diameter, diameter)
        
    def shape(self):
        path = QPainterPath()
        p = self.padding
        path.addEllipse(self.getPortBoundingRect().adjusted(-p, -p, p, p))
        return path
    
    def setHighlight(self, value):
        self.highlighted = value
        self.update()
        
    def isHighlighted(self):
        return self.highlighted
    
    def connectTo(self, port, connection):
        self.connections[connection] = port
        
    def getConnectedPorts(self):
        return self.connections.values()
    
    def removeConnection(self, connection):
        self.connections.pop(connection)
        
    def removeConnections(self):
        connections = []
        for connection, port in self.getConnections().iteritems():
            connections.append(connection)
            port.removeConnection(connection)
            connection.delete()
        [self.removeConnection(connection) for connection in connections]
        self.connections.clear()
        
    def getConnections(self):
        return self.connections
    
    def hasConnections(self):
        return len(self.getConnections()) is not 0
    
    def updateConnections(self):
        for connection in self.getConnections().keys():
            connection.updatePoints()
            connection.updatePath()
            
    def paint(self, painter, option, widget):
        painter.setPen(self.pen)
        
        painter.setBrush(self.brush)
        if self.isHighlighted():
            painter.setBrush(self.highlightBrush)
            
        painter.setFont(self.font)
        
        painter.drawEllipse(self.getPortBoundingRect())
        
        painter.setPen(self.textColor)
        textRect = self.boundingRect()
        n = 12*3 + 20
        textRect.setWidth(textRect.width() - n)
        textRect.moveLeft(n / 2.0)
        
        alignment = Qt.AlignLeft
        if self.getDirection() is NodePort.OUTPUT:
            alignment = Qt.AlignRight
            
        painter.drawText(textRect, alignment | Qt.AlignVCenter, self.getLabel())
        
        