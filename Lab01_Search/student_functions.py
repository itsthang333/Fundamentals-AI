import numpy as np
import queue

def BFS(matrix, start, end):
    """
    BFS algorithm:
    Parameters:
    ---------------------------
    matrix: np array 
        The graph's adjacency matrix
    start: integer
        starting node
    end: integer
        ending node
    
    Returns
    ---------------------
    visited
        The dictionary contains visited nodes, each key is a visited node,
        each value is the adjacent node visited before it.
    path: list
        Founded path
    """
    # TODO: 
    path=[]
    frontier = queue.Queue()
    visited ={}

    frontier.put(start)
    visited[start] = None

    while not frontier.empty():
        current = frontier.get()
        if current == end:
            break

        for child in range(len(matrix)):
            if matrix[current][child] and child not in visited:
                frontier.put(child)
                visited[child] = current

    while end is not None:
        path.insert(0,end)
        end = visited.get(end)
   
    return visited, path

def DFS(matrix, start, end):
    """
    DFS algorithm
     Parameters:
    ---------------------------
    matrix: np array 
        The graph's adjacency matrix
    start: integer 
        starting node
    end: integer
        ending node
    
    Returns
    ---------------------
    visited 
        The dictionary contains visited nodes: each key is a visited node, 
        each value is the key's adjacent node which is visited before key.
    path: list
        Founded path
    """

    # TODO:     
    path=[]
    visited ={}

    visited[start] = None
    frontier =[start] # as a stack

    while frontier:
        current_node = frontier.pop()

        if current_node == end:
            break

        for child in range(len(matrix[current_node])):
            if matrix[current_node][child] and child not in visited:
                frontier.append(child)
                visited[child] = current_node

    while end is not None:
        path.insert(0,end)
        end = visited.get(end)

    return visited, path


def UCS(matrix, start, end):
    """
    Uniform Cost Search algorithm
     Parameters:visited
    ---------------------------
    matrix: np array
        The graph's adjacency matrix
    start: integer
        starting node
    end: integer
        ending node
    
    Returns
    ---------------------
    visited
        The dictionary contains visited nodes: each key is a visited node, 
        each value is the key's adjacent node which is visited before key.
    path: list
        Founded path
    """
    # TODO:  
    path = []
    visited = {}
    frontier = queue.PriorityQueue()

    frontier.put((0, start))
    costs = {start: 0}

    while not frontier.empty():
        current_cost, current_node = frontier.get()

        if current_node == end:
            break

        if current_node not in visited:
            visited[current_node] = None

            for child in range(len(matrix[current_node])):
                if matrix[current_node][child]:
                    new_cost = current_cost + matrix[current_node][child]
                    if child not in costs or new_cost < costs[child]:
                        costs[child] = new_cost
                        frontier.put((new_cost, child))
                        visited[child] = current_node

    while end is not None:
        path.insert(0, end)
        end = visited.get(end)

    return visited, path

def GBFS(matrix, start, end):
    """
    Greedy Best First Search algorithm 
    heuristic : edge weights
     Parameters:
    ---------------------------
    matrix: np array 
        The graph's adjacency matrix
    start: integer 
        starting node
    end: integer
        ending node
   
    Returns
    ---------------------
    visited
        The dictionary contains visited nodes: each key is a visited node, 
        each value is the key's adjacent node which is visited before key.
    path: list
        Founded path
    """
    # TODO: 
    path = []
    visited = {}
    frontier = queue.PriorityQueue()

    frontier.put((0, start))

    while not frontier.empty():
        _, current_node = frontier.get()

        if current_node == end:
            break

        if current_node not in visited:
            visited[current_node] = None

            for child in range(len(matrix[current_node])):
                if matrix[current_node][child] and child not in visited:
                    heuristic_value = matrix[child][end]
                    frontier.put((heuristic_value, child))
                    visited[child] = current_node

    while end is not None:
        path.insert(0, end)
        end = visited.get(end)

    return visited, path


def Astar(matrix, start, end, pos):
    """
    A* Search algorithm
    heuristic: eclid distance based positions parameter
     Parameters:
    ---------------------------
    matrix: np array UCS
        The graph's adjacency matrix
    start: integer 
        starting node
    end: integer
        ending node
    pos: dictionary. keys are nodes, values are positions
        positions of graph nodes
    Returns
    ---------------------
    visited
        The dictionary contains visited nodes: each key is a visited node, 
        each value is the key's adjacent node which is visited before key.
    path: list
        Founded path
    """
    # TODO: 
    def euclid_distance(pos1, pos2):
        return np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
    
    open_list = queue.PriorityQueue()
    closed_list = set()
    open_list.put((0, start))
    costs = {start: 0}
    parents = {start: None}
    
    while not open_list.empty():
        _, current_node = open_list.get()
        
        if current_node == end:
            break
        
        if current_node in closed_list:
            continue
        
        closed_list.add(current_node)
        
        for child in range(len(matrix[current_node])):
            if matrix[current_node][child]:
                new_cost = costs[current_node] + matrix[current_node][child]
                heuristic_value = euclid_distance(pos[child], pos[end])
                f_value = new_cost + heuristic_value
                
                if child not in costs or new_cost < costs[child]:
                    costs[child] = new_cost
                    open_list.put((f_value, child))
                    parents[child] = current_node
    
    path = []
    node = end
    while node is not None:
        path.insert(0, node)
        node = parents.get(node)
    
    return parents, path
