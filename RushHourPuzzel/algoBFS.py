from collections import deque
from Node import Node
from game import RushHourPuzzle
def BFS(s, successorsFn, isGoal):
    Open = deque()  # FIFO queue
    Closed = []     # list

    init_node = Node(s, None, None)  # Node(state, parentNode, action)
    if isGoal(init_node.state):
        return init_node

    Open.append(init_node)
    Closed = []

    while Open:
        current = Open.popleft()  # Choose the shallowest node in Open
        
        Closed.append(current)

        for action, successor in successorsFn(current.state):
            child = Node(successor, current, action)  # Create a new node and link to its parent

            # Check if child.state not in Closed and not in Open
            in_closed = any(child.state.equals(node.state) for node in Closed)
            in_open = any(child.state.equals(node.state) for node in Open)
            if not in_closed and not in_open:
                if isGoal(child.state):
                    return child
                Open.append(child)
    return None
