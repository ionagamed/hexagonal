FROM frolvlad/alpine-python3
WORKDIR /hexagonal
COPY requirements.txt requirements.txt
COPY wait-for-postgres.sh /wait-for-postgres.sh
RUN chmod +x /wait-for-postgres.sh
RUN pip install -r requirements.txt
RUN apk update && \
    apk add --repository http://dl-cdn.alpinelinux.org/alpine/edge/main --no-cache py3-psycopg2
RUN apk add postgresql-client
