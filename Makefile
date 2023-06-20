export FLASK_APP=app.py

run:
	python3 -m flask run --host=0.0.0.0

database:
	rm db/users.db
	sqlite3 db/users.db < db/db.sql
