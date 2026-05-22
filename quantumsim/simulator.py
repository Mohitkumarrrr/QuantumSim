"""
State-vector quantum circuit simulator.

Applies gates via tensor-product expansion and performs projective
measurements to produce classical bit-string outcomes.
"""

from __future__ import annotations

from collections import Counter
from typing import Dict, List, Optional, Tuple

import numpy as np
from numpy.typing import NDArray

from quantumsim.circuit import QuantumCircuit, GateOp


class Simulator:
    """Execute a QuantumCircuit and return measurement results.

    The simulator maintains a full 2ⁿ state vector and applies gate
    operations as unitary matrix multiplications.
    """

    def __init__(self) -> None:
        self._state: Optional[NDArray[np.complexfloating]] = None
        self._num_qubits: int = 0

    # ── Public API ─────────────────────────────────────────────────────
    def run(
        self,
        circuit: QuantumCircuit,
        shots: int = 1024,
    ) -> Dict[str, int]:
        """Simulate the circuit and return measurement counts.

        Args:
            circuit: The quantum circuit to execute.
            shots: Number of measurement repetitions.

        Returns:
            Dictionary mapping bit-string outcomes to their counts.
        """
        counts: Counter[str] = Counter()
        for _ in range(shots):
            self._initialise_state(circuit.num_qubits)
            self._apply_operations(circuit.operations)
            outcome = self._measure(circuit.measured_qubits)
            counts[outcome] += 1
        return dict(sorted(counts.items()))

    def statevector(self, circuit: QuantumCircuit) -> NDArray[np.complexfloating]:
        """Return the final state vector *without* measurement collapse.

        Args:
            circuit: The quantum circuit to execute.

        Returns:
            Complex state vector of length 2ⁿ.
        """
        self._initialise_state(circuit.num_qubits)
        self._apply_operations(circuit.operations)
        return self._state.copy()  # type: ignore[union-attr]

    def probabilities(self, circuit: QuantumCircuit) -> NDArray[np.floating]:
        """Return the probability distribution over computational-basis states.

        Args:
            circuit: The quantum circuit to execute.

        Returns:
            Real array of probabilities, length 2ⁿ.
        """
        sv = self.statevector(circuit)
        return np.abs(sv) ** 2

    def is_entangled(self, circuit: QuantumCircuit) -> bool:
        """Heuristic check: return *True* if the output state is entangled.

        Uses the reduced density matrix of the first qubit.  If its purity
        Tr(ρ²) < 1 − ε the state is entangled.
        """
        if circuit.num_qubits < 2:
            return False
        sv = self.statevector(circuit)
        n = circuit.num_qubits
        psi = sv.reshape([2] * n)
        # Trace out everything except qubit-0
        axes = list(range(1, n))
        rho = np.tensordot(psi, psi.conj(), axes=(axes, axes))
        purity = float(np.real(np.trace(rho @ rho)))
        return purity < 1.0 - 1e-6

    # ── Internal helpers ───────────────────────────────────────────────
    def _initialise_state(self, num_qubits: int) -> None:
        """Set the state vector to |00…0⟩."""
        self._num_qubits = num_qubits
        self._state = np.zeros(2**num_qubits, dtype=complex)
        self._state[0] = 1.0 + 0j

    def _apply_operations(self, operations: List[GateOp]) -> None:
        """Apply each gate operation to the state vector."""
        for op in operations:
            full_matrix = self._expand_gate(op)
            self._state = full_matrix @ self._state  # type: ignore[union-attr]

    def _expand_gate(self, op: GateOp) -> NDArray[np.complexfloating]:
        """Expand a gate into the full 2ⁿ × 2ⁿ Hilbert space.

        For a single-qubit gate, tensor-products with identity matrices
        are used.  For two-qubit gates, qubit re-ordering is handled via
        permutation matrices when the targets are not adjacent or are
        in non-standard order.
        """
        n = self._num_qubits
        gate = op.matrix
        targets = op.targets

        if len(targets) == 1:
            return self._single_qubit_expand(gate, targets[0], n)
        elif len(targets) == 2:
            return self._two_qubit_expand(gate, targets[0], targets[1], n)
        else:
            return self._general_expand(gate, targets, n)

    @staticmethod
    def _single_qubit_expand(
        gate: NDArray[np.complexfloating], target: int, n: int
    ) -> NDArray[np.complexfloating]:
        """Expand a single-qubit gate using Kronecker products."""
        ops = [np.eye(2, dtype=complex)] * n
        ops[target] = gate
        result = ops[0]
        for m in ops[1:]:
            result = np.kron(result, m)
        return result

    @staticmethod
    def _two_qubit_expand(
        gate: NDArray[np.complexfloating], q0: int, q1: int, n: int
    ) -> NDArray[np.complexfloating]:
        """Expand a two-qubit gate, handling arbitrary qubit indices."""
        dim = 2**n

        # Build the full-space matrix element-by-element
        full = np.zeros((dim, dim), dtype=complex)
        for i in range(dim):
            for j in range(dim):
                # Extract the 2-bit sub-indices for the target qubits
                i_q0 = (i >> (n - 1 - q0)) & 1
                i_q1 = (i >> (n - 1 - q1)) & 1
                j_q0 = (j >> (n - 1 - q0)) & 1
                j_q1 = (j >> (n - 1 - q1)) & 1

                # Remaining bits must match (identity on other qubits)
                i_rest = i
                j_rest = j
                for q in (q0, q1):
                    bit_mask = ~(1 << (n - 1 - q))
                    i_rest = i_rest & bit_mask
                    j_rest = j_rest & bit_mask
                if i_rest != j_rest:
                    continue

                sub_i = (i_q0 << 1) | i_q1
                sub_j = (j_q0 << 1) | j_q1
                full[i, j] = gate[sub_i, sub_j]
        return full

    @staticmethod
    def _general_expand(
        gate: NDArray[np.complexfloating],
        targets: Tuple[int, ...],
        n: int,
    ) -> NDArray[np.complexfloating]:
        """Expand a gate on an arbitrary number of target qubits."""
        k = len(targets)
        dim = 2**n
        full = np.zeros((dim, dim), dtype=complex)
        for i in range(dim):
            for j in range(dim):
                # Check non-target bits match
                mask_bits = set(range(n)) - set(targets)
                match = all(
                    ((i >> (n - 1 - b)) & 1) == ((j >> (n - 1 - b)) & 1)
                    for b in mask_bits
                )
                if not match:
                    continue
                sub_i = 0
                sub_j = 0
                for idx, t in enumerate(targets):
                    sub_i |= (((i >> (n - 1 - t)) & 1) << (k - 1 - idx))
                    sub_j |= (((j >> (n - 1 - t)) & 1) << (k - 1 - idx))
                full[i, j] = gate[sub_i, sub_j]
        return full

    def _measure(self, qubits: List[int]) -> str:
        """Perform projective measurement on the specified qubits."""
        probs = np.abs(self._state) ** 2  # type: ignore[union-attr]
        probs = probs / probs.sum()  # normalise to avoid fp drift
        dim = len(probs)
        outcome_index = np.random.choice(dim, p=probs)
        n = self._num_qubits
        full_bits = format(outcome_index, f"0{n}b")
        return "".join(full_bits[q] for q in qubits)
