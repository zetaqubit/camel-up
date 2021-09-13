from absl import app
from absl import flags
from absl import logging
import numpy as np

from simulation import board
from simulation import game_round

FLAGS = flags.FLAGS

flags.DEFINE_integer('n_spaces', 16, 'Number of spaces in the race track.')
flags.DEFINE_integer('n_camels', 5, 'Number of camels in the race track.')
flags.DEFINE_integer('n_players', 2, 'Number of players in the game.')


def main(_):
  b = board.Board(FLAGS.n_spaces, FLAGS.n_camels, FLAGS.n_players)

  print(
      f'Running with n_spaces={FLAGS.n_spaces}, '
      f'n_camels={FLAGS.n_camels}, '
      f'n_players={FLAGS.n_players}.')



if __name__ == '__main__':
  app.run(main)
