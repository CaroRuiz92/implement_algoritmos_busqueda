from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class BreadthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Go Right

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", state=grid.start, cost=0, parent=None, action=None) #Nodo inicial


        # Initialize the reached dictionary with the initial state
        reached = {} #diccionario de estados
        reached[node.state] = True

        # Return if the node contains a goal state
        if node.state == grid.end: #Chequeo test-objetivo
            return Solution(node, reached)

        # Initialize the frontier with the initial node
        # In this example, the frontier is a queue
        frontier = QueueFrontier()
        frontier.add(node)


        while True:

            #  Fail if the frontier is empty
            if frontier.is_empty(): 
                return NoSolution(reached) #si la frontera esta vacia, no quedan nodos por ver, por ende no hay solucion

            # Remove a node from the frontier
            node = frontier.remove() #saco el nodo de la frontera

            # Go 
            successors = grid.get_neighbours(node.state) #posibles casos (evita los muros)
            
            for accion in successors: #recorro los posibles casos
                new_state = successors[accion] 
                if new_state not in reached: #me fijo que no este en los visitados
                    new_node = Node("", new_state,
                                    node.cost + grid.get_cost(new_state),
                                    parent=node, action=accion)

                    if new_state == grid.end: #Con esto creo que agrego el nuevo nodo a la solucion
                        return Solution(new_node, reached)
                    
                    reached[new_state] = True #marco el estado que alcance
                    frontier.add(new_node) 