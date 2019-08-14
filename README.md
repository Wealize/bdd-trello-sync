# bdd-trello-sync

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/1c3991991f754dbfbf9087da93b74942)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=TheNeonProject/bdd-trello-sync&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/1c3991991f754dbfbf9087da93b74942)](https://www.codacy.com?utm_source=github.com&utm_medium=referral&utm_content=TheNeonProject/bdd-trello-sync&utm_campaign=Badge_Coverage)

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
