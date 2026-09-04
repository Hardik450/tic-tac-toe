import os

from flask import Flask, jsonify, render_template, request

import tictactoe as ttt

app = Flask(__name__)


def board_status(board):
    """Build the status payload the frontend needs after any move."""
    game_over = ttt.terminal(board)
    return {
        "board": board,
        "game_over": game_over,
        "winner": ttt.winner(board) if game_over else None,
        "current_player": None if game_over else ttt.player(board),
    }


def parse_board(data):
    board = data.get("board")
    if (
        not isinstance(board, list)
        or len(board) != 3
        or any(not isinstance(row, list) or len(row) != 3 for row in board)
    ):
        raise ValueError("Malformed board")
    # Normalize any stray values to the shapes tictactoe.py expects.
    clean = []
    for row in board:
        clean_row = []
        for cell in row:
            clean_row.append(cell if cell in (ttt.X, ttt.O) else ttt.EMPTY)
        clean.append(clean_row)
    return clean


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/new_game")
def new_game():
    return jsonify(board_status(ttt.initial_state()))


@app.route("/api/move", methods=["POST"])
def move():
    """Apply a human move."""
    data = request.get_json(force=True, silent=True) or {}
    try:
        board = parse_board(data)
        action = tuple(data.get("action"))
    except (ValueError, TypeError):
        return jsonify({"error": "Malformed request"}), 400

    if ttt.terminal(board):
        return jsonify({"error": "Game is already over"}), 400
    if action not in ttt.actions(board):
        return jsonify({"error": "Invalid move"}), 400

    board = ttt.result(board, action)
    return jsonify(board_status(board))


@app.route("/api/ai_move", methods=["POST"])
def ai_move():
    """Compute and apply the AI's optimal move."""
    data = request.get_json(force=True, silent=True) or {}
    try:
        board = parse_board(data)
    except ValueError:
        return jsonify({"error": "Malformed request"}), 400

    if ttt.terminal(board):
        return jsonify({"error": "Game is already over"}), 400

    action = ttt.minimax(board)
    board = ttt.result(board, action)
    return jsonify(board_status(board))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
