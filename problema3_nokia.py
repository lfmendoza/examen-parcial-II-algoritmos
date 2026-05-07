"""
Examen Parcial #2 - Análisis y Diseño de Algoritmos
Problema 3: Combinaciones de n dígitos en el teclado Nokia 3230

Cuente la cantidad total de secuencias de n teclazos donde:
  a. Se puede comenzar con cualquier dígito (0-9).
  b. El siguiente teclazo debe ser arriba, abajo, a la izquierda o a
     la derecha del más reciente (incluyendo permanecer en la misma
     tecla, según se infiere del ejemplo n=2 -> 36 que incluye 00, 11,
     22, ..., 99).
  c. Las teclas '*' y '#' no se pueden presionar.

Paradigma: programación dinámica. El problema posee subestructura óptima
(en sentido de conteo) y subproblemas traslapados.

Caracterización: f(k, d) = número de secuencias de longitud k que
terminan en el dígito d.
Recurrencia:
    f(1, d) = 1                       para todo d en {0,...,9}
    f(k, d) = sum_{d' en N(d)} f(k-1, d')   para k >= 2
Donde N(d) son los vecinos válidos de d (incluyendo a d mismo).
Total = sum_{d=0..9} f(n, d).

Complejidad: O(n) tiempo (10 estados por nivel, sumas acotadas) y O(1)
memoria si se trabaja con dos arreglos rolling de tamaño 10.
"""

from typing import Dict, List


# Tabla de vecinos del teclado del Nokia 3230.
# Cada dígito tiene como vecinos a sí mismo y a las teclas que están
# directamente arriba, abajo, a la izquierda y a la derecha (siempre que
# no sean '*' ni '#').
#
# Layout del teclado:
#   1 2 3
#   4 5 6
#   7 8 9
#   * 0 #
#
# Verificación con n=2: |N(0)|+...+|N(9)| = 2+3+4+3+4+5+4+3+5+3 = 36. OK.
VECINOS: Dict[int, List[int]] = {
    0: [0, 8],
    1: [1, 2, 4],
    2: [1, 2, 3, 5],
    3: [2, 3, 6],
    4: [1, 4, 5, 7],
    5: [2, 4, 5, 6, 8],
    6: [3, 5, 6, 9],
    7: [4, 7, 8],
    8: [0, 5, 7, 8, 9],
    9: [6, 8, 9],
}


def contar_secuencias_nokia(n: int) -> int:
    """
    Cuenta el número de secuencias válidas de longitud n.

    Args:
        n: longitud de la secuencia (entero positivo).

    Returns:
        Número total de combinaciones válidas de n dígitos.
    """
    if n <= 0:
        raise ValueError("n debe ser entero positivo.")

    # Caso base: para longitud 1, hay exactamente una secuencia por cada
    # dígito (la secuencia de un solo teclazo).
    f = [1] * 10  # f[d] = f(1, d)

    # Iteración bottom-up: construimos f(k, d) a partir de f(k-1, d').
    # Solo mantenemos dos arreglos (rolling) porque cada nivel solo
    # depende del inmediato anterior.
    for _ in range(2, n + 1):
        nuevo_f = [0] * 10
        for d in range(10):
            # f(k, d) = suma de f(k-1, d') para todo d' vecino de d.
            nuevo_f[d] = sum(f[dp] for dp in VECINOS[d])
        f = nuevo_f

    return sum(f)


def listar_secuencias_nokia(n: int) -> List[str]:
    """
    Enumera todas las secuencias válidas (útil para validar conteos en
    tamaños pequeños). Para n grandes la lista crece exponencialmente,
    así que solo conviene para verificación.
    """
    if n <= 0:
        raise ValueError("n debe ser entero positivo.")

    # Empezamos con todas las secuencias de longitud 1.
    secuencias = [str(d) for d in range(10)]

    # Extendemos: cada secuencia se prolonga a sus vecinos válidos.
    for _ in range(n - 1):
        nuevas = []
        for s in secuencias:
            ultimo = int(s[-1])
            for dp in VECINOS[ultimo]:
                nuevas.append(s + str(dp))
        secuencias = nuevas

    return secuencias


# -------------------- Casos de prueba --------------------
if __name__ == "__main__":
    print("=" * 60)
    print("PROBLEMA 3 - COMBINACIONES NOKIA 3230 (programación dinámica)")
    print("=" * 60)

    # Caso 1: ejemplo del enunciado, n=2 -> 36.
    print("Caso de prueba 1: n = 2 (ejemplo del enunciado)")
    n = 2
    total = contar_secuencias_nokia(n)
    secuencias = listar_secuencias_nokia(n)
    print(f"  Total por DP: {total}")
    print(f"  Total por enumeración: {len(secuencias)}")
    print(f"  Primeras 16 secuencias enumeradas: {secuencias[:16]}")
    assert total == 36, "Inconsistencia con el ejemplo del enunciado"
    print("  Verificado contra el enunciado: 36 ✓")
    print()

    # Caso 2: caso base n=1 -> 10 (cada dígito por sí solo).
    print("Caso de prueba 2: n = 1 (caso base)")
    total = contar_secuencias_nokia(1)
    print(f"  Total: {total}")
    assert total == 10
    print("  Verificado: 10 ✓")
    print()

    # Caso 3: n=3, verificación cruzada DP vs enumeración exhaustiva.
    print("Caso de prueba 3: n = 3 (verificación cruzada DP vs enumeración)")
    total_dp = contar_secuencias_nokia(3)
    secuencias_3 = listar_secuencias_nokia(3)
    total_enum = len(secuencias_3)
    print(f"  Total por DP: {total_dp}")
    print(f"  Total por enumeración: {total_enum}")
    assert total_dp == total_enum, "DP y enumeración discrepan"
    print(f"  Coinciden: {total_dp} ✓")
    print()

    # Caso 4: n=5, verificación cruzada para confirmar correctitud.
    print("Caso de prueba 4: n = 5 (escala media, verificación cruzada)")
    total_dp = contar_secuencias_nokia(5)
    total_enum = len(listar_secuencias_nokia(5))
    print(f"  Total por DP: {total_dp}")
    print(f"  Total por enumeración: {total_enum}")
    assert total_dp == total_enum
    print(f"  Coinciden: {total_dp} ✓")
    print()

    # Caso 5: n grande, donde la enumeración sería inviable pero la DP
    # corre en milisegundos.
    print("Caso de prueba 5: n = 50 (la DP escala, la enumeración no)")
    total = contar_secuencias_nokia(50)
    print(f"  Total: {total}")
    print(f"  (Enumeración tendría tamaño del orden de 4^50 ≈ 1.27e30)")
    print()

    print("Todos los casos pasaron correctamente.")
