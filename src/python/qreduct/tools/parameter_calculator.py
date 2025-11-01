"""Interactive parameter helper for the Q-Reduct whitepaper prototype."""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass, asdict

from ..quantum.mock_oracle import GroverIterationEstimator


@dataclass
class ParameterReport:
    file_size: int
    chunk_size: int
    chunk_count: int
    digest_bits: int
    parity_bits: int
    merkle_branch_bits: int
    constraint_bits_per_chunk: int
    total_constraint_size: int
    storage_ratio: float
    classical_candidates: int
    grover_iterations: float


DEFAULT_DIGEST_BITS = 256


def estimate_merkle_branch_bits(chunk_count: int, digest_bits: int) -> int:
    if chunk_count <= 1:
        return 0
    levels = math.ceil(math.log(chunk_count, 2))
    return levels * digest_bits


def build_report(file_size: int, chunk_size: int, parity_bits: int, digest_bits: int = DEFAULT_DIGEST_BITS) -> ParameterReport:
    chunk_count = math.ceil(file_size / chunk_size)
    merkle_branch_bits = estimate_merkle_branch_bits(chunk_count, digest_bits)
    constraint_bits_per_chunk = digest_bits + parity_bits + merkle_branch_bits
    total_constraint_size = math.ceil(constraint_bits_per_chunk / 8) * chunk_count
    storage_ratio = total_constraint_size / file_size if file_size else 0.0
    classical_candidates = 1 << (chunk_size * 8)
    grover_estimator = GroverIterationEstimator(search_space=classical_candidates, solutions=1)
    return ParameterReport(
        file_size=file_size,
        chunk_size=chunk_size,
        chunk_count=chunk_count,
        digest_bits=digest_bits,
        parity_bits=parity_bits,
        merkle_branch_bits=merkle_branch_bits,
        constraint_bits_per_chunk=constraint_bits_per_chunk,
        total_constraint_size=total_constraint_size,
        storage_ratio=storage_ratio,
        classical_candidates=classical_candidates,
        grover_iterations=grover_estimator.estimated_iterations(),
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file_size", type=int, help="Original file size in bytes")
    parser.add_argument("chunk_size", type=int, help="Chunk size in bytes")
    parser.add_argument("--parity-bits", type=int, default=32, help="Parity bits per chunk")
    parser.add_argument("--digest-bits", type=int, default=DEFAULT_DIGEST_BITS, help="Digest bit-length")
    parser.add_argument("--json", action="store_true", help="Emit JSON for integration with web tools")
    args = parser.parse_args(argv)

    report = build_report(args.file_size, args.chunk_size, args.parity_bits, args.digest_bits)
    if args.json:
        print(json.dumps(asdict(report), indent=2))
    else:
        print(f"File size: {report.file_size} bytes")
        print(f"Chunk size: {report.chunk_size} bytes")
        print(f"Chunk count: {report.chunk_count}")
        print(f"Constraint size per chunk: {report.constraint_bits_per_chunk} bits")
        print(f"Total constraint footprint: {report.total_constraint_size} bytes")
        print(f"Storage ratio (constraints/original): {report.storage_ratio:.2%}")
        print(f"Classical search space: {report.classical_candidates} candidates")
        print(f"Grover iterations (est.): {report.grover_iterations:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
