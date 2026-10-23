"""Local web interface for the lexer and parser. Run with python -B app.py."""

import json
from dataclasses import fields, is_dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from lexer import tokenize
from parser import Parser

FRONTEND = Path(__file__).parent / "frontend"
MAX_SOURCE_BYTES = 100_000


def ast_to_dict(value):
    """Keep node names so the syntax tree is easier to read in the browser."""
    if is_dataclass(value):
        return {"node": type(value).__name__, **{
            field.name: ast_to_dict(getattr(value, field.name))
            for field in fields(value)
        }}
    if isinstance(value, list):
        return [ast_to_dict(item) for item in value]
    if isinstance(value, dict):
        return {key: ast_to_dict(item) for key, item in value.items()}
    return value


def analyze(source):
    tokens = []
    stage = "lexer"
    try:
        tokens = tokenize(source)
        stage = "parser"
        parser = Parser(tokens)
        program = parser.parse()
        # The parser currently stops after the program and trailing functions.
        if not parser.is_at_end():
            token = parser.peek()
            raise SyntaxError(f"Line {token[2]}: Unexpected token '{token[1]}' after program.")
        return {"ok": True, "tokens": tokens, "ast": ast_to_dict(program)}
    except (SyntaxError, RecursionError, ValueError) as error:
        message = str(error)
        if isinstance(error, RecursionError):
            message = "Expressions are nested too deeply. Try simplifying the program."
        return {"ok": False, "tokens": tokens, "ast": None,
                "error": {"stage": stage, "message": message}}


class Handler(BaseHTTPRequestHandler):
    def send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        assets = {"/": ("index.html", "text/html"),
                  "/style.css": ("style.css", "text/css"),
                  "/app.js": ("app.js", "text/javascript")}
        asset = assets.get(self.path.split("?", 1)[0])
        if asset is None:
            self.send_error(404)
            return
        body = (FRONTEND / asset[0]).read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", asset[1] + "; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/api/analyze":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= MAX_SOURCE_BYTES:
                self.send_json({"message": "Choose a program smaller than 100 KB."}, 413)
                return
            data = json.loads(self.rfile.read(length))
            if not isinstance(data, dict) or not isinstance(data.get("source"), str):
                raise ValueError("Expected a source string.")
        except (ValueError, UnicodeDecodeError):
            self.send_json({"message": "Send a JSON object with a source string."}, 400)
            return
        self.send_json(analyze(data["source"]))


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8000), Handler)
    print("LOLCODE Workbench: http://127.0.0.1:8000", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
