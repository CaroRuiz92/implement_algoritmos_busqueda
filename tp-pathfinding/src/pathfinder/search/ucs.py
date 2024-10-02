from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier, StackFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class UniformCostSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        # Initialize a node with the initial position
        node = Node("", state=grid.start, cost=0, parent=None, action=None)

        # Initialize the reached dictionary with the initial state
        reached = {} #diccionario de estados
        reached[node.state] = True

        # Return if the node contains a goal state


        # Initialize the frontier with the initial node
        # In this example, the frontier is a queue
        frontier = PriorityQueueFrontier()
        frontier.add(node)
        alcanzados = {}

        while True:

            #  Fail if the frontier is empty
            if frontier.is_empty():
                return NoSolution(reached)

            # Remove a node from the frontier
            node = frontier.pop()
           
            if node.state == grid.end: #Chequeo test-objetivo
                return Solution(node, reached)

            successors = grid.get_neighbours(node.state) #posibles casos (evita los muros)

            for accion in successors: #recorro los posibles casos
                new_state = successors[accion]
                if new_state not in reached: #me fijo que no este en los visitados
                    new_node = Node("", new_state,
                                    node.cost + grid.get_cost(new_state),
                                    parent=node, action=accion)

               
                if s not in alcanzados or new_node < alcanzados[s]: