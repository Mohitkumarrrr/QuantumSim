"""
Quantum gate definitions as unitary matrices.

All single-qubit gates are 2×2 complex numpy arrays.  Multi-qubit gates
(e.g. CNOT, SWAP) are 4×4 matrices operating on the tensor-product space.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


class Gates:
    """Library of standard quantum gates."""

    # ── Pauli gates ────────────────────────────────────────────────────
    @staticmethod
    def X() -> NDArray[np.complexfloating]:
        """Pauli-X (NOT) gate — bit flip."""
        return np.array([[0, 1], [1, 0]], dtype=complex)

    @staticmethod
    def Y() -> NDArray[np.complexfloating]:
        """Pauli-Y gate."""
        return np.array([[0, -1j], [1j, 0]], dtype=complex)

    @staticmethod
    def Z() -> NDArray[np.complexfloating]:
        """Pauli-Z gate — phase flip."""
        return np.array([[1, 0], [0, -1]], dtype=complex)

    # ── Hadamard ───────────────────────────────────────────────────────
    @staticmethod
    def H() -> NDArray[np.complexfloating]:
        """Hadamard gate — creates superposition."""
        return np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)

    # ── Phase gates ────────────────────────────────────────────────────
    @staticmethod
    def S() -> NDArray[np.complexfloating]:
        """S gate (π/2 phase)."""
        return np.array([[1, 0], [0, 1j]], dtype=complex)

    @staticmethod
    def T() -> NDArray[np.complexfloating]:
        """T gate (π/4 phase)."""
        return np.array(
            [[1, 0], [0, np.exp(1j * np.pi / 4)]],
            dtype=complex,
        )

    @staticmethod
    def Phase(phi: float) -> NDArray[np.complexfloating]:
        """General phase gate R_φ with arbitrary angle *phi* (radians)."""
        return np.array(
            [[1, 0], [0, np.exp(1j * phi)]],
            dtype=complex,
        )

    # ── Rotation gates ─────────────────────────────────────────────────
    @staticmethod
    def Rx(theta: float) -> NDArray[np.complexfloating]:
        """Rotation about the X-axis by *theta* radians."""
        c = np.cos(theta / 2)
        s = np.sin(theta / 2)
        return np.array([[c, -1j * s], [-1j * s, c]], dtype=complex)

    @staticmethod
    def Ry(theta: float) -> NDArray[np.complexfloating]:
        """Rotation about the Y-axis by *theta* radians."""
        c = np.cos(theta / 2)
        s = np.sin(theta / 2)
        return np.array([[c, -s], [s, c]], dtype=complex)

    @staticmethod
    def Rz(theta: float) -> NDArray[np.complexfloating]:
        """Rotation about the Z-axis by *theta* radians."""
        return np.array(
            [[np.exp(-1j * theta / 2), 0], [0, np.exp(1j * theta / 2)]],
            dtype=complex,
        )

    # ── Multi-qubit gates ──────────────────────────────────────────────
    @staticmethod
    def CNOT() -> NDArray[np.complexfloating]:
        """Controlled-NOT gate (control ⊗ target)."""
        return np.array(
            [[1, 0, 0, 0],
             [0, 1, 0, 0],
             [0, 0, 0, 1],
             [0, 0, 1, 0]],
            dtype=complex,
        )

    @staticmethod
    def SWAP() -> NDArray[np.complexfloating]:
        """SWAP gate."""
        return np.array(
            [[1, 0, 0, 0],
             [0, 0, 1, 0],
             [0, 1, 0, 0],
             [0, 0, 0, 1]],
            dtype=complex,
        )

    @staticmethod
    def CZ() -> NDArray[np.complexfloating]:
        """Controlled-Z gate."""
        return np.array(
            [[1, 0, 0, 0],
             [0, 1, 0, 0],
             [0, 0, 1, 0],
             [0, 0, 0, -1]],
            dtype=complex,
        )

    @staticmethod
    def Toffoli() -> NDArray[np.complexfloating]:
        """Toffoli (CCNOT) gate — 8×8 matrix on 3 qubits."""
        gate = np.eye(8, dtype=complex)
        gate[6, 6] = 0
        gate[7, 7] = 0
        gate[6, 7] = 1
        gate[7, 6] = 1
        return gate

    # ── Custom gate builder ────────────────────────────────────────────
    @staticmethod
    def custom(matrix: NDArray[np.complexfloating]) -> NDArray[np.complexfloating]:
        """Validate and return a custom unitary gate.

        Args:
            matrix: A square complex matrix.

        Raises:
            ValueError: If the matrix is not unitary.
        """
        mat = np.asarray(matrix, dtype=complex)
        n = mat.shape[0]
        if mat.shape != (n, n):
            raise ValueError("Gate matrix must be square.")
        product = mat @ mat.conj().T
        if not np.allclose(product, np.eye(n), atol=1e-8):
            raise ValueError("Gate matrix must be unitary (U·U† = I).")
        return mat
