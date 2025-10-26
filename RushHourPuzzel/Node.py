class Node:
    def __init__(self, state, parent=None, action=None, g=0, f=0):
        self.state = state      
        self.parent = parent    
        self.action = action    
        self.g = g              
        self.f = f             

    def getPath(self):
        path = []
        node = self
        while node is not None:
            path.append(node.state)
            node = node.parent
        path.reverse()  
        return path   

    def getSolution(self):
        solution = []
        node = self
        while node is not None:
            if node.action is not None:
                solution.append(node.action)
            node = node.parent
        solution.reverse()
        return solution

    def setF(self, h):
       
        # Si h est une fonction, appelle-la
        if callable(h):
            h_val = h(self.state)
        else:
            h_val = h
        self.f = self.g + h_val
        return self.f