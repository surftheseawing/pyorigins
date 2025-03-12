from pyorigins.common import normalise
from pyorigins.json_file import JsonFile
import os

class Tag:
  def __init__(self, name):
    self.name = name
    self.path = None
    self.data = {}  

  def build(self, tags_path):
    json_name = normalise(self.name) + ".json"
    json_path = os.path.join(
        tags_path,
        self.path,
        json_name,
      ) if self.path else os.path.join(
        tags_path,
        json_name)
    JsonFile(json_path, self.data).build()
    return self

  def with_path(self, path):
    self.path = path
    return self
 
  def with_replace(self, replace):
    self.data = self.data | {
      "replace": replace
    }
    return self

  def with_values(self, values):
    self.data = self.data | {
      "values" : values
    }
    return self
