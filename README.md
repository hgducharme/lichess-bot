# Installation

The following will outline how to get the bot up and running utilizing the stockfish engine. First, clone the repo.

```
git clone https://github.com/hgducharme/lichess-bot.git
cd lichess-bot/
```

Create and install the python environment

```
cd /path/to/lichess-bot/
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

Either download stockfish from [the stockfish website](https://stockfishchess.org/download/) or clone the [stockfish repo](https://github.com/official-stockfish/Stockfish), rename it to `stockfish`, and place it inside the `engines/` directory

```
mv /path/to/downloaded/Stockfish/directory /path/to/lichess-bot/src/engines/Stockfish
```

There is no need to keep the binary running in a separate terminal, the Python `Stockfish` library will handle that. Update the path to the stockfish binary in `settings.py` 

```
ENGINE= {
 "path": os.path.join(ENGINE_DIR, "Stockfish/src/stockfish")
  ...
}
```

Make sure everything works!

 ```
 cd lichess-bot/src/lichess/
 python3 main.py
 ```

# Running Tests

To run the tests from the root directory:

```
pytest test/
```

To run a coverage report (from the root directory):

```
coverage run --source=src/lichess -m pytest -v test/ && coverage report -m
```

To see a nicer coverage output (run from the same directory you ran the above coverage command):

```
coverage html && open htmlcov/index.html
```