# Feed Me Event Booking Website

This is the repository for the Feed Me website.

## Setup Instructions

### Setup env_config.py

Setup the env_config.py file manually with local host, the database name,
and your local username and password. 

### Setup virtual environment

Create and activate a virtual environment:

(MacOS)
```
python3 -m venv /path/to/venv
source venv/bin/activate
```

(Windows)
```
python -3 -m venv c:/path/to/venv
source venv/bin/activate
```

Install packages through requirements.txt:
```
pip install -r requirements.txt
```

Run Flask app:
```
flask run --reload --debugger
```

Exit virtual environment:
```
deactivate
```

### Setup database

:memo: TODO

### .app_config.py

Contains TEMPLATES_AUTO_RELOAD setting (don't need to restart Flask for changes) and secret key.

### .flaskenv

Contains settings so that user doesn't have to specify in terminal.