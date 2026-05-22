# ⚛️ QuantumSim

**A quantum mechanics simulator that models quantum systems, implements quantum gates, and visualises quantum states.**

Built for physics students and researchers who want to understand quantum computing fundamentals through hands-on simulation — without needing access to real quantum hardware.

---

## ✨ Features

- **Qubit State Vectors** — Full complex-amplitude representation with automatic normalisation
- **Comprehensive Gate Library** — Pauli (X, Y, Z), Hadamard, Phase (S, T), Rotation (Rx, Ry, Rz), CNOT, SWAP, CZ, Toffoli
- **Circuit Builder** — Fluent API for constructing multi-qubit quantum circuits with ASCII diagram output
- **State-Vector Simulator** — Exact unitary simulation with multi-shot measurement sampling
- **Entanglement Detection** — Automatic purity-based entanglement checking via reduced density matrices
- **Bloch Sphere Visualisation** — Interactive 3D plots of single-qubit states on the Bloch sphere
- **Probability Histograms** — Publication-quality bar charts of measurement outcome distributions
- **Quantum Algorithms** — Ready-to-run implementations of Deutsch-Jozsa, Grover's search, quantum teleportation, and Bell state preparation

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/mohitkumar/quantumsim.git
cd quantumsim

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Requirements

- Python ≥ 3.9
- NumPy ≥ 1.21
- Matplotlib ≥ 3.5

---

## 🚀 Quick Start

### Creating and Measuring a Bell State

```python
from quantumsim import QuantumCircuit, Simulator

# Build a Bell state circuit: |Φ⁺⟩ = (|00⟩ + |11⟩) / √2
qc = QuantumCircuit(2)
qc.h(0)          # Hadamard on qubit 0
qc.cx(0, 1)      # CNOT: control=0, target=1
qc.measure()

# Simulate
sim = Simulator()
counts = sim.run(qc, shots=1024)
print(counts)  # {'00': ~512, '11': ~512}
```

### Inspecting the State Vector

```python
sv = sim.statevector(qc)
print(sv)  # [0.707+0j, 0, 0, 0.707+0j]

# Check entanglement
print(sim.is_entangled(qc))  # True
```

### Using the Qubit Class Directly

```python
from quantumsim import Qubit

q = Qubit.plus()               # |+⟩ state
print(q.probabilities())       # (0.5, 0.5)
print(q.bloch_coordinates())   # (1.0, 0.0, 0.0)
result = q.measure()           # Collapses to |0⟩ or |1⟩
```

---

## 📊 Visualisation

### Probability Distribution

```python
from quantumsim.visualization import plot_probabilities

fig = plot_probabilities(counts, title="Bell State Measurements")
fig.savefig("bell_probs.png", dpi=150)
```

### Bloch Sphere

```python
from quantumsim.visualization import plot_bloch_sphere
from quantumsim import Qubit

q = Qubit.plus()
coords = [q.bloch_coordinates()]
fig = plot_bloch_sphere(coords, labels=["|+⟩"])
fig.savefig("bloch.png", dpi=150)
```

### Circuit Diagram

```python
qc = QuantumCircuit(3)
qc.h(0).cx(0, 1).cx(1, 2)
print(qc.draw())
# q0: [ H ]─[CX ]───────
# q1: ──────[CX ]─[CX ]─
# q2: ────────────[CX ]─
```

---

## 🧪 Quantum Algorithms

### Grover's Search

```python
from quantumsim.algorithms import grovers_search
from quantumsim import Simulator

circuit = grovers_search(target=3, num_qubits=2)
sim = Simulator()
counts = sim.run(circuit, shots=1024)
print(counts)  # |11⟩ dominates with ~100% probability
```

### Deutsch-Jozsa

```python
from quantumsim.algorithms import deutsch_jozsa

# Test a balanced oracle
circuit = deutsch_jozsa(oracle_type="balanced")
counts = Simulator().run(circuit, shots=100)
print(counts)  # {'1': 100} → balanced function detected
```

### Quantum Teleportation

```python
from quantumsim.algorithms import quantum_teleportation

circuit = quantum_teleportation()
print(circuit.draw())
```

---

## 📖 Theory

### Quantum Computing Basics

**Qubits** are the fundamental unit of quantum information. Unlike classical bits (0 or 1), a qubit exists in a *superposition*:

$$|ψ⟩ = α|0⟩ + β|1⟩$$

where α and β are complex amplitudes satisfying |α|² + |β|² = 1.

**Quantum gates** are unitary transformations that manipulate qubit states. Key gates include:

| Gate | Matrix | Effect |
|------|--------|--------|
| X | `[[0,1],[1,0]]` | Bit flip (quantum NOT) |
| H | `[[1,1],[1,-1]]/√2` | Creates superposition |
| CNOT | 4×4 matrix | Entangles two qubits |

**Measurement** collapses the quantum state — the probability of observing |0⟩ is |α|² and |1⟩ is |β|².

**Entanglement** occurs when two qubits share correlations that cannot be described independently. The Bell state |Φ⁺⟩ = (|00⟩ + |11⟩)/√2 is the canonical example.

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

---

## 📁 Project Structure

```
QuantumSim/
├── quantumsim/
│   ├── __init__.py          # Package init
│   ├── qubit.py             # Qubit state representation
│   ├── gates.py             # Quantum gate matrices
│   ├── circuit.py           # Circuit builder
│   ├── simulator.py         # State-vector simulator
│   ├── visualization.py     # Plotting utilities
│   └── algorithms.py        # Quantum algorithms
├── examples/
│   ├── bell_states.py       # Bell state demo
│   ├── grovers_search.py    # Grover's algorithm
│   └── quantum_teleportation.py
├── tests/
│   ├── test_qubit.py
│   └── test_circuit.py
├── requirements.txt
├── setup.py
├── LICENSE
└── README.md
```

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m "Add amazing feature"`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Guidelines

- Add unit tests for new features
- Follow PEP 8 style conventions
- Include type hints and docstrings
- Keep quantum mechanics implementations physically accurate

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Built with ❤️ and quantum superposition by <strong>Mohit Kumar</strong>
</p>
