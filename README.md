# Lick Generator

> "The Lick is a lick regarded as "the most famous jazz cliché ever". The phrase has been used on numerous jazz and pop records and is part of several classical compositions. In recent years, it has become an internet meme and is sometimes used for comedic effect." - [Wikipedia](https://en.wikipedia.org/wiki/The_Lick)

This site allows you to specify some parameters, and generate your own lick to download.

## Running

* Specify at the top of `lick_generator.py` in `LICK_GEN_MAX` how many audio files it is allowed to generate. This will be based on storage limits.

* Create a virtual env (i.e. `python3 -m venv .venv` and `source .venv/bin/activate`)

* Install the dependencies (`pip install -r requirements.txt`)

* Run the Python file (`python3 lick_generator.py`). Visit the site at the URL given by Flask in the console (i.e. `http://127.0.0.1:5000`).

###### Michael Grace, February 2021