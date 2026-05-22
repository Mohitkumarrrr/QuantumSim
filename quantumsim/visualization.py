"""
Visualization utilities for quantum states and circuits.

Provides Bloch sphere plots, probability histograms, state-evolution
charts, and circuit diagrams — all built on matplotlib.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (enables 3-D projection)
from numpy.typing import NDArray


def plot_probabilities(
    counts: Dict[str, int],
    title: str = "Measurement Outcomes",
    figsize: Tuple[int, int] = (10, 5),
) -> Figure:
    """Bar chart of measurement outcome probabilities.

    Args:
        counts: Mapping of bit-string → count.
        title: Plot title.
        figsize: Figure dimensions.

    Returns:
        The matplotlib Figure.
    """
    total = sum(counts.values())
    labels = list(counts.keys())
    probs = [v / total for v in counts.values()]

    fig, ax = plt.subplots(figsize=figsize)
    colours = plt.cm.viridis(np.linspace(0.25, 0.85, len(labels)))  # type: ignore[attr-defined]
    ax.bar(labels, probs, color=colours, edgecolor="black", linewidth=0.6)
    ax.set_xlabel("Outcome", fontsize=12)
    ax.set_ylabel("Probability", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_ylim(0, 1.05)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    return fig


def plot_bloch_sphere(
    coordinates: List[Tuple[float, float, float]],
    labels: Optional[List[str]] = None,
    title: str = "Bloch Sphere",
    figsize: Tuple[int, int] = (8, 8),
) -> Figure:
    """Plot one or more qubit states on the Bloch sphere.

    Args:
        coordinates: List of (x, y, z) Bloch vectors.
        labels: Optional label for each point.
        title: Plot title.
        figsize: Figure dimensions.

    Returns:
        The matplotlib Figure.
    """
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection="3d")

    # Draw wireframe sphere
    u = np.linspace(0, 2 * np.pi, 40)
    v = np.linspace(0, np.pi, 30)
    xs = np.outer(np.cos(u), np.sin(v))
    ys = np.outer(np.sin(u), np.sin(v))
    zs = np.outer(np.ones_like(u), np.cos(v))
    ax.plot_wireframe(xs, ys, zs, color="lightgrey", alpha=0.3, linewidth=0.4)

    # Axes
    ax.plot([-1.2, 1.2], [0, 0], [0, 0], color="grey", linewidth=0.5)
    ax.plot([0, 0], [-1.2, 1.2], [0, 0], color="grey", linewidth=0.5)
    ax.plot([0, 0], [0, 0], [-1.2, 1.2], color="grey", linewidth=0.5)
    ax.text(1.3, 0, 0, "X", fontsize=10)
    ax.text(0, 1.3, 0, "Y", fontsize=10)
    ax.text(0, 0, 1.3, "|0⟩", fontsize=11, fontweight="bold")
    ax.text(0, 0, -1.35, "|1⟩", fontsize=11, fontweight="bold")

    # Plot state vectors
    colours = plt.cm.plasma(np.linspace(0.2, 0.8, len(coordinates)))  # type: ignore[attr-defined]
    for idx, (x, y, z) in enumerate(coordinates):
        ax.quiver(0, 0, 0, x, y, z, color=colours[idx], arrow_length_ratio=0.08, linewidth=2)
        lbl = labels[idx] if labels else f"q{idx}"
        ax.text(x * 1.1, y * 1.1, z * 1.1, lbl, fontsize=9)

    ax.set_xlim([-1.4, 1.4])
    ax.set_ylim([-1.4, 1.4])
    ax.set_zlim([-1.4, 1.4])
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_box_aspect([1, 1, 1])
    ax.axis("off")
    plt.tight_layout()
    return fig


def plot_state_evolution(
    states: List[NDArray[np.complexfloating]],
    step_labels: Optional[List[str]] = None,
    title: str = "State Evolution",
    figsize: Tuple[int, int] = (12, 5),
) -> Figure:
    """Heatmap of probability amplitudes across circuit steps.

    Args:
        states: List of state vectors after each gate operation.
        step_labels: Label for each step (defaults to integer indices).
        title: Plot title.
        figsize: Figure dimensions.

    Returns:
        The matplotlib Figure.
    """
    prob_matrix = np.array([np.abs(s) ** 2 for s in states]).T
    n_basis = prob_matrix.shape[0]
    n_steps = prob_matrix.shape[1]
    basis_labels = [format(i, f"0{int(np.log2(n_basis))}b") for i in range(n_basis)]

    if step_labels is None:
        step_labels = [str(i) for i in range(n_steps)]

    fig, ax = plt.subplots(figsize=figsize)
    cax = ax.imshow(prob_matrix, aspect="auto", cmap="inferno", vmin=0, vmax=1)
    fig.colorbar(cax, ax=ax, label="Probability")
    ax.set_xticks(range(n_steps))
    ax.set_xticklabels(step_labels, rotation=45, ha="right")
    ax.set_yticks(range(n_basis))
    ax.set_yticklabels(basis_labels)
    ax.set_xlabel("Circuit Step", fontsize=12)
    ax.set_ylabel("Basis State", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight="bold")
    plt.tight_layout()
    return fig


def plot_circuit(
    circuit_text: str,
    title: str = "Quantum Circuit",
    figsize: Tuple[int, int] = (14, 4),
) -> Figure:
    """Render a text circuit diagram on a matplotlib figure.

    Args:
        circuit_text: The ASCII circuit string from ``QuantumCircuit.draw()``.
        title: Plot title.
        figsize: Figure dimensions.

    Returns:
        The matplotlib Figure.
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.text(
        0.02, 0.95,
        circuit_text,
        transform=ax.transAxes,
        fontsize=11,
        fontfamily="monospace",
        verticalalignment="top",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#f0f0f0", edgecolor="grey"),
    )
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.axis("off")
    plt.tight_layout()
    return fig
