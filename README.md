# lolcode-interpreter

An interpreter for LOLCODE, written in Python.

## Status
- [x] Lexer
- [x] Parser
- [ ] Interpreter
- [x] Initial frontend (editor, tokens, syntax tree)

## Usage
python3 lexer.py

## Web workbench

Start the local frontend with Python (no additional packages needed):

```sh
python -B app.py
```

Open http://127.0.0.1:8000 in your browser. Stop the server with Ctrl+C.

- Write LOLCODE or load one of the included examples.
- Click **Analyze code**, or press Ctrl+Enter (Cmd+Enter on macOS).
- Inspect the token table and syntax tree, or read lexer/parser errors.
- Open a `.lol` or `.txt` file, and save your editor contents as `playground.lol`.

The workbench uses the existing Python lexer and parser. It checks syntax;
it does not execute programs yet. Keep a saved copy of your code before
closing or refreshing the page. The server listens on localhost for local use.

Run the frontend API checks with:

```sh
python -B -m unittest test_app.py
```
