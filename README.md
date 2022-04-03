# ToDo App (Python)

Sample todo app that leverage Python as the backend.

## Development

```shell
python -m venv .venv
./.venv/Scripts/activate
python -m pip install pip-tools mypy
# pip-compile requirements.in
pip-sync
```

Provide app configuration via `.env` file

```txt
SECRET_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Start app

```shell
uvicorn app.main:app --reload
```
