import json
import os

class JsonFile:
  def __init__(self, name, data):
    self.name = name
    self.data = data

  def build(self):
    dirname = os.path.dirname(self.name)
    if not os.path.exists(dirname):
      os.makedirs(dirname)
    with open(self.name, "w") as file:
      json.dump(self.data, file, indent=2)
