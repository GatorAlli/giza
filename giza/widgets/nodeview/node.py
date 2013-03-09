from PyQt4.QtGui import (QGraphicsItem, QGraphicsPathItem, QColor, QPen, QBrush, 
                         QGraphicsDropShadowEffect, QFont, QRadialGradient,
                         QPainterPath)
from PyQt4.QtCore import (QRectF, Qt, QPointF, QPropertyAnimation, QEasingCurve,
                         QObject, pyqtProperty)


class Node(QGraphicsItem):
    """
    Node
    """
    
    def __init__(self):
        super(Node, self).__init__()
        
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        
        self.title = ""
        self.width, self.height = 150, 180
        self.headerSize = 14
        self.shadowBlurRadius = 20
        
        self.backgroundColor     = QColor( 120, 120, 120, 230 )
        self.normalBorderColor   = QColor(  15,  15,  15,  64 )
        self.selectedBorderColor = QColor( 255, 191,   0, 102 )
        self.textColor           = QColor(  30,  30,  30, 255 )
        self.shadowColor         = QColor(   0,   0,   0, 255 )
        self.selectedShadowColor = QColor( 100, 100, 100, 255 )
        
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(self.shadowBlurRadius)
        self.shadow.setOffset(0, 0)
        self.setGraphicsEffect(self.shadow)
        
        self.pen   = QPen()
        self.brush = QBrush(Qt.SolidPattern)
        self.font  = QFont()
        self.pen.setWidth(1)
        self.brush.setColor(self.backgroundColor)
        self.font.setPointSize(10)
        
        self.ports = []
        
    def itemChange(self, change, value):
        """
        Triggers different actions based on changes within the QGraphicsItem.
        """
        if change == QGraphicsItem.ItemSelectedHasChanged:
            self.setSelected(value.toBool())
        if change == QGraphicsItem.ItemPositionHasChanged:
            [port.updateConnections() for port in self.ports]
            
        return super(Node, self).itemChange(change, value)
    
    def setSelected(self, selected):
        if selected:
            # Node was selected
            self.shadow.setColor(self.selectedShadowColor)
        else:
            # Node was deselected
            self.shadow.setColor(self.shadowColor)
            
    def boundingRect(self):
        """
        Returns a bounding rect based on defined width and height.
        """
        return QRectF(0, 0, self.width, self.height).adjusted(
            -self.shadowBlurRadius, -self.shadowBlurRadius, 
             self.shadowBlurRadius,  self.shadowBlurRadius)
    
    def paint(self, painter, option, widget):
        """
        Paint method for the QGraphicsItem
        """
        # Draw base rectangle
        
        if self.isSelected():
            self.pen.setColor(self.selectedBorderColor)
        else:
            self.pen.setColor(self.normalBorderColor)
            
        painter.setPen(self.pen)
        painter.setFont(self.font)
        painter.setBrush(self.brush)
        painter.drawRoundedRect(0, 0, self.width, self.height, 4, 4)
        
        # Draw title text
        
        painter.setPen(self.textColor)
        painter.drawText(10, 20, self.title)
    
    def addPort(self, port):
        """
        Adds a port.
        
        Retrieves rows pertaining to the given keys from the Table instance 
        represented by big_table.  Silly things may happen if 
        other_silly_variable is not None.
        
        Args:
            port (NodePort): the port to add.
        """
        self.ports.append(port)
        port.setParentItem(self)
        self.updatePorts()
        
    def removePort(self, port):
        """Removes a port.

        :param port: the port to remove
        """
        self.ports.remove(port)
        self.updatePorts()
        
    def updatePorts(self):
        for i, port in enumerate(self.ports):
            port.width = self.width + 12 * 2 + 12
            port.setPos(0 - 12 - 6, 30 + i * 30)
    
    @property
    def inputPorts(self):
        """
        Returns a list of owned input ports.
        """
        return [port for port in self.ports if port.isInput()]
    
    @property
    def outputPorts(self):
        """
        Returns a list of owned output ports.
        """
        return [port for port in self.ports if port.isOutput()]
        
    def getImmediateAncestors(self):
        """
        Returns a list of the nodes immediate ancestors.
        
        Retrieves the nodes that are directly connected to any of the node's 
        input ports. With this node graph::
        
            [D]
                > [B]
            [E]       > [A]
                  [C]
        
        Getting the immediate ancestors of [A] would return [[B], [C]].
        """
        ancestors = []
        for port in self.inputPorts:
            for port in port.connectedPorts:
                ancestors.append(port.parentItem())
        return ancestors
    
    def getAllAncestors(self, source=None):
        """
        Returns a list of the nodes ancestors.
        
        Retrieves the nodes that are implicitly and explicitly connected to any 
        of the node's input ports. With this node graph::
        
            [D]
                > [B]
            [E]       > [A]
                  [C]
        
        Getting the ancestors of [A] would return [[B], [C], [D], [E]].""" 
        if not source:
            source = self
        
        ancestors = []
        for ancestor in self.getImmediateAncestors():
            if ancestor not in ancestors and ancestor is not source:
                ancestors.append(ancestor)
                ancestors.extend(ancestor.getAllAncestors(source))
                
        return ancestors
        
class AnimationAdapter(QObject):
    def __init__(self, parent, obj):
        super(AnimationAdapter, self).__init__()
        self.obj = obj
        
    def __get_opacity(self):
        return self.obj.opacity()
    
    def __set_opacity(self, opacity):
        return self.obj.setOpacity(opacity)
    
    opacity = pyqtProperty(float, __get_opacity, __set_opacity)
        
class NodeConnector(QGraphicsPathItem):
    def __init__(self, sourcePort=None, destinationPort=None):
        super(NodeConnector, self).__init__()
        
        self.adapter     = AnimationAdapter(self, self)
        self.lastPort    = None
        self.points      = None
        self.valid       = False
        self.active      = False
        self.source      = sourcePort
        self.destination = destinationPort
        self.pen         = QPen(QColor(30, 30, 30, 200), 2)

        self.setPen(self.pen)
        self.setZValue(-1)
        
        # Animations
        self.fadeInAnimation = QPropertyAnimation(self.adapter, "opacity")
        self.fadeInAnimation.setDuration(300)
        self.fadeInAnimation.setStartValue(0.5)
        self.fadeInAnimation.setEndValue(1.0)
        self.fadeInAnimation.setEasingCurve(QEasingCurve.InOutQuad)
        
        self.fadeOutAnimation = QPropertyAnimation(self.adapter, "opacity")
        self.fadeOutAnimation.setDuration(300)
        self.fadeOutAnimation.setStartValue(1.0)
        self.fadeOutAnimation.setEndValue(0.5)
        self.fadeOutAnimation.setEasingCurve(QEasingCurve.InOutQuad)
        
        self.updatePath()
        
        # Start animation
        self.setOpacity(0.5)
        self.fadeInAnimation.start()
    
    def animateOpacity(self):
        self.anim = QPropertyAnimation(self.adapter, "opacity")
        self.anim.setDuration(300)
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.5)
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.anim.start()
        
    def getPoint(self, item):
        if isinstance(item, NodePort):
            point = item.scenePos() + item.getPortBoundingRect().center()
        else:
            point = item
            
        return point
    
    def updatePoints(self):
        if self.source and self.destination:
            if self.startPoint is self.source:
                self.points = [self.getPoint(self.source), 
                               self.getPoint(self.destination)]
            else:
                self.points = [self.getPoint(self.destination),
                               self.getPoint(self.source)]

    def updatePath(self):
        if self.points and self.points[0] and self.points[1]:
            pos1, pos2 = self.points
            path = QPainterPath()
            path.moveTo(pos1)
            
            e = 0.5
            f = 1
            if self.startPoint.isInput():
                f = -1
                
            dx = pos2.x() - pos1.x()
            dy = pos2.y() - pos1.y()
                
            ctrl1 = QPointF(pos1.x() + abs(dx) * e * f, pos1.y())
            ctrl2 = QPointF(pos2.x() - abs(dx) * e * f, pos1.y() + dy)
            
            path.cubicTo(ctrl1, ctrl2, pos2)
            
            self.setPath(path)
    
    def setStartPoint(self, port):
        if port.isInput():
            self.destination = port
        else:
            self.source = port
        self.startPoint = port
        
    def setEndPoint(self, port):
        if isinstance(port, QPointF):
            self.valid = False
            
            if self.lastPort:
                self.lastPort.setHighlight(False)
                self.lastPort = None
                
            if self.startPoint.isInput():
                self.source = port
            else:
                self.destination = port
                
            self.updatePoints()
            
        elif self.isConnectionValid(self.startPoint, port):
            self.valid = True
            if self.startPoint.isInput():
                self.source = port
            else:
                for connection in port.connections:
                    connection.fadeOutAnimation.start()
                self.destination = port
            port.setHighlight(True)
            self.lastPort = port
            self.updatePoints()
            
        else:
            self.valid = False
    
    def connectNodes(self):
        if self.valid:
            self.source.connectTo(self.destination, self)
            self.destination.removeConnections()
            self.destination.connectTo(self.source, self)
        else:
            self.delete()
    
    def isConnectionValid(self, port1, port2):
        valid = False
        if isinstance(port1, NodePort) and isinstance(port2, NodePort):
            cyclic = False
            if port1.isInput():
                cyclic = port1.parentItem() in port2.parentItem().getAllAncestors()
            else:
                cyclic = port2.parentItem() in port1.parentItem().getAllAncestors()
                
            valid = (port1 is not port2 and 
                isinstance(port1, NodePort) and isinstance(port2, NodePort) and
                port1.parentItem() is not port2.parentItem() and 
                port1.direction is not port2.direction and 
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
                
        self.label     = label or portType["label"]
        self.type      = portType
        self.direction = direction
        
        self.pen = QPen(QColor(30, 30, 30, 255*.25))
        self.pen.setWidth(1)
        
        self.setColor(portType["color"])
        
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
        
        if not self.connector.valid:
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
        
        if self.isInput():
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
    
    def isInput(self):
        return self.direction == NodePort.INPUT

    def isOutput(self):
        return self.direction == NodePort.OUTPUT

    def connectTo(self, port, connection):
        self.connections[connection] = port
        
    @property
    def connectedPorts(self):
        return self.connections.values()
    
    def removeConnection(self, connection):
        self.connections.pop(connection)
        
    def removeConnections(self):
        connections = []
        for connection, port in self.connections.iteritems():
            connections.append(connection)
            port.removeConnection(connection)
            connection.delete()
        [self.removeConnection(connection) for connection in connections]
        self.connections.clear()
    
    def hasConnections(self):
        return len(self.connections) is not 0
    
    def updateConnections(self):
        for connection in self.connections.keys():
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
        if self.isOutput():
            alignment = Qt.AlignRight
            
        painter.drawText(textRect, alignment | Qt.AlignVCenter, self.label)
        
        