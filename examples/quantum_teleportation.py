"""
Quantum Teleportation — Transferring a qubit state using entanglement.

Demonstrates the quantum teleportation protocol where Alice sends the
state of qubit q0 to Bob's qubit q2 using a shared Bell pair and
classical communication (simulated via controlled gates).
"""

from quantumsim.algorithms import quantum_teleportation
from quantumsim.simulator import Simulator
from quantumsim.visualization import plot_probabilities

import numpy as np


def main() -> None:
    """Run the quantum teleportation protocol and display results."""
    sim = Simulator()

    print("╔══════════════════════════════════════════╗")
    print("║      Quantum Teleportation Protocol      ║")
    print("╚══════════════════════════════════════════╝")

    circuit = quantum_teleportation()

    print("\nCircuit diagram:")
    print(circuit.draw())

    # Get the statevector
    sv = sim.statevector(circuit)
    print("\nFinal state vector (amplitudes):")
    n = circuit.num_qubits
    for i, amp in enumerate(sv):
        if abs(amp) > 1e-10:
            label = format(i, f"0{n}b")
            print(f"  |{label}⟩ : {amp:.4f}  (prob = {abs(amp)**2:.4f})")

    # Run measurements
    counts = sim.run(circuit, shots=4096)
    total = sum(counts.values())

    print("\nMeasurement results (4096 shots):")
    for outcome, count in counts.items():
        prob = count / total
        print(f"  |{outcome}⟩ : {count:>5}  ({prob:.3f})")

    print("\nNote: Bob's qubit (q2) receives the teleported state.")
    print("The measurement of q2 should match the statistics of the")
    print("original state |+⟩ (equal probability of 0 and 1).")

    fig = plot_probabilities(counts, title="Quantum Teleportation Results")
    fig.savefig("teleportation_results.png", dpi=150)
    print("\nSaved plot to teleportation_results.png")


if __name__ == "__main__":
    main()
