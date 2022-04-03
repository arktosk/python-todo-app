# ToDo App (Python)

Sample todo app that leverage Python as the backend.

## Development

This app using poetry to manage their dependencies, so please make sure you have it installed.

```shell
python -m venv .venv
./.venv/Scripts/activate
poetry install
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
