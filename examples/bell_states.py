"""
Bell States — Creating and measuring all four Bell states.

Bell states are maximally entangled two-qubit states that form the
foundation of quantum information protocols such as teleportation
and superdense coding.
"""

from quantumsim.algorithms import bell_state
from quantumsim.simulator import Simulator
from quantumsim.visualization import plot_probabilities

BELL_NAMES = ["Φ⁺", "Φ⁻", "Ψ⁺", "Ψ⁻"]


def main() -> None:
    """Create, simulate, and display all four Bell states."""
    sim = Simulator()

    for variant in range(4):
        circuit = bell_state(variant)
        print(f"\n{'='*40}")
        print(f"  Bell State |{BELL_NAMES[variant]}⟩  (variant={variant})")
        print(f"{'='*40}")
        print(circuit.draw())

        counts = sim.run(circuit, shots=2048)
        total = sum(counts.values())
        print("\nMeasurement results:")
        for outcome, count in counts.items():
            prob = count / total
            print(f"  |{outcome}⟩ : {count:>5}  ({prob:.3f})")

        # Check entanglement
        is_ent = sim.is_entangled(circuit)
        print(f"\n  Entangled: {is_ent}")

    # Visualise the last Bell state
    fig = plot_probabilities(counts, title=f"Bell State |{BELL_NAMES[3]}⟩")
    fig.savefig("bell_state_distribution.png", dpi=150)
    print("\nSaved plot to bell_state_distribution.png")


if __name__ == "__main__":
    main()
