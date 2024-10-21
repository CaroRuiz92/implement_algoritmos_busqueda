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
        self.time = inicio-fin
        



def max_action(problem: OptProblem, state, tabu) -> tuple[list, float]:
        dic = {}
        

class Tabu(LocalSearch):

    """Algoritmo de busqueda tabu."""
    def solve(self, problem: OptProblem):
        actual = problem.init
        mejor = actual
        tabu = []
        problem.niters = 0

        max_iter = 15
        tabu_size = 10

        while problem.niters < max_iter:
            accion = max_action(problem, actual, tabu)
            sucesor = problem.result(actual, accion)
            if problem.obj_val(mejor) < problem.obj_val(sucesor):
                mejor = sucesor
                tabu.append(sucesor)
            if len(tabu) > tabu_size:
                tabu.pop(0)

            actual = sucesor
            problem.niters += 1
        return mejor