FROM python:alpine3.17

WORKDIR /bisous-bisous

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY static static
COPY templates templates
COPY db/users.db db/users.db
COPY app.py app.py
COPY database.py database.py
COPY flask_session flask_session

ENV FLASK_APP=app.py
EXPOSE 5000

CMD [ "python3", "-m", "flask", "run", "--host", "0.0.0.0" ]
