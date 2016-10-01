from os import path


print(path.isfile(path.abspath(path.join(path.dirname(__file__), 'configuration.yaml'))))