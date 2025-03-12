from pyorigins.json_file import JsonFile
import os

class OriginLayer:
  def __init__(self, origins):
    self.namespace = "origins"
    self.file = "origin.json"
    self.data = {
      "origins": [
        origin.get_path() for origin in origins
      ]
    }

  def with_namespace(self, namespace):
    self.namespace = namespace
    return self

  def with_data(self, data):
    self.data = self.data | data
    return self

  def build(self, data_path):
    JsonFile(
      os.path.join(
        data_path,
        self.namespace,
        "origin_layers",
        self.file),
      self.data
    ).build()
    return self
