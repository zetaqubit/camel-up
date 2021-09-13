"""Representation of the game state.

Conventions:
  - camels range in [1, n_camels]
  - tracks range in [1, n_camels]
  - valid spaces range in [1, n_spaces]
  - special space 0 is starting zone
  - special space n_spaces+1 in finish zone

"""
import numpy as np

class Tracks:
  def __init__(self, n_spaces=16, n_camels=5):
    self.n_spaces = n_spaces
    self.n_camels = n_camels

    # minus_one
    # plus_one
    # track_5
    # track_4
    # ...
    # track_1
    self.features = [
        'minus_one',
        'plus_one',
    ] + [
        f'track_{i}' for i in range(n_camels, 0, -1)
    ]

    # state is [features, position].
    # Special positions:
    #  - state[:, 0] is before the track (camels that haven't moved yet)
    #  - state[:, -1] is after the track (camels that won)
    self.state = np.zeros((len(self.features), (n_spaces + 2)))

    # state[:, 0] is special:
    #  - All camels start here at the beginning of the game.
    #  - Camels don't obey the stacked move behavior here.
    for i in range(1, n_camels + 1):
      self.state[-i, 0] = i

  def is_end_of_game(self):
    return np.any(self.state[-self.n_camels:, -1] > 0)

  def is_legal_state(self):
    # Check plus/minus tiles.
    # Rule #1: tiles must be in the main track (not before/after).
    if np.any(self.state[:2, 0]):
      return False, 'Plus/Minus in starting zone.'
    if np.any(self.state[:2, -1]):
      return False, 'Plus/Minus in finish zone.'

    # Rule #2: each tile may have only either plus or minus.
    mask_0 = (self.state[0, :] != 0)
    mask_1 = (self.state[1, :] != 0)
    if np.any(mask_0 & mask_1):
      return False, 'Same tile has both plus and minus.'

    # Rule #3: adjacent tiles cannot have plus/minus.
    mask_01 = mask_0 | mask_1
    for i in range(len(mask_01) - 1):
      if mask_01[i] and mask_01[i+1]:
        return False, 'Adjacent tiles have plus/minus.'

    # Check camels.
    # Rule #1: each camel must be in exact one position.
    for camel in range(1, self.n_camels + 1):
      camel_mask = self.state[-self.n_camels:, :] == camel
      n_camel_pos = np.sum(camel_mask)
      if n_camel_pos != 1:
        return False, f'Camel {camel} is in {n_camel_pos} positions.'

    # Rule #2: camels must be stacked from the bottom track upwards.
    for track in range(1, self.n_camels):
      track_mask = self.state[-track, 1:] != 0
      above_tracks_mask = np.sum(self.state[2:-track, 1:], axis=0) != 0
      if np.any((1 - track_mask) & above_tracks_mask):
        return False, 'Camels not stacked from bottom track upwards.'

    # Rule #3: no camel can be on a tile with plus/minus.
    camels_mask = self.state[-self.n_camels:, :] != 0
    if np.any(camels_mask & mask_01):
      return False, 'Camels cannot be on a tile with plus/minus.'

    return True, 'Legal'

  def print(self):
    print(self.state)


class Board:
  """Representation of the board, including the tracks and player states.
  """
  def __init__(self, n_spaces=16, n_camels=5, n_players=2):
    self.n_spaces = n_spaces
    self.n_camels = n_camels
    self.n_players = n_players

    self.tracks = Tracks(n_spaces, n_camels)


  def print(self):
    self.tracks.print()

