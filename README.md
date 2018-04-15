# crispy-pastebin-train-anything

### Main.py
Fetch, download and insert pastes to the database and disk. It uses restlogging/ as a local logger.

### Properties.py
It's a wrapper for Python file config.py, in which we have our values like password, username, etc

### Logger.py
Plain wrapper for my other Java project restlogging/, just provide header value and data to the function log() and it'll save given log to the database.

### tableP.sql
SQL file to create table used by our scraper to keep information and content of the pastes.

## How to run it?
I recommend buying pastebin PRO API and whitelist your computer IP. Then log on to mysql, select database, run file `tableP.sql`. Fill `config.py` with values of your own, and run Main.py file :)
