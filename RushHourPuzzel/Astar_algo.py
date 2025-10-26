from collections import deque
from Node import Node
from game import RushHourPuzzle


#il calcule combien de voiture est entre la voiture X et la distance X et la sortie 
def h(s):
    x = s.vagent["x"]#0
    y = s.vagent["y"]#2
    length = s.vagent["length"]#2
    voiture_x = x + length -1 #0+2-1=1 

    heuristic = s.board_width-voiture_x -1#6-1-1=4
    
    for j in range(voiture_x+1, s.board_width-1):
        if s.board[y][j] != "." and s.board[y][j-1]!=s.board[y][j]:
            heuristic += 1


    return heuristic

def min_list(Open):
   
    min_f = Open[0].f
    pos_min = 0

    for i in range(1, len(Open)):
        if Open[i].f < min_f:
            min_f = Open[i].f
            pos_min = i

    return pos_min


def A(s, successorsFn, isGoal):
    
    Open =[] # on va utiliser une liste pour acceder a l'element avec le min f
    Closed = []     # list

    init_node = Node(s, None, None)  # Node(state, parentNode, action ,g,f)
    init_node.setF(h)
    
    if isGoal(init_node.state):
        return init_node
    
    Open.append(init_node) #on ajoute the first node
    
    while Open:
        # Choose the lowest f in the nodes in Open
        pos=min_list(Open)
        current=Open.pop(pos)

        if isGoal(current.state):
            return current
        
        Closed.append(current)

        for action, successor in successorsFn(current.state):
            g=current.g+1
            child = Node(successor, current, action,g)  # Create a new node and link to its parent
            child.setF(h)
            

            in_closed = any(child.state.equals(node.state) for node in Closed)
            in_open = any(child.state.equals(node.state) for node in Open)

            if not in_closed and not in_open:
                Open.append(child)
            elif(in_open):
                for i , node in enumerate(Open):
                    if(child.state.equals(node.state)):
                        if (child.f<(node.f)):
                            Open[i]=child
                        
            elif(in_closed):
                for i , node in enumerate(Closed):
                    if(child.state.equals(node.state)):
                        if (child.f<(node.f)):
                            Closed.pop(i)
                            Open.append(child) 
                        


    return None