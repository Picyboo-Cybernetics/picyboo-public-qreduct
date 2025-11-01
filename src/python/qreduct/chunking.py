"""Chunking utilities for the Q-Reduct demo pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass
class Chunk:
    """Represents a fixed-size chunk of the original payload."""

    index: int
    data: bytes

    def bit_length(self) -> int:
        """Return the number of meaningful bits in this chunk."""

        return len(self.data) * 8


def chunk_bytes(data: bytes, chunk_size: int) -> List[Chunk]:
    """Split *data* into equally sized :class:`Chunk` objects.

    The final chunk is padded with zero bytes purely for presentation purposes.
    The caller is expected to track the real payload length separately when
    creating constraints.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    chunks: List[Chunk] = []
    for idx in range(0, len(data), chunk_size):
        window = data[idx : idx + chunk_size]
        if len(window) < chunk_size:
            window = window.ljust(chunk_size, b"\x00")
        chunks.append(Chunk(index=len(chunks), data=window))
    return chunks


def chunk_from_iterable(values: Iterable[int], chunk_size: int) -> List[Chunk]:
    """Helper that builds a bytes object from an iterable before chunking."""

    return chunk_bytes(bytes(values), chunk_size)
