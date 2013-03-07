import os
import inspect
from giza.widgets import Node

def getNodeTypes():
    categories = {}
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nodetypes")
    
    for fileName in os.listdir(path):
        if fileName.endswith(".py") and fileName != "__init__.py":
            fileName = fileName[:-3]
            module = __import__(".".join(["nodetypes", fileName]), 
                                fromlist=[fileName])
            category = categories[module] = []
            
            for member in inspect.getmembers(module, inspect.isclass):
                nodeClass = member[1]
                if inspect.isclass(nodeClass) and (nodeClass.__module__ is module.__name__):
                    category.append(nodeClass)

    return categories
