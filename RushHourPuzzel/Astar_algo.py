from collections import deque
from Node import Node
from game import RushHourPuzzle


#il calcule le nombre de voiture qui sont entre la voiture X et la sortie,et la distance X et la sortie 
def h(s,parent_state=None):
    x = s.vagent["x"]
    y = s.vagent["y"]
    length = s.vagent["length"]
    voiture_x = x + length - 1

    # H1
    distance_sortie = s.board_width - voiture_x - 1

    # H2
    voitures_blk = 0
    for j in range(voiture_x + 1, s.board_width):
        if s.board[y][j] != ".":
            voitures_blk += 1

    # H3:si la voiture X revient en arriere on ajoute un panlite
    H3 = 0
    if parent_state is not None:
        x_parent = parent_state.vagent["x"]
        if x < x_parent:  # X recule (se déplace vers la gauche)
            H3 = x_parent - x # Pénalité proportionnelle à la distance reculée

    # Heuristique : distance + voitures bloquantes + pénalité
    heuristic = distance_sortie+voitures_blk + H3

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
    init_node.setF(lambda state: h(state))
    
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
            child.setF(lambda state: h(state, current.state))
            

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