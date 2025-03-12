class Tooltip:
  def __init__(self, text):
    self.text = text
    self.data = {
        "type": "origins:tooltip",
        "text": text,
    }

  def with_items(self, items):
    self.data = self.data | {
      "item_condition": {
        "type": "origins:ingredient",
        "ingredient": items
      }
    }
