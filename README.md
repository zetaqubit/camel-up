# Camel Up

## Background

[Camel Up](https://boardgamegeek.com/boardgame/153938/camel)
is a multi-player board game where each player tries to maximize their income
by correctly betting on the winning camel in a race with 5 camels.

## Simulation
`simulation` implements the rules of the board game. It keeps track of the game
state and maintains the list of legal moves on a turn.

## RL Agent
`agent` contains an RL agent trained to maximize its probability of winning the
game.
