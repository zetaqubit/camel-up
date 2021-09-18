"""Representation of the game state.

Conventions:
  - camels range in [1, n_camels]
  - tracks range in [1, n_camels]
  - valid spaces range in [1, n_spaces]
  - special space 0 is starting zone
  - special space n_spaces+1 in finish zone

"""
from dataclasses import dataclass

import numpy as np

from simulation import game_round

@dataclass
class CamelState:
  camel_id: int
  position: int

@dataclass
class TileState:
  player_id: int
  plus: bool
  position: None

class TrackState:
  def __init__(self, n_spaces=16, n_camels=5, n_players=2):
    self.n_spaces = n_spaces
    self.n_camels = n_camels

    # List of (camel_id, position), sorted from camel in first position to last,
    # top camel to bottom at each position.
    # Special positions:
    #  0: starting zone
    #  n_spaces+1: ending zone
    self.camel_states = [CamelState(camel_id, 0) for camel_id in range(1, n_camels+1)]

    self.player_tiles = [TileState(player_id, True, None) for player_id in range(n_players)]

  def camel_standings(self):
    return [c.camel_id for c in self.camel_states]

  def apply_move(self, move):
    if self.is_end_of_game():
      raise ValueError('Game has already ended.')

    if isinstance(move, CamelState):
      return self._apply_camel_move(move)

    if isinstance(move, TileState):
      return self._apply_tile_move(move)

  def _apply_camel_move(self, camel_state):
    camel_idx = self._find_camel_idx(camel_state.camel_id)
    start_pos = self.camel_states[camel_idx].position
    if start_pos == 0:
      idxs_moving = [camel_idx]
    else:
      idxs_moving = self._find_camels_to_move(start_pos, camel_idx)

    end_pos = min(camel_state.position, self.n_spaces+1)
    for idx in idxs_moving:
      self.camel_states[idx].position = end_pos + 0.5  # hack to get moving camels to front/top.
    self.camel_states.sort(key=lambda camel: camel.position, reverse=True)
    for i in range(len(self.camel_states)):
      if self.camel_states[i].position == end_pos + 0.5:
        self.camel_states[i].position = end_pos


  def _find_camels_to_move(self, position, end_idx):
    return [i for i, camel in enumerate(self.camel_states)
            if camel.position == position and i <= end_idx]

  def _apply_tile_move(self, tile_state):
    self.player_tiles[tile_state.player_id] = tile_state

  def _find_camel_idx(self, camel_id):
    for idx, camel in enumerate(self.camel_states):
      if camel.camel_id == camel_id:
        return idx

  def find_camel(self, camel_id):
    return self.camel_states[self._find_camel_idx(camel_id)]


  def is_end_of_game(self):
    # Check if first camel is in the ending zone.
    return self.camel_states[0].position > self.n_spaces

  def render_to_array(self):
    a = np.zeros((self.n_camels, self.n_spaces+2), dtype=np.int)
    for i, camel in enumerate(self.camel_states):
      row = self.n_camels - 1
      while a[row, camel.position] != 0:
        row -= 1
      a[row, camel.position] = camel.camel_id

      if i == len(self.camel_states) - 1 or self.camel_states[i+1].position != camel.position:
        a[row:self.n_camels, camel.position] = a[row:self.n_camels, camel.position][::-1]
    return a

  def print(self):
    print(self.render_to_array())


TRACK_START_ROW = 2
TRACK_START_COL = 1

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

  def apply_move(self, move):
    if self.is_end_of_game():
      raise ValueError('Game has already ended.')

    start_rows, start_col = self._find_all_camels_to_move(move.camel_id)
    end_col = start_col + move.spaces
    if end_col >= self.max_col:
      end_col = self.max_col - 1

    end_row = -1
    while self.state[end_row, end_col] != 0:
      end_row -= 1
    end_rows = list(range(end_row, end_row-len(start_rows), -1))

    self.state[end_rows, end_col] = self.state[start_rows, start_col]
    self.state[start_rows, start_col] = 0
    
    

  def _find_all_camels_to_move(self, camel):
    start_row, start_col = self._find_camel(camel)
    if start_col == 0:
      return [start_row], start_col
    rows = []
    while start_row >= TRACK_START_ROW and self.state[start_row, start_col] != 0:
      rows.append(start_row)
      start_row -= 1
    return rows, start_col

  def _find_camel(self, camel):
    idxs = np.argwhere(self.state == camel)
    idxs = [idx for idx in idxs if idx[0] >= TRACK_START_ROW]  # skip non-tracks.
    assert len(idxs) == 1  # camel should only be at 1 place
    return idxs[0]


  @property
  def max_col(self):
    return len(self.state[0])

  @property
  def max_row(self):
    return len(self.state)


  def print(self):
    print(self.state)


class Board:
  """Representation of the board, including the tracks and player states.
  """
  def __init__(self, n_spaces=16, n_camels=5, n_players=2):
    self.n_spaces = n_spaces
    self.n_camels = n_camels
    self.n_players = n_players

    self.tracks = TrackState(n_spaces, n_camels, n_players)
    self.round = game_round.GameRound(self.tracks)

  def step_randomly(self):
    if self.round.is_end_of_round():
      self.round.start_new_round()

    move = self.round.get_camel_move()
    print(move)
    self.apply_move(move)

  def apply_move(self, move):
    self.round.apply_move(move)
    self.tracks.apply_move(move)

  def print(self):
    self.tracks.print()

