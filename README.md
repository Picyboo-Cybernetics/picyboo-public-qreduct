# Q-Reduct: Quantum-Ready Erasure Codec

**Series:** Picyboo Public Research Series  
**Organization:** Picyboo Cybernetics Inc., Research Lab (Canada)

**Keywords:** Quantum Algorithms, Grover Search, Information Theory, Constraint Satisfaction, Lossless Compression, Post-Quantum Storage, Computational Complexity, Data Density

## About Picyboo Cybernetics

We develop advanced systems across quantum computing, artificial intelligence, and decentralized networks to enable the next generation of technology. Therefore, we distribute select frameworks, implementations, and development tools as open source—enabling developers and institutions to build on our technology foundation.

## Overview

Breakthrough: Reducing Data Storage to 10%–20% of Original Size – The Future of Post-Quantum Infrastructure

Classical compression algorithms achieve 60–70% reduction by exploiting statistical patterns; Q-Reduct achieves 80–90% reduction by solving the inverse problem – encoding only the mathematical constraints that uniquely specify the original data, then reconstructing content through constraint satisfaction. Classical reconstruction is intentionally made computationally infeasible; quantum algorithms using Grover search reduce the computational cost from O(2^n) to O(2^(n/2)), making decoding practical on future quantum hardware. This establishes a fundamentally different information-theoretic paradigm where storage density and reconstruction complexity are deliberately decoupled.

## Whitepaper

- PDF: docs/halenta-q-reduct-quantum-ready-erasure-codec-for-extreme-storage-reduction-2025-10-09-v1_3.pdf  
- DOI: https://doi.org/10.5281/zenodo.17455524

## Repository Purpose

Public research reference for industry and collaborators. Mirrors the technical whitepaper and provides stubs for reference implementations or models.

## Contents

### Educational Prototype

The repository now ships a minimal, fully documented prototype pipeline in `src/python/qreduct/`. It demonstrates how chunks, constraint generation (digests, linear syndromes, Merkle commitments) and an oracle-guided recovery step fit together on tiny payloads. The code is intentionally small so it can run on commodity hardware while mirroring the concepts described in the whitepaper.

```bash
PYTHONPATH=src/python python -m qreduct.demo --chunk-size 1 --parity-bits 4
```

The demo prints the generated constraints, recomputes a missing chunk through brute force, and reports the equivalent Grover iteration budget for the same search space.

### Evaluation Sandbox

To reproduce the "classically impractical" behaviour on bite-sized data sets, run the benchmark helper:

```bash
PYTHONPATH=src/python python -m qreduct.eval.bruteforce_demo "Hello" --chunk-size 1 --parity-bits 4
```

The script measures how many classical candidates are examined when recovering the final chunk, and records the elapsed time.

### Parameter Calculator / Web Integration Hook

`src/python/qreduct/tools/parameter_calculator.py` summarises the storage footprint and classical vs. Grover search budgets for any `(file_size, chunk_size, parity_bits)` tuple. The tool is designed to feed a future web-based calculator—use the `--json` flag to export structured output that can be consumed by your sandbox or dashboard.

```bash
PYTHONPATH=src/python python -m qreduct.tools.parameter_calculator 1048576 32 --parity-bits 64 --json
```

The JSON payload contains everything required to recreate the view on a website (chunk counts, constraint sizes, Grover iteration estimates, etc.).

### Quantum Integration Shim

`src/python/qreduct/quantum/mock_oracle.py` introduces a lightweight abstraction that mirrors the interface future Grover-based oracles would expose. The estimator is already used by the CLI demos so downstream projects can be built around the same API and later swap in a real quantum backend.

## Status

Openly published for transparency. Implementation stubs and educational prototypes included. Roadmaps and production code will be added as they mature.

## How to Cite

> Halenta, D. N. (2025). *Q-Reduct: Quantum-Ready Erasure Codec.* Picyboo Cybernetics Inc.  
> DOI: https://doi.org/10.5281/zenodo.17455524

## Links

- Website: https://picyboo.com
- Technical Sandbox: https://picyboo.net
- GitHub Organization: https://github.com/Picyboo-Cybernetics