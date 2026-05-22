"""
Quantum circuit construction and text-diagram rendering.

A circuit holds an ordered list of gate operations that can be applied
to a multi-qubit state vector by the Simulator.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple

import numpy as np
from numpy.typing import NDArray

from quantumsim.gates import Gates


@dataclass
class GateOp:
    """A single gate operation inside a circuit.

    Attributes:
        name: Human-readable gate name (e.g. "H", "CNOT").
        matrix: Unitary matrix for the gate.
        targets: Qubit indices the gate acts on.
    """
    name: str
    matrix: NDArray[np.complexfloating]
    targets: Tuple[int, ...]


class QuantumCircuit:
    """Builder for a sequence of quantum gate operations.

    Args:
        num_qubits: Number of qubits in the circuit.
    """

    def __init__(self, num_qubits: int) -> None:
        if num_qubits < 1:
            raise ValueError("Circuit must have at least 1 qubit.")
        self.num_qubits: int = num_qubits
        self.operations: List[GateOp] = []
        self._measurements: List[int] = []

    # ── Gate helpers (single-qubit) ────────────────────────────────────
    def h(self, target: int) -> "QuantumCircuit":
        """Apply Hadamard gate."""
        self._validate_qubit(target)
        self.operations.append(GateOp("H", Gates.H(), (target,)))
        return self

    def x(self, target: int) -> "QuantumCircuit":
        """Apply Pauli-X gate."""
        self._validate_qubit(target)
        self.operations.append(GateOp("X", Gates.X(), (target,)))
        return self

    def y(self, target: int) -> "QuantumCircuit":
        """Apply Pauli-Y gate."""
        self._validate_qubit(target)
        self.operations.append(GateOp("Y", Gates.Y(), (target,)))
        return self

    def z(self, target: int) -> "QuantumCircuit":
        """Apply Pauli-Z gate."""
        self._validate_qubit(target)
        self.operations.append(GateOp("Z", Gates.Z(), (target,)))
        return self

    def s(self, target: int) -> "QuantumCircuit":
        """Apply S gate."""
        self._validate_qubit(target)
        self.operations.append(GateOp("S", Gates.S(), (target,)))
        return self

    def t(self, target: int) -> "QuantumCircuit":
        """Apply T gate."""
        self._validate_qubit(target)
        self.operations.append(GateOp("T", Gates.T(), (target,)))
        return self

    def rx(self, target: int, theta: float) -> "QuantumCircuit":
        """Apply Rx rotation gate."""
        self._validate_qubit(target)
        self.operations.append(GateOp(f"Rx({theta:.2f})", Gates.Rx(theta), (target,)))
        return self

    def ry(self, target: int, theta: float) -> "QuantumCircuit":
        """Apply Ry rotation gate."""
        self._validate_qubit(target)
        self.operations.append(GateOp(f"Ry({theta:.2f})", Gates.Ry(theta), (target,)))
        return self

    def rz(self, target: int, theta: float) -> "QuantumCircuit":
        """Apply Rz rotation gate."""
        self._validate_qubit(target)
        self.operations.append(GateOp(f"Rz({theta:.2f})", Gates.Rz(theta), (target,)))
        return self

    # ── Multi-qubit gates ──────────────────────────────────────────────
    def cx(self, control: int, target: int) -> "QuantumCircuit":
        """Apply CNOT (CX) gate."""
        self._validate_qubit(control)
        self._validate_qubit(target)
        if control == target:
            raise ValueError("Control and target must differ.")
        self.operations.append(GateOp("CX", Gates.CNOT(), (control, target)))
        return self

    def cz(self, control: int, target: int) -> "QuantumCircuit":
        """Apply Controlled-Z gate."""
        self._validate_qubit(control)
        self._validate_qubit(target)
        self.operations.append(GateOp("CZ", Gates.CZ(), (control, target)))
        return self

    def swap(self, q1: int, q2: int) -> "QuantumCircuit":
        """Apply SWAP gate."""
        self._validate_qubit(q1)
        self._validate_qubit(q2)
        self.operations.append(GateOp("SWAP", Gates.SWAP(), (q1, q2)))
        return self

    def add_gate(
        self,
        name: str,
        matrix: NDArray[np.complexfloating],
        targets: Tuple[int, ...],
    ) -> "QuantumCircuit":
        """Add an arbitrary gate to the circuit.

        Args:
            name: Display name.
            matrix: Unitary matrix.
            targets: Qubit indices the gate acts on.
        """
        for t in targets:
            self._validate_qubit(t)
        self.operations.append(GateOp(name, np.asarray(matrix, dtype=complex), targets))
        return self

    # ── Measurement ────────────────────────────────────────────────────
    def measure(self, qubits: Optional[List[int]] = None) -> "QuantumCircuit":
        """Mark qubits for measurement at the end of the circuit.

        Args:
            qubits: Qubit indices to measure.  ``None`` measures all.
        """
        if qubits is None:
            qubits = list(range(self.num_qubits))
        for q in qubits:
            self._validate_qubit(q)
        self._measurements = qubits
        return self

    @property
    def measured_qubits(self) -> List[int]:
        """Return the list of qubit indices marked for measurement."""
        return self._measurements if self._measurements else list(range(self.num_qubits))

    # ── Text diagram ───────────────────────────────────────────────────
    def draw(self) -> str:
        """Return an ASCII text diagram of the circuit."""
        lines: List[List[str]] = [[] for _ in range(self.num_qubits)]
        for op in self.operations:
            width = len(op.name) + 2  # padding inside box
            for q in range(self.num_qubits):
                if q in op.targets:
                    label = op.name.center(width)
                    lines[q].append(f"[{label}]")
                else:
                    lines[q].append("─" * (width + 2))
        rows: List[str] = []
        for q in range(self.num_qubits):
            prefix = f"q{q}: "
            row = "─".join(lines[q]) if lines[q] else ""
            rows.append(prefix + row)
        return "\n".join(rows)

    # ── Internal helpers ───────────────────────────────────────────────
    def _validate_qubit(self, index: int) -> None:
        if not 0 <= index < self.num_qubits:
            raise IndexError(
                f"Qubit index {index} out of range for {self.num_qubits}-qubit circuit."
            )

    def __repr__(self) -> str:
        return (
            f"QuantumCircuit(num_qubits={self.num_qubits}, "
            f"ops={len(self.operations)})"
        )

    def __str__(self) -> str:
        return self.draw()
