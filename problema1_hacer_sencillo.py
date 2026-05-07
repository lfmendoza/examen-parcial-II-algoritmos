"""
Examen Parcial #2 - Análisis y Diseño de Algoritmos
Problema 1: Hacer sencillo

Dado un monto m (en centavos), encontrar la cantidad mínima de monedas
necesarias para alcanzarlo, usando denominaciones {1, 5, 10, 25}.

Paradigma: Greedy. Justificación: el problema posee subestructura óptima
y greedy-choice property. El conjunto canónico {1, 5, 10, 25} garantiza
que la decisión local (tomar la moneda más grande posible) es siempre
parte de alguna solución óptima.

Complejidad: O(|D|) por monto. En este caso |D| = 4, por lo que es O(1)
en términos de denominaciones, independiente de m.
"""

from typing import List, Tuple


# Denominaciones disponibles, ordenadas en forma descendente.
# El orden descendente es lo que materializa la "elección greedy".
DENOMINACIONES: List[int] = [25, 10, 5, 1]


def hacer_sencillo(m: int, denominaciones: List[int] = DENOMINACIONES) -> List[Tuple[int, int]]:
    """
    Devuelve la descomposición mínima de m como lista de (denominación, cantidad).

    Args:
        m: monto a alcanzar, expresado como entero (e.g., centavos).
        denominaciones: lista de denominaciones disponibles. Debe estar ordenada
                        en forma descendente para que el algoritmo greedy opere
                        correctamente sobre el sistema canónico {1, 5, 10, 25}.

    Returns:
        Lista de pares (d, k) significando "k monedas de denominación d".
        Solo se incluyen denominaciones con k > 0.
    """
    if m < 0:
        raise ValueError("El monto debe ser no negativo.")

    resultado: List[Tuple[int, int]] = []
    restante = m

    # Por cada denominación d en orden descendente, tomamos la cantidad
    # máxima de monedas de d que cabe dentro del monto restante.
    for d in denominaciones:
        if restante == 0:
            break
        cantidad = restante // d
        if cantidad > 0:
            resultado.append((d, cantidad))
            restante -= cantidad * d

    # Postcondición: si las denominaciones incluyen 1, restante siempre llega a 0.
    assert restante == 0, "El sistema de denominaciones no alcanza el monto exactamente."
    return resultado


def total_monedas(descomposicion: List[Tuple[int, int]]) -> int:
    """Suma de monedas usadas en la descomposición."""
    return sum(k for _, k in descomposicion)


def imprimir_resultado(m: int, descomposicion: List[Tuple[int, int]]) -> None:
    """Salida amigable para inspección humana."""
    print(f"Monto objetivo: Q{m / 100:.2f}  ({m} centavos)")
    print(f"Total de monedas: {total_monedas(descomposicion)}")
    for d, k in descomposicion:
        print(f"  - {k} moneda(s) de Q{d / 100:.2f}")
    print()


# -------------------- Casos de prueba --------------------
if __name__ == "__main__":
    print("=" * 60)
    print("PROBLEMA 1 - HACER SENCILLO (greedy)")
    print("=" * 60)
    print(f"Denominaciones (orden descendente): {DENOMINACIONES}")
    print()

    # Caso 1: ejemplo del enunciado (Q2.93 = 293 centavos)
    print("Caso de prueba 1: monto del enunciado")
    descomp = hacer_sencillo(293)
    imprimir_resultado(293, descomp)
    # Esperado: 11x25 + 1x10 + 1x5 + 3x1 = 16 monedas

    # Caso 2: monto que cae justo en una denominación
    print("Caso de prueba 2: monto exactamente divisible por la mayor denominación")
    descomp = hacer_sencillo(100)
    imprimir_resultado(100, descomp)
    # Esperado: 4 monedas de 25

    # Caso 3: monto pequeño donde no aplica la mayor denominación
    print("Caso de prueba 3: monto menor a la mayor denominación")
    descomp = hacer_sencillo(17)
    imprimir_resultado(17, descomp)
    # Esperado: 1x10 + 1x5 + 2x1 = 4 monedas

    # Caso 4: cero (caso borde)
    print("Caso de prueba 4: monto cero")
    descomp = hacer_sencillo(0)
    imprimir_resultado(0, descomp)
    # Esperado: 0 monedas

    # Caso 5: monto grande
    print("Caso de prueba 5: monto grande")
    descomp = hacer_sencillo(9_999)
    imprimir_resultado(9_999, descomp)
