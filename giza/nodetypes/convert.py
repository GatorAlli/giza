from giza.widgets import Node, NodePort

moduleData = {
    "name"       : "Convert",
    "description": "Convert elements for the Node classes.",
}


class MixNode(Node):
    
    name = "Mix"
    description = ":D"
    
    def __init__(self):
        super(MixNode, self).__init__()
        
        self.setTitle("Mix")
        self.addPort(NodePort(NodePort.COLOR,  NodePort.OUTPUT,  "In"))
        self.addPort(NodePort(NodePort.COLOR,  NodePort.OUTPUT,  "In"))
        self.addPort(NodePort(NodePort.COLOR,  NodePort.INPUT,  "In"))
        self.addPort(NodePort(NodePort.VALUE,  NodePort.OUTPUT, "Out"))
        self.addPort(NodePort(NodePort.PIXMAP, NodePort.INPUT,  "In"))
        self.addPort(NodePort(NodePort.COLOR,  NodePort.OUTPUT, "Out"))