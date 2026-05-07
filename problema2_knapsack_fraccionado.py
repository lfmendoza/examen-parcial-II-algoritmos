"""
Examen Parcial #2 - Análisis y Diseño de Algoritmos
Problema 2: Knapsack fraccionado

Un ladrón con una bolsa de capacidad W (en unidades u de peso) busca robar
el máximo valor posible de n artículos. El artículo i tiene precio p_i y
cantidad disponible w_i en u's. Es posible tomar fracciones a nivel de u's.

Paradigma: Greedy por densidad de valor v_i = p_i / w_i.
Justificación: el problema posee subestructura óptima y greedy-choice
property; la decisión local óptima es tomar todo lo posible del artículo
de mayor densidad.

Complejidad: O(n log n) por el ordenamiento, donde n es la cantidad de
artículos. La fase greedy posterior es O(n).
"""

from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Articulo:
    """Representa un artículo del problema."""
    nombre: str
    precio: float       # p_i: valor total si se toma w_i u's
    peso_total: int     # w_i: cantidad de u's disponibles

    @property
    def densidad(self) -> float:
        """v_i = p_i / w_i: valor por u."""
        return self.precio / self.peso_total


@dataclass
class Toma:
    """Cantidad tomada de un artículo en la solución."""
    articulo: Articulo
    cantidad_u: float   # u's tomadas (puede ser fraccional)

    @property
    def valor(self) -> float:
        """Valor obtenido por la cantidad tomada."""
        return self.cantidad_u * self.articulo.densidad


def knapsack_fraccionado(W: int, articulos: List[Articulo]) -> Tuple[List[Toma], float]:
    """
    Resuelve el problema del knapsack fraccionado.

    Args:
        W: capacidad en unidades u.
        articulos: lista de artículos disponibles.

    Returns:
        Tupla (tomas, valor_total) donde tomas es la lista de qué se tomó
        y cuánto, y valor_total es el valor robado.
    """
    if W < 0:
        raise ValueError("La capacidad debe ser no negativa.")

    # Paso 1: ordenar los artículos por densidad descendente.
    # Esta es la materialización de la elección greedy: priorizar el de
    # mayor v_i = p_i / w_i.
    ordenados = sorted(articulos, key=lambda a: a.densidad, reverse=True)

    tomas: List[Toma] = []
    capacidad_restante = W

    # Paso 2: avanzar por los artículos en orden descendente de densidad.
    # Por cada uno, tomar lo máximo posible: todo el artículo si cabe,
    # o solo lo que quepa de capacidad restante.
    for art in ordenados:
        if capacidad_restante == 0:
            break
        cantidad = min(art.peso_total, capacidad_restante)
        tomas.append(Toma(art, cantidad))
        capacidad_restante -= cantidad

    valor_total = sum(t.valor for t in tomas)
    return tomas, valor_total


def imprimir_resultado(W: int, articulos: List[Articulo],
                       tomas: List[Toma], valor: float) -> None:
    """Salida amigable para inspección humana."""
    print(f"Capacidad W = {W} u's")
    print("Artículos disponibles:")
    for a in articulos:
        print(f"  - {a.nombre}: p={a.precio}, w={a.peso_total}, "
              f"densidad={a.densidad:.3f}")
    print("Solución:")
    for t in tomas:
        print(f"  - {t.cantidad_u} u(s) de {t.articulo.nombre} "
              f"(valor parcial = {t.valor:.2f})")
    print(f"Valor total robado: {valor:.2f}")
    print()


# -------------------- Casos de prueba --------------------
if __name__ == "__main__":
    print("=" * 60)
    print("PROBLEMA 2 - KNAPSACK FRACCIONADO (greedy por densidad)")
    print("=" * 60)

    # Caso 1: ejemplo del enunciado.
    # item 1: $60, w=10  -> densidad 6
    # item 2: $100, w=20 -> densidad 5
    # item 3: $120, w=30 -> densidad 4
    # capacidad W = 50
    # Solución esperada: 10 de item1, 20 de item2, 20 de item3 -> 240
    print("Caso de prueba 1: ejemplo del enunciado")
    articulos1 = [
        Articulo("item 1", 60, 10),
        Articulo("item 2", 100, 20),
        Articulo("item 3", 120, 30),
    ]
    tomas1, valor1 = knapsack_fraccionado(50, articulos1)
    imprimir_resultado(50, articulos1, tomas1, valor1)

    # Caso 2: capacidad apenas excede al artículo de mayor densidad,
    # el siguiente por densidad solo cabe parcialmente.
    print("Caso de prueba 2: el knapsack se cierra con un artículo a fracción")
    articulos2 = [
        Articulo("oro", 500, 5),     # densidad 100
        Articulo("plata", 240, 8),   # densidad 30
        Articulo("cobre", 90, 15),   # densidad 6
    ]
    tomas2, valor2 = knapsack_fraccionado(10, articulos2)
    imprimir_resultado(10, articulos2, tomas2, valor2)
    # Esperado: 5 oro (500) + 5 plata (150) = 650

    # Caso 3: capacidad suficiente para todo.
    print("Caso de prueba 3: capacidad alcanza para todos los artículos")
    articulos3 = [
        Articulo("A", 30, 5),
        Articulo("B", 20, 4),
        Articulo("C", 10, 3),
    ]
    tomas3, valor3 = knapsack_fraccionado(20, articulos3)
    imprimir_resultado(20, articulos3, tomas3, valor3)
    # Esperado: todo -> valor 60

    # Caso 4: capacidad cero.
    print("Caso de prueba 4: capacidad nula")
    tomas4, valor4 = knapsack_fraccionado(0, articulos1)
    imprimir_resultado(0, articulos1, tomas4, valor4)

    # Caso 5: el peor artículo por densidad nunca se toma porque la
    # capacidad se llena antes.
    print("Caso de prueba 5: la densidad descendente excluye al peor artículo")
    articulos5 = [
        Articulo("alfa", 100, 4),    # densidad 25
        Articulo("beta", 90, 6),     # densidad 15
        Articulo("gamma", 50, 10),   # densidad 5
    ]
    tomas5, valor5 = knapsack_fraccionado(10, articulos5)
    imprimir_resultado(10, articulos5, tomas5, valor5)
    # Esperado: 4 alfa + 6 beta = 100+90 = 190
