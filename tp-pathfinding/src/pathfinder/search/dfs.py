from ..models.grid import Grid
from ..models.frontier import StackFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class DepthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Depth First Search
        Args:
            grid (Grid): Grid of points
            
        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)

         # Initialize the explored dictionary to be empty
        explored = {} 

        # Return if the node contains a goal state
        if node.state == grid.end:
            return Solution(node, explored)
        
        # Initialize the frontier with the initial node
        # In this example, the frontier is a queue
        frontier = StackFrontier()
        frontier.add(node)

    # Bucle principal de DFS
        while True:
            if frontier.is_empty():  # Si la frontera esta vacia, no hay solucion
                return NoSolution(explored)
        
            n = frontier.remove()  # Desapilar el nodo de la frontera
        
            if n.state in explored:  # Si ya ha sido expandido, saltar
                continue
        
            # Add the node to the explored dictionary
            explored[n.state] = True  # Marcar como expandido (STATE: UBICACION)
        
        # Expandir todos los sucesores del nodo
            successors = grid.get_neighbours(n.state)
            for dato in successors.values():
                s_prima = dato
            
                if s_prima not in explored:  # Control para evitar expandir el estado ya expandido
                    n_prima = Node("", s_prima, n.cost + grid.get_cost(s_prima), parent=n, action=None)

                
                    if n_prima.state == grid.end:  # Si el estado es objetivo, retornar la solucion
                        return Solution(n_prima, explored)
                
                    frontier.add(n_prima)  # Agregar el nuevo nodo a la frontera










        
        
        
