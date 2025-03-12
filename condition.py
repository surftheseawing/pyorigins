
from pyorigins.common import normalise

class ResourceRangeCondition():
  def __init__(self, resource_name, low_threshold, high_threshold):
    self.data = {
      "type": "origins:and",
      "conditions": [
        {
          "type": "origins:resource",
          "resource": "*:" + normalise(resource_name) + "_resource",
          "comparison": ">=",
          "compare_to": low_threshold
        },
        {
          "type": "origins:resource",
          "resource": "*:" + normalise(resource_name) + "_resource",
          "comparison": "<",
          "compare_to": high_threshold
        }
      ]
    }
