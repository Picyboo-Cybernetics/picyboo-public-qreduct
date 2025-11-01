"""Simple evaluation helpers for the Q-Reduct reference prototype."""

from __future__ import annotations

import argparse
import time
from dataclasses import dataclass

from ..chunking import chunk_bytes
from ..constraints import assemble_constraints
from ..oracle_sim import ExhaustiveOracle


@dataclass
class BenchmarkResult:
    chunk_bits: int
    elapsed: float
    candidates_examined: int


def run_benchmark(payload: bytes, chunk_size: int, parity_bits: int) -> BenchmarkResult:
    chunks = chunk_bytes(payload, chunk_size)
    bundle = assemble_constraints(chunks, parity_bits=parity_bits)
    target = bundle.chunks[-1]
    oracle = ExhaustiveOracle(bundle, target)

    start = time.perf_counter()
    result = oracle.search()
    elapsed = time.perf_counter() - start

    return BenchmarkResult(
        chunk_bits=bundle.chunk_size * 8,
        elapsed=elapsed,
        candidates_examined=result.checked_candidates,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("payload", type=str, help="Payload string to benchmark")
    parser.add_argument("--chunk-size", type=int, default=1, help="Chunk size in bytes")
    parser.add_argument("--parity-bits", type=int, default=4, help="Parity rows")
    args = parser.parse_args()

    result = run_benchmark(args.payload.encode("utf-8"), args.chunk_size, args.parity_bits)
    print(f"Chunk bits: {result.chunk_bits}")
    print(f"Candidates examined: {result.candidates_examined}")
    print(f"Elapsed time: {result.elapsed * 1000:.3f} ms")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
