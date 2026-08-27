# AGENTS.md

## Cursor Cloud specific instructions

This is a small single-service Flask web app (a classroom check-in quiz, UI is in Chinese). A random quiz question is read from `questions.xlsx` (via `pandas`/`openpyxl`); answering it correctly checks a name in, and `/results` shows the tally.

### Services

| Service | Run command | URL |
| --- | --- | --- |
| Flask dev server | `.venv/bin/python app.py` | http://127.0.0.1:5000/ |

Routes: `/` (quiz page), `POST /submit` (grade + check in), `/results` (check-in tally).

### Environment

- Python 3.12 with a virtualenv at `.venv` (dependencies are pinned in `requirements.txt`). The update script keeps `.venv` in sync; activate it with `. .venv/bin/activate` or call binaries directly as `.venv/bin/...`.
- The system package `python3.12-venv` is required to create the venv (already present in the environment snapshot).

### Non-obvious notes

- `correct_answer` is a single module-level global that is overwritten on **every** `GET /`. `POST /submit` grades against that shared global, not against a per-session question. So any request that hits `GET /` (e.g. a second browser tab, a reload, or a separate probe) changes the "correct" answer for everyone. When testing an end-to-end check-in, load the page once and submit without any intervening `GET /`, or the answer you see may not match what `/submit` grades against.
- `sign_in_data` is kept in memory only; restarting the server clears all check-ins.
- There is no configured linter or automated test suite in this repo. The closest available check is `python -m py_compile app.py`.
- Production entrypoints exist but are not needed for development: `Procfile` (`gunicorn app:app`) and `vercel.json`. Use the Flask dev server (`python app.py`) for development.
