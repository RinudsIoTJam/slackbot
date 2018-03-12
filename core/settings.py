import json

def load(filename, **kwargs):
  with open(filename, 'r') as settings_file:
    config = json.load(settings_file)
  return config

def save(config, filename, **kwargs):
  with open(filename, 'w') as settings_file:
    json.dump(config, settings_file, indent=2, sort_keys=False)
  return