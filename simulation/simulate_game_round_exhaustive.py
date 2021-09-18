import copy
import functools

from absl import app
from absl import flags
from absl import logging
import json
import numpy as np

from simulation import board
from simulation import game_round

FLAGS = flags.FLAGS

flags.DEFINE_integer('n_spaces', 16, 'Number of spaces in the race track.')
flags.DEFINE_integer('n_camels', 5, 'Number of camels in the race track.')
flags.DEFINE_integer('n_players', 2, 'Number of players in the game.')
flags.DEFINE_string('initial_state', '',
    'Initial state of the board, serialized as json. Supported key-values: \n'
    ' a) "camel_states": [[camel_id, position], ...]. Example: [[1, 10], [2, 11]] \n'
    ' b) "camels_not_moved": [camel_id, ...]. Example: [2, 4, 5] \n')


def round_end_probs(b):

  def tree_search(board_state):
    n_first_place = np.zeros((b.n_camels + 1,))
    n_second_place = np.zeros((b.n_camels + 1,))

    if board_state.tracks.is_end_of_game() or board_state.round.is_end_of_round():
      standings = board_state.tracks.camel_standings()
      n_first_place[standings[0]] = 1
      n_second_place[standings[1]] = 1
      return n_first_place, n_second_place

    all_moves = board_state.round.get_all_camel_moves()
    for move in all_moves:
      new_b = copy.deepcopy(board_state)
      new_b.apply_move(move)
      first, second = tree_search(new_b)
      n_first_place += first
      n_second_place += second

    return n_first_place, n_second_place

  n_1st, n_2nd = tree_search(b)
  assert sum(n_1st) == sum(n_2nd)
  n_simulations = sum(n_1st)

  print(f'Exhaustive search through {n_simulations} simulations.')
  print(f'First place percentages: {n_1st / n_simulations}')
  print(f'Second place percentages: {n_2nd / n_simulations}')
  return 

def main(_):
  b = board.Board(FLAGS.n_spaces, FLAGS.n_camels, FLAGS.n_players)

  # Apply initial states if provided.
  init_state = json.loads(FLAGS.initial_state)

  if 'camel_states' in init_state:
    camel_states = init_state['camel_states']
    camel_states = [board.CamelState(i, p) for i, p in camel_states]
    for camel_state in camel_states:
      b.tracks.apply_move(camel_state)
  if 'camels_not_moved' in init_state:
    camels_not_moved = init_state['camels_not_moved']
    camels_not_moved = list(map(int, camels_not_moved))
    b.round.camels_not_moved = camels_not_moved

  print(
      f'Running with n_spaces={FLAGS.n_spaces}, '
      f'n_camels={FLAGS.n_camels}, '
      f'n_players={FLAGS.n_players}.')
  b.print()

  print('End of round probabilities: ')
  print(round_end_probs(b))
  


if __name__ == '__main__':
  app.run(main)
