"""Unit tests for the Qubit class."""

import numpy as np
import pytest

from quantumsim.qubit import Qubit


class TestQubitCreation:
    """Tests for qubit initialisation."""

    def test_default_is_zero_state(self) -> None:
        q = Qubit()
        assert np.allclose(q.state, [1, 0])

    def test_one_state(self) -> None:
        q = Qubit.one()
        assert np.allclose(q.state, [0, 1])

    def test_plus_state(self) -> None:
        q = Qubit.plus()
        expected = np.array([1, 1]) / np.sqrt(2)
        assert np.allclose(q.state, expected)

    def test_minus_state(self) -> None:
        q = Qubit.minus()
        expected = np.array([1, -1]) / np.sqrt(2)
        assert np.allclose(q.state, expected)

    def test_auto_normalisation(self) -> None:
        q = Qubit(3, 4)
        assert np.isclose(np.linalg.norm(q.state), 1.0)

    def test_zero_vector_raises(self) -> None:
        with pytest.raises(ValueError):
            Qubit(0, 0)


class TestProbabilities:
    """Tests for probability calculations."""

    def test_zero_state_probabilities(self) -> None:
        p0, p1 = Qubit.zero().probabilities()
        assert np.isclose(p0, 1.0)
        assert np.isclose(p1, 0.0)

    def test_plus_state_probabilities(self) -> None:
        p0, p1 = Qubit.plus().probabilities()
        assert np.isclose(p0, 0.5)
        assert np.isclose(p1, 0.5)


class TestMeasurement:
    """Tests for measurement collapse."""

    def test_zero_state_always_measures_zero(self) -> None:
        q = Qubit.zero()
        assert q.measure() == 0

    def test_one_state_always_measures_one(self) -> None:
        q = Qubit.one()
        assert q.measure() == 1

    def test_measurement_collapses_state(self) -> None:
        q = Qubit.plus()
        result = q.measure()
        assert result in (0, 1)
        expected = [1, 0] if result == 0 else [0, 1]
        assert np.allclose(q.state, expected)


class TestBlochCoordinates:
    """Tests for Bloch sphere coordinates."""

    def test_zero_state_is_north_pole(self) -> None:
        x, y, z = Qubit.zero().bloch_coordinates()
        assert np.isclose(z, 1.0)
        assert np.isclose(x, 0.0)

    def test_one_state_is_south_pole(self) -> None:
        x, y, z = Qubit.one().bloch_coordinates()
        assert np.isclose(z, -1.0)

    def test_plus_state_on_x_axis(self) -> None:
        x, y, z = Qubit.plus().bloch_coordinates()
        assert np.isclose(x, 1.0)
        assert np.isclose(z, 0.0, atol=1e-10)
