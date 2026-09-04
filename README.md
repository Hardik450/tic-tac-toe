# Tic-Tac-Toe (Flask)

A web version of the pygame tic-tac-toe project. The unbeaten minimax AI
(`tictactoe.py`) is unchanged — it now runs behind a small Flask API instead
of a pygame loop.

## Project structure

```
app.py              Flask app + API routes
tictactoe.py         Game logic and minimax AI (unchanged from the original)
templates/index.html Page markup
static/style.css     Styling
static/script.js     Frontend game logic (fetches from the API)
requirements.txt     Python deps
Procfile              Tells Render how to start the app
```

## Run locally

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Visit http://localhost:5000

## Deploy on Render

1. Push this folder to a GitHub repo.
2. In Render: **New +** → **Web Service** → connect the repo.
3. Settings:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app` (already set via the `Procfile`, so
     Render should pick it up automatically)
4. Deploy. Render sets the `PORT` environment variable automatically, and
   `app.py` already reads it.

No other configuration is needed — there's no database or external service.
