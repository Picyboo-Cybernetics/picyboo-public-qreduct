"""Executable demo for the mini Q-Reduct pipeline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Optional

from .chunking import chunk_bytes
from .constraints import assemble_constraints
from .oracle_sim import recover_missing_chunk


SAMPLE_PAYLOAD = b"Q-Reduct demo payload."


def load_payload(path: Optional[Path]) -> bytes:
    if path is None:
        return SAMPLE_PAYLOAD
    return path.read_bytes()


def run_demo(path: Optional[Path], chunk_size: int, parity_bits: int) -> dict:
    payload = load_payload(path)
    chunks = chunk_bytes(payload, chunk_size=chunk_size)
    bundle = assemble_constraints(chunks, parity_bits=parity_bits)
    missing_index = len(chunks) - 1
    result = recover_missing_chunk(bundle, missing_index)

    return {
        "original_payload": payload.decode("utf-8", errors="replace"),
        "chunk_count": len(chunks),
        "chunk_size": chunk_size,
        "parity_bits": parity_bits,
        "constraints": [
            {
                "index": c.index,
                "digest": c.digest,
                "syndrome": c.syndrome,
                "merkle_path": c.merkle_path,
            }
            for c in bundle.chunks
        ],
        "merkle_root": bundle.merkle_root,
        "recovery": {
            "missing_index": missing_index,
            "candidate_bits": bundle.chunk_size * 8,
            "classical_checked": result.checked_candidates,
            "grover_iterations": result.quantum_iterations,
            "recovered_chunk_hex": result.recovered_chunk.data.hex(),
        },
    }


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "payload",
        nargs="?",
        type=Path,
        help="Optional path to the payload file. Uses a demo string when omitted.",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=1,
        help="Chunk size in bytes (small values keep the brute-force search tractable).",
    )
    parser.add_argument(
        "--parity-bits",
        type=int,
        default=4,
        help="Number of parity rows used to build the syndrome.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON instead of a human-readable summary.",
    )
    args = parser.parse_args(argv)

    report = run_demo(args.payload, args.chunk_size, args.parity_bits)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("Payload:", report["original_payload"])
        print("Chunk count:", report["chunk_count"])
        print("Merkle root:", report["merkle_root"])
        print("Recovered chunk (hex):", report["recovery"]["recovered_chunk_hex"])
        print("Classical candidates checked:", report["recovery"]["classical_checked"])
        print("Estimated Grover iterations:", f"{report['recovery']['grover_iterations']:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
