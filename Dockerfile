FROM python:3.7-alpine
WORKDIR /usr/local/src/
RUN apk update && apk add --no-cache postgresql-dev gcc python3-dev musl-dev uwsgi-python3
COPY requirements.txt /usr/local/src/requirements.txt
RUN pip install --no-cache-dir -r /usr/local/src/requirements.txt
COPY . /usr/local/src
RUN pip install --no-cache-dir -e . && python setup.py clean --all
EXPOSE 3031
CMD [ "uwsgi", "--socket", "0.0.0.0:3031", \
               "--uid", "uwsgi", \
               "--plugins", "python3", \
               "--protocol", "uwsgi", \
               "--wsgi", "librarian:wsgi" ]
