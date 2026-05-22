"""
Grover's Search Algorithm — Finding a marked item in an unsorted database.

Demonstrates quadratic speed-up: for N=4 items, a single Grover iteration
finds the target with high probability (~100% for 2 qubits).
"""

from quantumsim.algorithms import grovers_search
from quantumsim.simulator import Simulator
from quantumsim.visualization import plot_probabilities


def main() -> None:
    """Run Grover's search for each possible 2-qubit target."""
    sim = Simulator()

    print("╔════════════════════════════════════════════╗")
    print("║    Grover's Search Algorithm (2 qubits)    ║")
    print("╚════════════════════════════════════════════╝")

    for target in range(4):
        circuit = grovers_search(target=target, num_qubits=2)

        print(f"\n── Target: |{format(target, '02b')}⟩ (decimal {target}) ──")
        print(circuit.draw())

        counts = sim.run(circuit, shots=2048)
        total = sum(counts.values())

        print("Results:")
        for outcome, count in counts.items():
            prob = count / total
            marker = " ← TARGET" if outcome == format(target, "02b") else ""
            print(f"  |{outcome}⟩ : {count:>5}  ({prob:.3f}){marker}")

        # Verify correctness
        sv = sim.statevector(circuit)
        probs = abs(sv) ** 2
        target_prob = probs[target]
        print(f"  Theoretical target probability: {target_prob:.4f}")

    # Visualise the last run
    fig = plot_probabilities(counts, title="Grover's Search — Target |11⟩")
    fig.savefig("grovers_search.png", dpi=150)
    print("\nSaved plot to grovers_search.png")


if __name__ == "__main__":
    main()
