from flask import Flask
import os
from importlib import import_module

env = os.environ.get('ENV', 'test')
config = import_module('config.' + env)

app = Flask('hexagonal')
app.config.update(config.config)
app.name = app.config.get('APP_NAME', 'hexagonal')


@app.route('/')
def hello_world():
    return 'Hello, world!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
