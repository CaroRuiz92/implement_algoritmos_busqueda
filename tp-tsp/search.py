"""Este modulo define la clase LocalSearch.

LocalSearch representa un algoritmo de busqueda local general.

Las subclases que se encuentran en este modulo son:

* HillClimbing: algoritmo de ascension de colinas. Se mueve al sucesor con
mejor valor objetivo. Ya viene implementado.

* HillClimbingReset: algoritmo de ascension de colinas de reinicio aleatorio.
No viene implementado, se debe completar.

* Tabu: algoritmo de busqueda tabu.
No viene implementado, se debe completar.
"""


from __future__ import annotations
from time import time
from problem import OptProblem


class LocalSearch:
    """Clase que representa un algoritmo de busqueda local general."""

    def __init__(self) -> None:
        """Construye una instancia de la clase."""
        self.niters = 0  # Numero de iteraciones totales
        self.time = 0  # Tiempo de ejecucion
        self.tour = []  # Solucion, inicialmente vacia
        self.value = None  # Valor objetivo de la solucion

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion."""
        self.tour = problem.init
        self.value = problem.obj_val(problem.init)


class HillClimbing(LocalSearch):
    """Clase que representa un algoritmo de ascension de colinas.

    En cada iteracion se mueve al estado sucesor con mejor valor objetivo.
    El criterio de parada es alcanzar un optimo local.
    """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Arrancamos del estado inicial
        actual = problem.init
        value = problem.obj_val(problem.init)

        while True:

            # Buscamos la acción que genera el sucesor con mayor valor objetivo
            act, succ_val = problem.max_action(actual)

            # Retornar si estamos en un maximo local:
            # el valor objetivo del sucesor es menor o igual al del estado actual
            if succ_val <= value:

                self.tour = actual
                self.value = value
                end = time()
                self.time = end-start
                return

            # Sino, nos movemos al sucesor
            actual = problem.result(actual, act)
            value = succ_val
            self.niters += 1


class HillClimbingReset(LocalSearch):
    """Algoritmo de ascension de colinas con reinicio aleatorio."""
    def __init__(self, max_reinicios: int = 10) -> None:
        super().__init__()
        self.max_reinicios = max_reinicios
        
    def solve(self, problema: OptProblem):
        inicio = time()
        
        total_reinicios = 0
        
        while total_reinicios < self.max_reinicios:
            estado_actual = problema.random_reset()
            valor_actual = problema.obj_val(estado_actual)
            
            while True:
                accion, valor_sucesor = problema.max_action(estado_actual) # busca la accion que genera el sucesor con mayor valor objetivo
                # si estamos en un maximo local, salir 
                if valor_sucesor <= valor_actual:
                    break
                
                # nos movemos al sucesor
                estado_actual = problema.result(estado_actual, accion)
                valor_actual = valor_sucesor
                self.niters += 1

            # actualizamos mejor solucion
            if self.value is None or valor_actual > self.value:
                self.tour = estado_actual
                self.value = valor_actual
            
            total_reinicios += 1
        
        fin = time()
        self.time = fin-inicio
        
###########################

def max_action_tabu(problem: OptProblem, state: list[int], tabu: list[tuple[int, int]] = []) -> tuple[tuple[int, int], float]:
    """ Adaptación de funcion max_action original """
    value = problem.obj_val(state)
    max_act = None
    max_val = float("-inf")
    
    for a in problem.actions(state):
        if a in tabu:
            continue
        i, j = a
        v1 = state[i] + 1  # origen de i
        v2 = state[i + 1] + 1  # destino de i
        v3 = state[j] + 1  # origen de j
        v4 = state[j + 1] + 1  # destino de j
        distl1l2 = problem.G.get_edge_data(v1, v2)['weight']
        distl3l4 = problem.G.get_edge_data(v3, v4)['weight']
        distl1l3 = problem.G.get_edge_data(v1, v3)['weight']
        distl2l4 = problem.G.get_edge_data(v2, v4)['weight']
        
        succ_value = value + distl1l2 + distl3l4 - distl1l3 - distl2l4
        
        if succ_value > max_val:
            max_act = a
            max_val = succ_value

    return max_act, max_val

###########################

class Tabu(LocalSearch):
    def __init__(self, max_iter: int = 15, tabu_size: int = 15) -> None:
        super().__init__()
        self.max_iter = max_iter
        self.tabu_size = tabu_size

    def solve(self, problem: OptProblem):
        
        start = time()

        # Inicializar estado_actual antes de usarlo
        estado_actual = problem.init
        mejor = estado_actual
        tabu = []
        iterac = 0

        # se actúa teniendo en cuenta la cantidad de iteraciones
        while iterac < self.max_iter:
            acc, val_acc = max_action_tabu(problem, estado_actual, tabu)
            
            if acc is None:
                break

            sucesor = problem.result(estado_actual, acc)

            if problem.obj_val(mejor) < problem.obj_val(sucesor):
                mejor = sucesor

            # se tiene en cuenta tabu para su comparativa dentro de max_action_tabu
            tabu.append(acc)
            if len(tabu) > self.tabu_size:
                tabu.pop(0)
            estado_actual = sucesor
            iterac += 1

            self.tour = mejor
            self.value = problem.obj_val(mejor)
            self.niters = iterac
            

        end = time()
        self.time = end-start
