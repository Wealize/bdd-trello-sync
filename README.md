# bdd-trello-sync

[![CircleCI](https://circleci.com/gh/TheNeonProject/bdd-trello-sync.svg?style=svg)](https://circleci.com/gh/TheNeonProject/bdd-trello-sync)

## Installation

```bash
virtualenv -p python3 .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
source .venv/bin/activate
TRELLO_APP_KEY=... TRELLO_TOKEN=... TRELLO_BOARD=... python app.py
```

## Test

```bash
source .venv/bin/activate
python -m pytest tests/ --disable-warnings
```
