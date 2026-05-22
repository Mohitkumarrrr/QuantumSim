"""Unit tests for QuantumCircuit and Simulator."""

import numpy as np
import pytest

from quantumsim.circuit import QuantumCircuit
from quantumsim.simulator import Simulator


class TestCircuitConstruction:
    """Tests for building circuits."""

    def test_single_qubit_circuit(self) -> None:
        qc = QuantumCircuit(1)
        qc.h(0)
        assert len(qc.operations) == 1
        assert qc.operations[0].name == "H"

    def test_invalid_qubit_index(self) -> None:
        qc = QuantumCircuit(2)
        with pytest.raises(IndexError):
            qc.h(5)

    def test_cnot_same_qubit_raises(self) -> None:
        qc = QuantumCircuit(2)
        with pytest.raises(ValueError):
            qc.cx(0, 0)

    def test_draw_returns_string(self) -> None:
        qc = QuantumCircuit(2)
        qc.h(0).cx(0, 1)
        diagram = qc.draw()
        assert isinstance(diagram, str)
        assert "q0" in diagram


class TestSimulator:
    """Tests for the simulation engine."""

    def test_identity_circuit(self) -> None:
        """Empty circuit preserves |00⟩."""
        qc = QuantumCircuit(2)
        sim = Simulator()
        sv = sim.statevector(qc)
        assert np.isclose(abs(sv[0]) ** 2, 1.0)

    def test_x_gate_flips(self) -> None:
        qc = QuantumCircuit(1)
        qc.x(0)
        sim = Simulator()
        sv = sim.statevector(qc)
        assert np.isclose(abs(sv[1]) ** 2, 1.0)

    def test_hadamard_superposition(self) -> None:
        qc = QuantumCircuit(1)
        qc.h(0)
        sim = Simulator()
        probs = sim.probabilities(qc)
        assert np.allclose(probs, [0.5, 0.5], atol=1e-10)

    def test_bell_state_entangled(self) -> None:
        qc = QuantumCircuit(2)
        qc.h(0).cx(0, 1)
        sim = Simulator()
        assert sim.is_entangled(qc)

    def test_measurement_counts(self) -> None:
        qc = QuantumCircuit(1)
        qc.x(0)
        qc.measure()
        sim = Simulator()
        counts = sim.run(qc, shots=100)
        assert counts == {"1": 100}

    def test_bell_state_correlations(self) -> None:
        """Bell state |Φ⁺⟩ should only produce 00 or 11."""
        qc = QuantumCircuit(2)
        qc.h(0).cx(0, 1).measure()
        sim = Simulator()
        counts = sim.run(qc, shots=500)
        for outcome in counts:
            assert outcome in ("00", "11")
