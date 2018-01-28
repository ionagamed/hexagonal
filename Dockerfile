FROM frolvlad/alpine-python3
WORKDIR /hexagonal
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apk update && \
    apk add --repository http://dl-cdn.alpinelinux.org/alpine/edge/main --no-cache py3-psycopg2