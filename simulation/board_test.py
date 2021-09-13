"""Tests for simulation.board."""

import unittest

import numpy as np
from parameterized import parameterized

from simulation import board


class TracksTest(unittest.TestCase):
  def test_initial_positions(self):
    t = board.Tracks(n_spaces=2, n_camels=3)
    np.testing.assert_array_equal(t.state,
        [
          [0, 0, 0, 0],
          [0, 0, 0, 0],
          [3, 0, 0, 0],
          [2, 0, 0, 0],
          [1, 0, 0, 0],
        ])

  @parameterized.expand([
    ([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [3, 0, 0, 0],
        [2, 0, 0, 0],
        [1, 0, 0, 0],
     ], False),
    ([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 3, 0],
        [0, 0, 2, 0],
        [0, 0, 1, 0],
     ], False),
    # Illegal, but test for it anyways.
    ([
        [0, 0, 0, 1],
        [0, 0, 0, 1],
        [0, 0, 3, 0],
        [0, 0, 2, 0],
        [0, 0, 1, 0],
     ], False),
    ([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [3, 0, 0, 0],
        [2, 0, 0, 0],
        [0, 0, 0, 1],
    ], True),
    ([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [3, 0, 0, 0],
        [2, 0, 0, 2],
        [1, 0, 0, 0],
    ], True),
    ([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [3, 0, 0, 3],
        [2, 0, 0, 0],
        [1, 0, 0, 0],
    ], True),

  ])
  def test_is_game_over(self, state, is_over):
    state = np.array(state)
    shape = state.shape
    t = board.Tracks(n_spaces=shape[1]-2, n_camels=shape[0]-2)
    t.state = state
    self.assertEqual(is_over, t.is_game_over())


  @parameterized.expand([
    ([
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [3, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0],
     ], True),
    ([
        [0, 0, 5, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [3, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0],
     ], True),
    ([
        [0, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 0],
        [3, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0],
     ], True),
    ([
        [1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [3, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0],
     ], False),
    ([
        [0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0],
        [3, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0],
     ], False),
    ([
        [0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0],
        [3, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0],
     ], False),
    ([
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1],
        [3, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0],
     ], False),
    ([
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [3, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0],
     ], False),
    ([
        [0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [3, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0],
     ], False),
    ([
        [0, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [3, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0],
     ], False),
    ([
        [0, 5, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [3, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0],
     ], False),
  ])
  def test_is_legal_state_plus_minus(self, state, is_legal):
    state = np.array(state)
    shape = state.shape
    t = board.Tracks(n_spaces=shape[1]-2, n_camels=shape[0]-2)
    t.state = state
    legal, reason = t.is_legal_state()
    self.assertEqual(is_legal, legal, msg=reason)


  @parameterized.expand([
    # Test camel mask only cares about camel track positions.'
    ([
        [0, 0, 0, 0, 0, 0],
        [0, 0, 2, 0, 0, 0],
        [3, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0],
     ], True),
    ([
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [3, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0],
        [1, 0, 0, 3, 0, 0],
     ], False),
    ([
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [3, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
     ], True),
    ([
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [3, 2, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
     ], False),
    ([
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 3, 0, 0, 0],
        [2, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0],
     ], False),
    ([
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [3, 0, 0, 0, 2, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0],
     ], False),
    ([
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0],
        [0, 0, 1, 3, 0, 0],
     ], False),
    ([
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 3, 0],
     ], True),
    ([
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 2, 1, 3, 0],
     ], True),
    ([
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0],
        [0, 3, 1, 0, 0, 0],
     ], True),
    ([
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1],
        [0, 0, 0, 3, 0, 2],
     ], True),
    ([
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 2],
        [0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 3, 0],
     ], False),
    ([
        [0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [3, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0],
     ], True),
    ([
        [0, 0, 4, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [3, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
     ], False),
  ])
  def test_is_legal_state_camels(self, state, is_legal):
    state = np.array(state)
    shape = state.shape
    t = board.Tracks(n_spaces=shape[1]-2, n_camels=shape[0]-2)
    t.state = state
    legal, reason = t.is_legal_state()
    self.assertEqual(is_legal, legal, msg=reason)
