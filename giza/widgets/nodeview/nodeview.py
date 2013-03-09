import sys
from PyQt4.QtGui import QGraphicsView, QApplication, QPainter

from nodeviewscene import NodeViewScene

class NodeView(QGraphicsView):
    """Pidfile
    
    This is the type returned by :func:`create_pidlock`.
    
    TIP: Use the :func:`create_pidlock` function instead,
    which is more convenient and also removes stale pidfiles (when
    the process holding the lock is no longer running).
    
    """
    
    def __init__(self):
        """This function does something.
        
        Args:
           name (str):  The name to use.
        
        Kwargs:
           state (bool): Current state to be in.
        
        Returns:
           int.  The return code::
        
              0 -- Success!
              1 -- No good.
              2 -- Try again.
        
        Raises:
           AttributeError, KeyError
        
        A really great idea.  A way you might use me is
        
        >>> print public_fn_with_googley_docstring(name='foo', state=None)
        0
        
        BTW, this always returns 0.  **NEVER** use with :class:`MyPublicClass`.
        
        """
        super(NodeView, self).__init__()
        
        # self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setRenderHint(QPainter.Antialiasing)
        self.setScene(NodeViewScene())