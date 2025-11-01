"""Quantum-inspired helper utilities.

The intent is not to implement Grover's search exactly but to expose the API
surface that future quantum integrations would occupy.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class GroverIterationEstimator:
    """Rough estimate of the Grover iteration count for a given search space."""

    search_space: int
    solutions: int

    def estimated_iterations(self) -> float:
        if self.solutions <= 0:
            raise ValueError("solutions must be positive")
        if self.search_space <= 0:
            raise ValueError("search_space must be positive")
        ratio = self.solutions / self.search_space
        ratio = max(min(ratio, 1.0), 1e-18)
        return math.pi / 4 * math.sqrt(1 / ratio)

    def success_probability(self, iterations: int) -> float:
        theta = math.asin(math.sqrt(self.solutions / self.search_space))
        return math.sin((2 * iterations + 1) * theta) ** 2


def amplitude_after_iterations(iterations: int, search_space: int, solutions: int = 1) -> float:
    """Return the amplitude on the marked states after Grover iterations."""

    estimator = GroverIterationEstimator(search_space=search_space, solutions=solutions)
    theta = math.asin(math.sqrt(estimator.solutions / estimator.search_space))
    return math.sin((2 * iterations + 1) * theta)
