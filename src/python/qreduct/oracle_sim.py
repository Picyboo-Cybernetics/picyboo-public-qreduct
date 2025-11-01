"""Classical and quantum-inspired oracle simulations for the demo."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .chunking import Chunk
from .constraints import ChunkConstraints, ConstraintBundle, compute_syndrome, sha256_digest
from .quantum.mock_oracle import GroverIterationEstimator


@dataclass
class OracleResult:
    """Result returned by a simulated oracle search."""

    recovered_chunk: Chunk
    checked_candidates: int
    quantum_iterations: float


class ExhaustiveOracle:
    """Brute-force search that enumerates all possible chunk values."""

    def __init__(self, bundle: ConstraintBundle, target: ChunkConstraints) -> None:
        self.bundle = bundle
        self.target = target

    @property
    def candidate_bits(self) -> int:
        return self.bundle.chunk_size * 8

    def iterate_candidates(self) -> Iterable[bytes]:
        for value in range(1 << self.candidate_bits):
            yield value.to_bytes(self.bundle.chunk_size, byteorder="big")

    def search(self) -> OracleResult:
        parity_matrix = self.bundle.parity_matrix
        iterations = 0
        for candidate in self.iterate_candidates():
            iterations += 1
            digest = sha256_digest(candidate)
            if digest != self.target.digest:
                continue
            chunk = Chunk(index=self.target.index, data=candidate)
            syndrome = compute_syndrome(chunk, parity_matrix)
            if list(syndrome) != list(self.target.syndrome):
                continue
            quantum_estimator = GroverIterationEstimator(
                search_space=1 << self.candidate_bits, solutions=1
            )
            return OracleResult(
                recovered_chunk=chunk,
                checked_candidates=iterations,
                quantum_iterations=quantum_estimator.estimated_iterations(),
            )
        raise ValueError("No candidate satisfied the provided constraints")


def recover_missing_chunk(bundle: ConstraintBundle, missing_index: int) -> OracleResult:
    """Simulate classical recovery of a missing chunk."""

    target = next(constraint for constraint in bundle.chunks if constraint.index == missing_index)
    oracle = ExhaustiveOracle(bundle, target)
    return oracle.search()
