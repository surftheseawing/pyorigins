from pyorigins.common import normalise
from pyorigins.badge import Badge
from pyorigins.json_file import JsonFile
from pyorigins.resource import ActiveSelf, ChargeComponents
from pyorigins.tooltip import Tooltip
import os

class Predicate:
  def __init__(self, namespace, name, type):
    self.namespace = namespace
    self.path = None
    self.name = name
    self.type = type
    self.data = {
      "condition": self.type,
    }

  def build(self, predicates_path):
    json_name = normalise(self.name) + ".json"
    json_path = os.path.join(
        predicates_path,
        self.path,
        json_name,
      ) if self.path else os.path.join(
        predicates_path,
        json_name)
    JsonFile(json_path, self.data).build()

  def with_data(self, data):
    self.data = self.data | data
    return self

  def with_path(self, path):
    self.path = path
    return self
