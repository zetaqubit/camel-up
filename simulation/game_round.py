import numpy as np

from simulation import board


class GameRound:
  def __init__(self, track_state, n_max_roll=3):
    self.track_state = track_state
    self.n_camels = track_state.n_camels
    self.n_max_roll = n_max_roll
    self.start_new_round()

  def get_camel_move(self, camel_id=None, roll=None):
    if camel_id is None:
      camel_id = np.random.choice(self.camels_not_moved)
    camel = self.track_state.find_camel(camel_id)
    if roll is None:
      roll = np.random.randint(1, self.n_max_roll+1)
    return board.CamelState(camel_id, camel.position + roll)

  def get_all_camel_moves(self):
    all_moves = []
    for camel_id in self.camels_not_moved:
      camel = self.track_state.find_camel(camel_id)
      for roll in range(1, self.n_max_roll+1):
        all_moves.append(board.CamelState(camel_id, camel.position + roll))
    return all_moves

  def apply_move(self, move):
    """Moves the specified camel, throwing exception if invalid camel."""
    self.camels_not_moved.remove(move.camel_id)

  def is_end_of_round(self):
    return len(self.camels_not_moved) == 0

  def start_new_round(self):
    self.camels_not_moved = list(range(1, self.n_camels+1))

