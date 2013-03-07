from giza import nodes

for module, nodeTypes in nodes.getNodeTypes().iteritems():
    print ""
    print "%s (%s)" % (module.moduleData["name"], 
                       module.moduleData["description"])
    
    for nodeType in nodeTypes:
        print "|-- %s (%s)" % (nodeType.name, nodeType.description)
    