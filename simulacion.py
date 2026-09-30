"""
Lógica de la simulación Monte Carlo de rachas de caras.

Este módulo no depende de ninguna interfaz: solo calcula y devuelve datos.
"""

import random
from dataclasses import dataclass
from statistics import mean, median
from typing import Callable, Optional


def experimento_continuo(largo_racha: int = 12, rng: Optional[random.Random] = None) -> int:
    """
    Lanza una moneda continuamente hasta obtener `largo_racha` caras seguidas.
    Retorna la cantidad total de lanzamientos que fueron necesarios.
    """
    rng = rng or random
    lanzamientos_totales = 0
    racha_caras = 0

    while racha_caras < largo_racha:
        lanzamientos_totales += 1
        moneda = rng.getrandbits(1)  # 1 es Cara, 0 es Cruz

        if moneda == 1:
            racha_caras += 1
        else:
            racha_caras = 0  # Se rompe la racha, volvemos a cero

    return lanzamientos_totales


def valor_esperado_teorico(largo_racha: int) -> int:
    """Valor esperado exacto de lanzamientos para n caras seguidas: 2^(n+1) - 2."""
    return 2 ** (largo_racha + 1) - 2


@dataclass
class ResultadoSimulacion:
    lanzamientos: list[int]
    largo_racha: int

    @property
    def promedio(self) -> float:
        return mean(self.lanzamientos)

    @property
    def mediana(self) -> float:
        return median(self.lanzamientos)

    @property
    def minimo(self) -> int:
        return min(self.lanzamientos)

    @property
    def maximo(self) -> int:
        return max(self.lanzamientos)

    @property
    def teorico(self) -> int:
        return valor_esperado_teorico(self.largo_racha)

    def promedios_acumulados(self) -> list[float]:
        """Promedio acumulado tras cada simulación (muestra la convergencia)."""
        acumulado = 0
        promedios = []
        for i, valor in enumerate(self.lanzamientos, start=1):
            acumulado += valor
            promedios.append(acumulado / i)
        return promedios


def simulacion_monte_carlo_continuo(
    num_simulaciones: int = 10000,
    largo_racha: int = 12,
    semilla: Optional[int] = None,
    al_progresar: Optional[Callable[[int, int], None]] = None,
) -> ResultadoSimulacion:
    """
    Ejecuta el experimento de lanzamientos continuos múltiples veces.

    `al_progresar(completadas, total)` se invoca periódicamente para que la
    interfaz pueda mostrar el avance sin que esta lógica la conozca.
    """
    if num_simulaciones < 1:
        raise ValueError("num_simulaciones debe ser al menos 1")
    if largo_racha < 1:
        raise ValueError("largo_racha debe ser al menos 1")

    rng = random.Random(semilla)
    paso_progreso = max(1, num_simulaciones // 100)
    lanzamientos = []

    for i in range(1, num_simulaciones + 1):
        lanzamientos.append(experimento_continuo(largo_racha, rng))
        if al_progresar and (i % paso_progreso == 0 or i == num_simulaciones):
            al_progresar(i, num_simulaciones)

    return ResultadoSimulacion(lanzamientos=lanzamientos, largo_racha=largo_racha)


if __name__ == "__main__":
    resultado = simulacion_monte_carlo_continuo(10000)
    print("-" * 50)
    print("RESULTADOS DE LA SIMULACIÓN (Lanzamientos continuos)")
    print(f"Promedio de lanzamientos necesarios: {resultado.promedio:.2f}")
    print(f"Valor teórico esperado: {resultado.teorico}")
