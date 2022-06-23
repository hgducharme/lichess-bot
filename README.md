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

# Installation

The following will outline how to get the bot up and running utilizing the stockfish engine. First, clone the repo.

```
git clone https://github.com/hgducharme/chessAI.git
cd chessAI/
```

Create and install the python environment

```
cd src/lichess/
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```

Create your settings file

```
cd src/lichess/conf/
cp settings.py.default settings.py
```

Add your API token to `settings.py`

```
API_TOKEN = "xxxxx"
```

Either download stockfish from (the stockfish website)[https://stockfishchess.org/download/] or clone the (stockfish repo)[https://github.com/official-stockfish/Stockfish], rename it to `stockfish`, and place it inside the `engines/` directory

```
mv /path/to/downloaded/stockfish/directory /path/to/chessAI/src/engines/stockfish
```

Update the path to the stockfish binary in `settings.py`. 

```
ENGINE= {
 "path": os.path.join(ENGINE_DIR, "stockfish/stockfish_XX_src/src/stockfish")
  ...
}
```

Make sure everything works!

 ```
 cd chessAI/src/lichess/
 python3 main.py
 ```
