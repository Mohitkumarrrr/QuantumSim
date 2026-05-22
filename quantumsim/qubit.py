"""
Qubit representation and single-qubit operations.

A qubit is represented as a 2-element complex state vector |ψ⟩ = α|0⟩ + β|1⟩
where |α|² + |β|² = 1.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from typing import Tuple


class Qubit:
    """A single qubit with state vector representation.

    Attributes:
        state: Complex state vector [α, β] representing α|0⟩ + β|1⟩.
    """

    def __init__(
        self,
        alpha: complex = 1.0 + 0j,
        beta: complex = 0.0 + 0j,
    ) -> None:
        """Initialise a qubit in the state α|0⟩ + β|1⟩.

        Args:
            alpha: Amplitude for |0⟩ basis state.
            beta: Amplitude for |1⟩ basis state.

        Raises:
            ValueError: If the state vector is not normalisable.
        """
        state = np.array([alpha, beta], dtype=complex)
        norm = np.linalg.norm(state)
        if norm < 1e-12:
            raise ValueError("State vector cannot be the zero vector.")
        self.state: NDArray[np.complexfloating] = state / norm

    # ── Factory helpers ─────────────────────────────────────────────────
    @classmethod
    def zero(cls) -> "Qubit":
        """Return |0⟩."""
        return cls(1.0, 0.0)

    @classmethod
    def one(cls) -> "Qubit":
        """Return |1⟩."""
        return cls(0.0, 1.0)

    @classmethod
    def plus(cls) -> "Qubit":
        """Return |+⟩ = (|0⟩ + |1⟩) / √2."""
        return cls(1.0, 1.0)

    @classmethod
    def minus(cls) -> "Qubit":
        """Return |−⟩ = (|0⟩ − |1⟩) / √2."""
        return cls(1.0, -1.0)

    # ── Probabilities & measurement ────────────────────────────────────
    def probabilities(self) -> Tuple[float, float]:
        """Return (P(|0⟩), P(|1⟩))."""
        p0 = float(np.abs(self.state[0]) ** 2)
        p1 = float(np.abs(self.state[1]) ** 2)
        return (p0, p1)

    def measure(self) -> int:
        """Perform a projective measurement, collapsing the state.

        Returns:
            0 or 1 — the measured basis state.
        """
        p0, _ = self.probabilities()
        outcome = 0 if np.random.random() < p0 else 1
        self.state = np.array(
            [1.0 + 0j, 0.0 + 0j] if outcome == 0 else [0.0 + 0j, 1.0 + 0j]
        )
        return outcome

    # ── Bloch sphere ───────────────────────────────────────────────────
    def bloch_coordinates(self) -> Tuple[float, float, float]:
        """Compute the Bloch sphere coordinates (x, y, z).

        Uses the density-matrix expectation values of the Pauli operators:
            x = 2·Re(α*β),  y = 2·Im(α*β),  z = |α|² − |β|²
        """
        alpha, beta = self.state
        x = float(2.0 * np.real(np.conj(alpha) * beta))
        y = float(2.0 * np.imag(np.conj(alpha) * beta))
        z = float(np.abs(alpha) ** 2 - np.abs(beta) ** 2)
        return (x, y, z)

    # ── Representation ─────────────────────────────────────────────────
    def __repr__(self) -> str:
        a, b = self.state
        return f"Qubit(α={a:.4f}, β={b:.4f})"

    def __str__(self) -> str:
        a, b = self.state
        parts: list[str] = []
        if np.abs(a) > 1e-10:
            parts.append(f"({a:.4f})|0⟩")
        if np.abs(b) > 1e-10:
            parts.append(f"({b:.4f})|1⟩")
        return " + ".join(parts) if parts else "0"
