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
        

class NumberInputNode(Node):
    
    name = "Number"
    description = "Lol this is a number!"
    
    def __init__(self):
        super(NumberInputNode, self).__init__()
        
        self.title = "Input Value"
        self.width = 200
        self.addPort(ValueNodePort(NodePort.OUTPUT, "Value"))