from PyQt4.QtGui import (QGraphicsItem, QGraphicsEllipseItem, QColor, QPen, QBrush, 
                         QGraphicsDropShadowEffect, QFont, QRadialGradient,
                         QPainterPath)
from PyQt4.QtCore import (QRectF, Qt, QPointF, QPropertyAnimation, QEasingCurve,
                          QObject, pyqtProperty)
import math

class Dial(QGraphicsItem):
    """
    Dial
    """
    
    def __init__(self):
        super(Dial, self).__init__()
        
        self.angle = 0

        # Colors
        self.color               = QColor(120, 120, 120, 255)
        self.notchColor          = QColor(115, 115, 115, 255)
        self.normalBorderColor   = QColor(  255,  255,  255, 30  )
        self.selectedBorderColor = QColor( 255, 191,   0, 102 )
        self.textColor           = QColor(  30,  30,  30, 255 )
        self.shadowColor         = QColor(0, 0, 0, 75)
        self.selectedShadowColor = QColor( 100, 100, 100, 255 )

        # Settings
        self.width, self.height = 75, 75
        
        # Drop Shadow
        self.shadowBlurRadius = 8
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(self.shadowBlurRadius)
        self.shadow.setOffset(0, 0.5)
        self.shadow.setColor(self.shadowColor)
        self.setGraphicsEffect(self.shadow)
        
        # Painter Definitions
        self.pen = QPen()
        gradient = QRadialGradient(self.boundingRect().center() + QPointF(0, -20), 80)
        gradient.setColorAt(0, self.color.lighter(117))
        gradient.setColorAt(1, self.color)
        self.brush = QBrush(gradient)
        self.font  = QFont()
        self.pen.setWidth(1)
        self.pen.setColor(self.normalBorderColor)
        self.brush.setColor(self.color)
        self.font.setPointSize(10)
        
        # Nodegraph Definitions
        self.dragPoint  = None
        self.dragAngle  = 0
        self.dragFactor = 0

        # Notch Specifications
        self.notch = DialNotch()
        self.notch.setParentItem(self)
        self.updateNotch()

    def boundingRect(self):
        """
        Overrides QGraphicsItem's boundingRect() virtual public function and 
        returns a valid bounding rect based on calculated width and height.
        """
        return QRectF(0, 0, self.width, self.height).adjusted(
            -self.shadowBlurRadius, -self.shadowBlurRadius, 
             self.shadowBlurRadius,  self.shadowBlurRadius)

    def paint(self, painter, option, widget):
        """
        Overrides QGraphicsItem's paint() virtual public function.
        """
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.drawEllipse(self.boundingRect())

    def mousePressEvent(self, event):
        self.dragPoint  = event.scenePos()
        self.dragAngle  = self.angle
        part     = self.height / 2
        distance = event.pos().y() - part
        if distance == 0:
            self.dragFactor = 0
        else:
            self.dragFactor = part / distance

    def mouseMoveEvent(self, event):
        scenePos = event.scenePos()
        d = scenePos - self.dragPoint
        self.angle = self.dragAngle + d.x() * self.dragFactor
        self.updateNotch()

    def mouseReleaseEvent(self, event):
        self.dragPoint = None
        self.dragAngle = 0

    def updateNotch(self):
        f  = 0.02
        dx = (self.width  - self.notch.width)  / 2
        dy = (self.height - self.notch.height) / 2
        x  = math.sin(math.radians(self.angle)) * dx + dx
        y  = math.cos(math.radians(self.angle)) * dy + dy
        self.notch.setPos(x, y)

class DialNotch(QGraphicsItem):
    """
    DialNotch
    """
    
    def __init__(self):
        super(DialNotch, self).__init__()
        self.setAcceptHoverEvents(True)
        # Colors
        self.color      = QColor(125, 125, 125, 255)
        self.normalBorderColor   = QColor(  255,  255,  255, 30  )
        self.selectedBorderColor = QColor( 255, 191,   0, 102 )
        self.textColor           = QColor(  30,  30,  30, 255 )
        self.shadowColor         = QColor(0, 0, 0, 75)
        self.selectedShadowColor = QColor( 100, 100, 100, 255 )

        # Settings
        self.width, self.height = 12, 12
        self.highlighted = False

        # Painter Definitions
        self.pen = QPen()
        self.pen.setWidth(1)
        self.pen.setColor(self.normalBorderColor)

        gradient = QRadialGradient(self.boundingRect().center() + QPointF(0, 1), self.width / 2.0)
        gradient.setColorAt(0,   self.color)
        gradient.setColorAt(0.5, self.color)
        gradient.setColorAt(1,   self.color.darker(120))
        self.brush = QBrush(gradient)

        gradient = QRadialGradient(self.boundingRect().center() + QPointF(0, 1), self.width / 2.0)
        gradient.setColorAt(0,   self.color.lighter(110))
        gradient.setColorAt(0.5, self.color.lighter(110))
        gradient.setColorAt(1,   self.color.darker(120).lighter(110))
        self.highlightBrush = QBrush(gradient)

        # Other
        self.tracking = False
        self.angle = None

    def boundingRect(self):
        """
        Overrides QGraphicsItem's boundingRect() virtual public function and 
        returns a valid bounding rect based on calculated width and height.
        """
        return QRectF(0, 0, self.width, self.height)

    def paint(self, painter, option, widget):
        """
        Overrides QGraphicsItem's paint() virtual public function.
        """
        painter.setPen(self.pen)

        painter.setBrush(self.brush)
        if self.highlighted:
            painter.setBrush(self.highlightBrush)

        painter.drawEllipse(self.boundingRect())

    def highlight(self, value):
        self.highlighted = value
        self.update()

    def hoverEnterEvent(self, event):
        self.highlight(True)
        
    def hoverLeaveEvent(self, event):
        self.highlight(False)

    def mousePressEvent(self, event):
        self.tracking = True
        parent = self.parentItem()
        parent.dragPoint  = event.pos()
        parent.dragAngle  = parent.angle

    def mouseMoveEvent(self, event):
        if self.tracking:
            parent = self.parentItem()
            d = event.scenePos() - parent.boundingRect().center()
            if self.angle:
                a = self.angle - math.degrees(math.atan2(-d.y(),d.x()))
            else:
                a = math.degrees(math.atan2(-d.y(),d.x()))
                self.angle = a
            parent.angle = parent.dragAngle - a
            parent.updateNotch()

    def mouseReleaseEvent(self, event):
        self.tracking = False
        parent = self.parentItem()
        parent.dragPoint = None
        parent.dragAngle = 0
        self.angle = None
