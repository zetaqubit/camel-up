"""Tests for simulation.game_round."""

import unittest

import numpy as np
from parameterized import parameterized

from simulation import board
from simulation import game_round


class GameRoundTest(unittest.TestCase):
  @parameterized.expand([
    ([(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3)], 2, 3),
  ])
  def test_get_all_camel_moves(self, expected_all_moves, n_camels, n_max_roll):
    expected_all_moves = [moves.CamelMove(c, m) for c, m in expected_all_moves]
    r = game_round.GameRound(n_camels=n_camels, n_max_roll=n_max_roll)
    self.assertEqual(r.get_all_camel_moves(), expected_all_moves)

  @parameterized.expand([
    (2, 3),
    (3, 3),
    (4, 4),
    (5, 4),
  ])
  def test_move_camel_random(self, n_camels, n_max_roll):
    r = game_round.GameRound(n_camels=n_camels, n_max_roll=n_max_roll)
    picked = []
    for i in range(n_camels):
      move = r.move_camel_random()
      picked.append(move.camel)
      self.assertTrue(1 <= move.spaces <= n_max_roll)
      self.assertEqual(len(r.camels_not_moved), n_camels - i - 1)
    self.assertEqual(sorted(picked), list(range(1, n_camels+1)))

  @parameterized.expand([
    (2, [2, 1]),
    (3, [3, 1, 2]),
    (4, [1, 2, 3, 4]),
    (5, [3, 1, 4, 5, 2]),
  ])
  def test_move_camel_valid(self, n_camels, camels_to_move):
    r = game_round.GameRound(n_camels=n_camels)
    picked = []
    for camel in camels_to_move:
      move = r.move_camel(camel)
      self.assertEqual(move.camel, camel)
      self.assertTrue(1 <= move.spaces <= 3)
    self.assertTrue(r.is_end_of_round())

  @parameterized.expand([
    ([1, 2, 3, 4, 5], 0),
    ([1, 2, 3, 4, 5], 6),
  ])
  def test_move_camel_invalid(self, camels_not_moved, camel):
    r = game_round.GameRound()
    r.camels_not_moved = camels_not_moved
    try:
      r.move_camel(camel)
      self.fail()
    except ValueError:
      pass

  @parameterized.expand([
    (2,), (3,), (4,), (5,),
  ])
  def test_is_end_of_round(self, n_camels):
    r = game_round.GameRound(n_camels=n_camels)
    for i in range(n_camels):
      self.assertFalse(r.is_end_of_round())
      r.move_camel_random()
    self.assertTrue(r.is_end_of_round())

