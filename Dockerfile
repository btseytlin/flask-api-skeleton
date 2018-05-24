FROM python:3.6-alpine
WORKDIR /usr/local/src/
RUN apk update && apk add --no-cache bash \
                                    postgresql-dev \
                                    gcc \
                                    python3-dev \
                                    musl-dev \
                                    libxml2-dev \
                                    libxslt-dev \
                                    build-base \
                                    linux-headers
RUN pip install uwsgi
COPY requirements.txt /usr/local/src/requirements.txt
RUN pip --no-cache-dir install  -r /usr/local/src/requirements.txt
COPY . /usr/local/src
RUN python setup.py clean --all && \
    pip --no-cache-dir install  -e . && \
    python setup.py clean --all
EXPOSE 8000
CMD [ "uwsgi", "--yaml /usr/local/src/uwsgi.yml" ]