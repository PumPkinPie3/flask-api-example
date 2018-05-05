FROM    python
COPY    . /app
WORKDIR /app
RUN     pip install -r requirements.txt
ENV     FLASK_APP /app/application.py
CMD     flask db_create && flask db_init && flask run -h 0.0.0.0