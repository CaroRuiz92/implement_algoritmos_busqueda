from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


def h_func(node):
    # se debe devolver un numero
    pass

class GreedyBestFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Greedy Best First Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)

        frontier = PriorityQueueFrontier()
        frontier.add(node, h_func(node))

        # Initialize the explored dictionary
        explored = {} 
        explored[node.state] = node.cost
        
        # Parte principal GBFS
        while True:
            if frontier.is_empty():  # Si la frontera esta vacia, no hay solucion
                return NoSolution(explored)
            
            n = frontier.pop()

            if n.state == grid.end:
                return Solution(n, explored)
            
            successors = grid.get_neighbours(n.state)

            for dato in successors.values():
                s_prima = dato
                c_prima = n.cost + grid.get_cost(s_prima) # VER
            
                if s_prima not in explored or c_prima < explored[s_prima]:
                    n_prima = Node("", s_prima, n.cost + grid.get_cost(s_prima), parent=n, action=None)
                    explored[s_prima] = c_prima
                    frontier.add(n_prima, h_func(n_prima))
