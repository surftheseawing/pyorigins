from pyorigins.common import normalise
from pyorigins.json_file import JsonFile
import os

class Origin:
  def __init__(self, name, desc):
    self.namespace = "origins"
    self.name = name
    self.desc = desc
    self.type = type
    self.data = {
      "name": self.name,
      "description": self.desc,
      "powers": []
    }

  def with_namespace(self, namespace):
    self.namespace = namespace
    return self

  def with_order(self, order):
    self.data = self.data | {
      "order": order
    }
    return self

  def with_impact(self, impact):
    self.data = self.data | {
      "impact": impact
    }
    return self

  def with_icon(self, icon_item):
    self.data = self.data | {
      "icon": {
        "item": icon_item
      },
    }
    return self

  def add_power_paths(self, power_paths):
    self.data["powers"] = self.data["powers"] + power_paths
    return self

  def add_powers(self, powers):
    power_paths = [power.get_path(self.namespace) for power in powers]
    self.data["powers"] = self.data["powers"] + power_paths
    return self

  def build(self, origins_path):
    JsonFile(
      os.path.join(
        origins_path,
        normalise(self.name) + ".json"),
      self.data
    ).build()
    return self

  def get_path(self):
    return ":".join([
      self.namespace,
      normalise(self.name)
    ])
