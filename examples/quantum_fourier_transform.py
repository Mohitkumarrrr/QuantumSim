#!/usr/bin/env python3
"""Quantum Fourier Transform (QFT) implementation."""
import numpy as np
from quantumsim.circuit import QuantumCircuit
from quantumsim.simulator import Simulator

def qft_circuit(n_qubits):
    circuit = QuantumCircuit(n_qubits)
    for i in range(n_qubits):
        circuit.add_gate('H', i)
        for j in range(i+1, n_qubits):
            angle = np.pi / (2 ** (j - i))
            circuit.add_gate('CP', [i, j], params={'theta': angle})
    return circuit

if __name__ == '__main__':
    qc = qft_circuit(3)
    sim = Simulator()
    result = sim.run(qc, shots=1024)
    print('QFT Results:', result)
