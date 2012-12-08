import os
from giza.widgets import Node

def getNodeTypes():
    categories = {}
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nodetypes")
    
    for fileName in os.listdir(path):
        if fileName.endswith('.py') and fileName != '__init__.py':
            fileName = fileName[:-3]
            module = __import__(".".join(["nodetypes", fileName]), 
                                fromlist=[fileName])
            category = categories[module] = []
            
            for nodeClass in dir(module):
                nodeClass = getattr(module, nodeClass)
                if isinstance(nodeClass, type) and nodeClass != Node:
                    category.append(nodeClass)

    return categories