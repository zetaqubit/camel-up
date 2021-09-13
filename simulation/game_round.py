import numpy as np

from simulation import moves


class GameRound:
  def __init__(self, n_camels=5, n_players=2, n_max_roll=3):
    self.n_players = n_players
    self.n_max_roll = n_max_roll
    self.camels_not_moved = list(range(1, n_camels+1))

  def move_camel_random(self):
    i = np.random.randint(len(self.camels_not_moved))
    camel = self.camels_not_moved.pop(i)
    spaces = np.random.randint(1, self.n_max_roll+1)
    return moves.CamelMove(camel, spaces)

  def move_camel(self, camel):
    """Moves the specified camel, throwing exception if invalid camel."""
    self.camels_not_moved.remove(camel)
    spaces = np.random.randint(1, self.n_max_roll+1)
    return moves.CamelMove(camel, spaces)

  def get_all_camel_moves(self):
    all_moves = []
    for camel in self.camels_not_moved:
      for roll in range(1, self.n_max_roll+1):
        all_moves.append(moves.CamelMove(camel, roll))
    return all_moves

  def is_end_of_round(self):
    return len(self.camels_not_moved) == 0

