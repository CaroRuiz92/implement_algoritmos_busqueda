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
        reached[node.state] = node.cost

        # Return if the node contains a goal state


        # Initialize the frontier with the initial node
        # In this example, the frontier is a queue
        frontier = PriorityQueueFrontier()
        frontier.add(node,node.cost) # el nodo inicial con costo 0
        alcanzados = {} # almacena los estados alcanzados con su costo

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
                new_cost = node.cost + grid.get_cost(new_state) # costo acumulado
               
               # si no alcanzamos este estado antes, o si el nuevo costo es menor
                if new_state not in alcanzados or new_cost < alcanzados[new_state]:
                    new_node = Node("",new_state,new_cost,parent=node,action=accion)
                    alcanzados[new_state]= new_cost # actualizamos el costo minimo 
                    frontier.add(new_node,new_cost) # encolamos el nuevo nodo con su costo