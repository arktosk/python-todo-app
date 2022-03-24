# ToDo App (Python)

Sample todo app that leverage Python as the backend.

## Development

```shell
python -m venv .venv
./.venv/Scripts/activate
python -m pip install pip-tools mypy
# pip-compile requirements.in
pip-sync
uvicorn app.main:app --reload
```
