FROM frolvlad/alpine-python3
WORKDIR /hexagonal
RUN pip install flask
RUN pip install flask_sqlalchemy
RUN apk update && \
    apk add --repository http://dl-cdn.alpinelinux.org/alpine/edge/main --no-cache py3-psycopg2
CMD ["python", "server/hexagonal/app.py"]