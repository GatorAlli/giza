from giza.widgets import Node, NodePort

moduleData = {
    "name"       : "Input",
    "description": "Input elements for the Node classes.",
}


class ColorInputNode(Node):
    
    name = "Color"
    description = "Lol this is awesome!"
    
    def __init__(self):
        super(ColorInputNode, self).__init__()
        
        self.setTitle("Color")
        self.addPort(NodePort(NodePort.COLOR, NodePort.OUTPUT, "ColorOut"))
        

class NumberInputNode(Node):
    
    name = "Number"
    description = "Lol this is a number!"
    
    def __init__(self):
        super(NumberInputNode, self).__init__()
        print "XD"