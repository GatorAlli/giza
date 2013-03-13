from giza.widgets import (Node, NodePort, ColorNodePort, 
                         ValueNodePort)

moduleData = {
    "name"       : "Input",
    "description": "Input elements for the Node classes.",
}


class ColorInputNode(Node):
    
    name = "Color"
    description = "Lol this is awesome!"
    
    def __init__(self):
        super(ColorInputNode, self).__init__()
        
        self.title = "Color"
        self.addPort(ColorNodePort(NodePort.OUTPUT, "Color"))
        

class ValueInputNode(Node):
    
    name = "Value"
    description = "A floating point number"
    
    def __init__(self):
        super(ValueInputNode, self).__init__()
        
        self.title = "Value"
        self.width = 200
        self.addPort(ValueNodePort(NodePort.OUTPUT, "Value"))