"""
QuantumSim — A quantum mechanics simulator with visualization.

Provides tools for building quantum circuits, simulating quantum gates,
and visualizing quantum states on Bloch spheres and probability histograms.
"""

__version__ = "1.0.0"
__author__ = "Mohit Kumar"

from quantumsim.qubit import Qubit
from quantumsim.gates import Gates
from quantumsim.circuit import QuantumCircuit
from quantumsim.simulator import Simulator

__all__ = ["Qubit", "Gates", "QuantumCircuit", "Simulator"]
