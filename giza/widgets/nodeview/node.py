from PyQt4.QtGui import *
from PyQt4.QtCore import *
import random
import time

class Node(QGraphicsWidget):
    """
    Node
    """
    
    def __init__(self):
        super(Node, self).__init__()
        
        # QGraphicsItem Flags
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        
        # Nodegraph Definitions
        self.ports = []
        
        # Layout
        layout = QGraphicsLinearLayout(Qt.Vertical)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Title Bar
        self.titleBar = NodeTitleBar()
        self.layout().addItem(self.titleBar)
        
        # Handle Bar
        self.handleBar = NodeHandleBar()
        self.layout().addItem(self.handleBar)

        # Colors
        self.backgroundColor     = QColor( 120, 120, 120, 230 )
        self.normalBorderColor   = QColor(  15,  15,  15,  64 )
        self.selectedBorderColor = QColor( 255, 191,   0, 102 )
        self.textColor           = QColor(  30,  30,  30, 255 )
        self.shadowColor         = QColor(   0,   0,   0, 255 )
        self.selectedShadowColor = QColor( 100, 100, 100, 255 )

        # Settings
        self.title = "Node"
        self.shadowBlurRadius = 20
        self.setMinimumWidth(150)
        self.setPreferredSize(200, -1)

        # Drop Shadow
        '''self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(self.shadowBlurRadius)
        self.shadow.setOffset(0, 0)
        self.shadow.setColor(self.shadowColor)
        self.setGraphicsEffect(self.shadow)'''
        
        # Painter Definitions
        self.pen   = QPen()
        self.brush = QBrush(Qt.SolidPattern)
        self.font  = QFont()
        self.pen.setWidth(1)
        self.pen.setColor(self.normalBorderColor)
        self.brush.setColor(self.backgroundColor)
        self.font.setPointSize(10)
        
        self.resizing = False
        
    def itemChange(self, change, value):
        """
        Overrides QGraphicsItem's boundingRect() virtual public function to 
        trigger different actions based on changes within the QGraphicsItem.
        """
        if change == QGraphicsItem.ItemSelectedHasChanged:
            self.setSelected(value.toBool())
        if change == QGraphicsItem.ItemPositionHasChanged:
            self.updateConnections()
            
        return super(Node, self).itemChange(change, value)
    
    def setGeometry(self, rect):
        super(Node, self).setGeometry(rect)
        self.updateConnections()
        
    def updateConnections(self):
        [port.updateConnections() for port in self.ports]
        
    def boundingRect(self):
        """
        Overrides QGraphicsItem's boundingRect() virtual public function and 
        returns a valid bounding rect based on calculated width and height.
        """
        return QRectF(QPointF(0, 0), self.geometry().size())#.adjusted(
            #-self.shadowBlurRadius, -self.shadowBlurRadius, 
            # self.shadowBlurRadius,  self.shadowBlurRadius)

    def paint(self, painter, option, widget):
        """
        Overrides QGraphicsItem's paint() virtual public function.
        """
        # Draw base rectangle
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.drawRoundedRect(self.boundingRect(), 4, 4)

    def setSelected(self, selected):
        """
        Changes visual parameters on a selection or deselection event.
        """
        if selected:
            # Node selected
            #self.shadow.setColor(self.selectedShadowColor)
            self.pen.setColor(self.selectedBorderColor)
        else:
            # Node deselected
            #self.shadow.setColor(self.shadowColor)
            self.pen.setColor(self.normalBorderColor)
    
    def handleMousePressEvent(self, event):
        self.resizing = True
        self.resizeStart = event.scenePos()
        self.originalSize = self.size()

    def handleMouseMoveEvent(self, event):
        if self.resizing:
            r = event.scenePos() - self.resizeStart
            self.resize(self.originalSize + QSizeF(r.x(), r.y()))
        
    def handleMouseReleaseEvent(self, event):
        self.resizing = False
    
    @property
    def title(self):
        return self.title

    @title.setter
    def title(self, title):
        self.titleBar.title = title

    def addPort(self, port):
        """
        Adds a port.
        """
        self.ports.append(port)
        self.layout().insertItem(1, port)
        #port.setParentItem(self)
        
    def removePort(self, port):
        """
        Removes a port.
        """
        self.ports.remove(port)
        port.remove()
    
    @property
    def inputPorts(self):
        """
        Returns a list of descendant input ports.
        """
        return [port for port in self.ports if port.isInput()]
    
    @property
    def outputPorts(self):
        """
        Returns a list of descendant output ports.
        """
        return [port for port in self.ports if port.isOutput()]
        
    def getImmediateAncestors(self):
        """
        Returns a list of the node's immediate ancestors.
        
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
            # Check to make sure that the iterator is not referencing in a 
            # cyclic loop
            if ancestor not in ancestors and ancestor is not source:
                ancestors.append(ancestor)
                ancestors.extend(ancestor.getAllAncestors(source))
                
        return ancestors

class NodeTitleBar(QGraphicsWidget):
    def __init__(self):
        super(NodeTitleBar, self).__init__()

        # Colors
        self.textColor = QColor(30, 30, 30, 255)

        # Painter Definitions
        self.pen = QPen(self.textColor)
        self.font = QFont()
        self.pen.setWidth(1)
        self.font.setPointSize(10)

        # Settings
        self.title = ""

        self.setMinimumSize(QSizeF(-1, 30))
        self.setPreferredSize(QSizeF(-1, 30))
        
    def paint(self, painter, option, widget):
        """
        Overrides QGraphicsItem's paint() virtual public function.
        """
        # Draw title text
        painter.setPen(self.pen)
        painter.setFont(self.font)
        painter.drawText(10, 20, self.title)

    def boundingRect(self):
        return QRectF(QPointF(0, 0), self.geometry().size())

    def mousePressEvent(self, event):
        super(NodeTitleBar, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        super(NodeTitleBar, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        super(NodeTitleBar, self).mouseReleaseEvent(event)

class NodeHandleBar(QGraphicsWidget):
    def __init__(self):
        super(NodeHandleBar, self).__init__()

        # Colors
        self.textColor = QColor(30, 30, 30, 100)
        
        self.size = 20
        
        # Painter Definitions
        self.pen = QPen(self.textColor)
        self.pen.setWidth(1)
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setPreferredSize(QSizeF(-1, self.size))
        
    def paint(self, painter, option, widget):
        """
        Overrides QGraphicsItem's paint() virtual public function.
        """
        # PAint the handle
        painter.setPen(self.pen)
        
        rect       = self.boundingRect()
        topRight   = rect.topRight()   - QPointF(4, 0)
        bottomLeft = rect.bottomLeft() - QPointF(0, 4)
        painter.drawLine(topRight + QPointF(0, 4), bottomLeft + QPointF(4, 0))
        painter.drawLine(topRight + QPointF(0, 8), bottomLeft + QPointF(8, 0))
        painter.drawLine(topRight + QPointF(0, 12), bottomLeft + QPointF(12, 0))
        
    def boundingRect(self):
        rect = QRectF(0, 0, self.size, self.size)
        rect.moveLeft(self.geometry().right() - self.size)
        return rect

    def mousePressEvent(self, event):
        self.parentItem().handleMousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.parentItem().handleMouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.parentItem().handleMouseReleaseEvent(event)
        
class AnimationAdapter(QObject):
    """
    AnimationAdapter allows QPropertyAnimation to animate otherwise 
    unanimatable objects by emulating properties.
    """

    def __init__(self, obj):
        super(AnimationAdapter, self).__init__()
        self.obj = obj
        
    def __get_opacity(self):
        return self.obj.opacity()
    
    def __set_opacity(self, opacity):
        return self.obj.setOpacity(opacity)
    
    opacity = pyqtProperty(float, __get_opacity, __set_opacity)

class NodeConnection(QGraphicsPathItem):
    """
    NodeConnection
    """
    def __init__(self, sourcePort=None, destinationPort=None):
        super(NodeConnection, self).__init__()
        
        self.adapter      = AnimationAdapter(self)
        self.lastPort     = None
        self.points       = None
        self.valid        = False
        self.active       = False
        self.source       = sourcePort
        self.destination  = destinationPort
        self.pen          = QPen(QColor(30, 30, 30, 200), 2)
        self.pendingStart = None
        self.pendingEnd   = None

        self.setPen(self.pen)
        self.setZValue(-1)
        
        if sourcePort and destinationPort:
            self.connect(sourcePort, destinationPort)

        # Animations
        self.fadeInAnimation = QPropertyAnimation(self.adapter, "opacity")
        self.fadeInAnimation.setDuration(150)
        self.fadeInAnimation.setStartValue(0.5)
        self.fadeInAnimation.setEndValue(1.0)
        self.fadeInAnimation.setEasingCurve(QEasingCurve.InOutQuad)
        
        self.fadeOutAnimation = QPropertyAnimation(self.adapter, "opacity")
        self.fadeOutAnimation.setDuration(150)
        self.fadeOutAnimation.setStartValue(1.0)
        self.fadeOutAnimation.setEndValue(0.5)
        self.fadeOutAnimation.setEasingCurve(QEasingCurve.InOutQuad)
        
        self.updatePath()
        
        # Starting animation
        self.setOpacity(0.5)
        self.fadeIn()
    
    def fadeOut(self):
        self.fadeOutAnimation.start()

    def fadeIn(self):
        self.fadeInAnimation.start()

    def getPosition(self, obj):
        point = None

        if isinstance(obj, NodePort):
            # Object is a NodePort
            point = obj.getSocketPosition()
        elif isinstance(obj, QPointF):
            # Object is a QPointF
            point = obj
            
        return point

    def getPoints(self):
        points = []

        if self.active:
            # Established connection
            points = [self.getPosition(self.source), 
                self.getPosition(self.destination)]
        elif self.pendingStart and self.pendingEnd:
            # Pending connection
            if self.pendingStart.isOutput():
                points = [self.getPosition(self.pendingStart), 
                    self.getPosition(self.pendingEnd)]
            else:
                points = [self.getPosition(self.pendingEnd),
                    self.getPosition(self.pendingStart)]

        return points

    def updatePath(self):
        points = self.getPoints()
        if points:
            leftPoint, rightPoint = points
            path = QPainterPath()
            path.moveTo(leftPoint)
            
            e  = 0.5
            dx = rightPoint.x() - leftPoint.x()
            dy = rightPoint.y() - leftPoint.y()
            
            ctrl1 = QPointF( leftPoint.x() + abs(dx) * e, leftPoint.y())
            ctrl2 = QPointF(rightPoint.x() - abs(dx) * e, leftPoint.y() + dy)
            
            path.cubicTo(ctrl1, ctrl2, rightPoint)
            
            self.setPath(path)
    
    def setStartPoint(self, port):
        if port.isInput():
            self.destination = port
        else:
            self.source = port
        self.startPoint = port
    
    def anchorTo(self, obj):
        if isinstance(obj, NodePort):
            self.pendingStart = obj
            self.updatePath()

    def dragTo(self, obj):
        self.pendingEnd = obj
        self.updatePath()

    def canConnect(self, obj1, obj2):
        """
        Returns a true/false value indicating whether or not the connection can
        be properly made with the specified objects.
        """
        # The objects must exist.
        if not obj1 or not obj2:
            return False

        # The objects must be ports.
        if not isinstance(obj1, NodePort) or not isinstance(obj2, NodePort):
            return False

        # The ports cannot be the same.
        if obj1 is obj2:
            return False

        # The ports cannot have the same parent node.
        if obj1.parentItem() is obj2.parentItem():
            return False

        # The ports must have opposite directions.
        if obj1.direction is obj2.direction:
            return False

        # The connection cannot be a cyclic loop.
        if obj1.isInput():
            if obj1.parentItem() in obj2.parentItem().getAllAncestors():
                return False
        else:
            if obj2.parentItem() in obj1.parentItem().getAllAncestors():
                return False

        # A connection cannot be a duplicate of another.
        if obj1 in obj2.connectedPorts or obj2 in obj1.connectedPorts:
            return False

        return True

    def canConnectTo(self, obj):
        """
        Returns a true/false value indicating whether or not the connection can
        be properly made with the current pending ports.
        """
        return self.canConnect(self.pendingStart, obj)

    def connectPendingPorts(self):
        return self.connect(self.pendingStart, self.pendingEnd)

    def connect(self, obj1, obj2):
        """
        Connect the connection.

        If connection succeeds, the connection is set to active. If the 
        connection fails, the connection automatically deletes itself.
        """
        success = False

        if not self.active:
            # Attempt connection
            if self.canConnect(obj1, obj2):
                self.pendingStart = None
                self.pendingEnd   = None
                
                if obj1.isOutput():
                    self.source, self.destination = obj1, obj2
                else:
                    self.destination, self.source = obj1, obj2

                self.source.connectTo(self.destination, self)
                self.destination.removeConnections()
                self.destination.connectTo(self.source, self)

                self.active = True
                success = True
            else:
                success = False

        return success

    def disconnect(self):
        """
        Disconnect the connection.

        This often occurrs when the connection is being relocated for 
        permanent modification or deletion.
        """
        if self.active:
            self.source.removeConnection(self)
            self.destination.removeConnection(self)

            self.pendingStart = self.source
            self.pendingEnd   = self.destination

            self.source       = None
            self.destination  = None

            self.active = False
        
    def delete(self):
        #self.setParentItem(None)
        self.scene().removeItem(self)
    
class NodePort(QGraphicsWidget):
    
    INPUT  = "input"
    OUTPUT = "output"
    
    def __init__(self, direction=INPUT, label=None):
        super(NodePort, self).__init__()
        
        self.textColor = QColor(30, 30, 30)
        self.font = QFont()
        self.font.setPointSize(10)
        
        self.connections = {}
        self.pendingConnection = None
        self.direction = direction
        self.label = label or self.direction.capitalize()
        self.socket = NodePortSocket()
        self.socket.setParentItem(self)
        
        self.setColor("#eee")
        self.setMinimumSize(QSizeF(-1, 30))
        self.setPreferredSize(QSizeF(-1, 30))
        
    def boundingRect(self):
        return QRectF(QPointF(0, 0), self.geometry().size())
    
    def setGeometry(self, rect):
        super(NodePort, self).setGeometry(rect)
        if self.isInput():
            self.socket.setPos(0, 15)
        else:
            self.socket.setPos(self.size().width(), 15)
            
    def getSocketPosition(self):
        return self.socket.scenePos() + self.socket.boundingRect().center()

    def socketMousePressEvent(self, event):
        if self.isInput() and self.hasConnections():
            # An existing connection is being dragged. Since input ports must 
            # only have one connection, set this connection as the pending 
            # connection.
            self.pendingConnection = self.connections.keys()[0]
            self.pendingConnection.disconnect()
        else:
            # A new connection is being created
            self.pendingConnection = NodeConnection()
            self.scene().addItem(self.pendingConnection)
            self.pendingConnection.anchorTo(self)
    
    def socketMouseMoveEvent(self, event):
        if self.pendingConnection:
            position = event.scenePos()
            # The pending connection is being dragged.
            item = self.scene().itemAt(position)
            
            pendingEnd = self.pendingConnection.pendingEnd
            if isinstance(pendingEnd, NodePort):
                pendingEnd = pendingEnd.socket
                
            if pendingEnd is not item:
                # The pending connection is being dragged over a new object.
                
                # Unhighlight any previously pending port sockets.
                pendingEnd = self.pendingConnection.pendingEnd
                if isinstance(pendingEnd, NodePort):
                    pendingEnd.socket.highlight(False)
                    pendingEnd.fadeConnections(False)

                if isinstance(item, NodePortSocket) and self.pendingConnection.canConnectTo(item.parentItem()):
                    # The pending connection is being dragged over a valid port.
                    # Highlight the port.
                    item.highlight(True)
                    item.parentItem().fadeConnections(True)
                    self.pendingConnection.dragTo(item.parentItem())
                else:
                    # Drag the pending connection to the current mouse position.
                    self.pendingConnection.dragTo(position)

                # Recalculate and redraw the connection
                self.pendingConnection.updatePath()
        
    def socketMouseReleaseEvent(self, event):
        if self.pendingConnection:
            # Attempt to connect in whatever state the connection is in.
            if not self.pendingConnection.connectPendingPorts():
                # Automatically delete if the connection fails
                self.pendingConnection.delete()
            self.pendingConnection = None
    
    def highlight(self, value):
        self.highlighted = value
        self.update()
    
    def fadeConnections(self, value):
        if self.isInput():
            if value:
                [connection.fadeOut() for connection in self.connections.keys()]
            else:
                [ connection.fadeIn() for connection in self.connections.keys()]

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
            connection.updatePath()
    
    def setColor(self, color):
        self.socket.setColor(color)
        
    def paint(self, painter, option, widget):
        painter.setPen(self.textColor)
        textRect = self.boundingRect()
        n = 30
        textRect.setWidth(textRect.width() - n)
        textRect.moveLeft(n / 2.0)
        textRect.moveTop(6)
        
        alignment = Qt.AlignLeft
        if self.isOutput():
            alignment = Qt.AlignRight
            
        painter.drawText(textRect, alignment, self.label)
        
    def remove(self):
        pass

class NodePortSocket(QGraphicsItem):
    def __init__(self):
        super(NodePortSocket, self).__init__()
        
        self.setAcceptHoverEvents(True)
        self.radius = 6
        self.padding = 20
        self.pen = QPen(QColor(30, 30, 30, 255*.25))
        self.highlighted = False
        self.pen.setWidth(1)
        self.setColor("#eee")
        
        diameter = self.radius * 2
        self.rect = QRectF(-self.radius, -self.radius, diameter, diameter)
        
    def setColor(self, color):
        self.color  = QColor(color)
        darkerColor = self.color.darker(110)
        gradient = QRadialGradient(self.boundingRect().center(), 6)
        gradient.setColorAt(0, self.color)
        gradient.setColorAt(1, darkerColor)
        self.brush = QBrush(gradient)
        
        self.highlightBrush = QBrush(self.color.lighter(110))
        
    def boundingRect(self):        
        return QRectF(-15, -15, 30, 30)
    
    def paint(self, painter, option, widget):
        painter.setPen(self.pen)
        
        painter.setBrush(self.brush)
        if self.highlighted:
            painter.setBrush(self.highlightBrush)

        painter.drawEllipse(self.rect)
    
    def hoverEnterEvent(self, event):
        self.highlight(True)
        
    def hoverLeaveEvent(self, event):
        self.highlight(False)
        
    def highlight(self, value):
        self.highlighted = value
        self.update()
        
    def mousePressEvent(self, event):
        self.parentItem().socketMousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        self.parentItem().socketMouseMoveEvent(event)
        
    def mouseReleaseEvent(self, event):
        self.parentItem().socketMouseReleaseEvent(event)
        
class ColorNodePort(NodePort):
    def __init__(self, *args, **kwargs):
        super(ColorNodePort, self).__init__(*args, **kwargs)
        self.label = self.label or "Color"
        self.setColor("#ccc")

class ValueNodePort(NodePort):
    def __init__(self, *args, **kwargs):
        super(ValueNodePort, self).__init__(*args, **kwargs)
        self.label = self.label or "Value"
        self.setColor("#356")

class PixmapNodePort(NodePort):
    def __init__(self, *args, **kwargs):
        super(PixmapNodePort, self).__init__(*args, **kwargs)
        self.label = self.label or "Image"
        self.setColor("#ff4")
