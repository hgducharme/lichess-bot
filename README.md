# Purpose

This is a hobbyist's attempt at machine learning by training a chess bot to play on lichess.com. 

This repo houses two things:

1. (Python) An interface to the lichess API
2. (C++) A chess engine that utilizes machine learning

# The Chess Engine

The brains of the chess engine can be broken up into three distinct categories:

1. Board representation - bitboard.
2. Search - Monte Carlo Tree Search (MCTS)
3. Evaluation - deep neural network