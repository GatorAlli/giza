from giza.widgets import (Node, NodePort, ColorNodePort, ValueNodePort, 
                         PixmapNodePort)

moduleData = {
    "name"       : "Convert",
    "description": "Convert elements for the Node classes.",
}


class MixNode(Node):
    
    name = "Mix"
    description = ":D"
    
    def __init__(self):
        super(MixNode, self).__init__()
        
        self.title = "Mix"
        # self.width = 400
        # self.addPort(NodePort(NodePort.OUTPUT, "lol"))
        # self.addPort(ColorNodePort(NodePort.OUTPUT))
        # self.addPort(ColorNodePort(NodePort.OUTPUT, "Vec4f"))
        # self.addPort(ValueNodePort(NodePort.OUTPUT, "Normal"))
        # self.addPort(PixmapNodePort(NodePort.INPUT, "Vec"))
        # self.addPort(PixmapNodePort(NodePort.INPUT, "Vec4f"))
        # self.addPort(ValueNodePort(NodePort.INPUT, "Normal"))
