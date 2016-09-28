import yaml


data = """
        name: amin
        """
print yaml.load(data)

yaml.dump({'name': 'reza'}, data)

print yaml.load(data)