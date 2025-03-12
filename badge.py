class Badge:
  def __init__(self, type):
    self.type = type
    self.sprite = None
    self.text = None
    self.data = {
      "type": type
    }

  def with_sprite(self, sprite):
    self.sprite = sprite
    self.data = self.data | {
      "sprite": sprite
    }
    return self

  def with_text(self, text):
    self.text = text
    self.data = self.data | {
      "text": text
    }
    return self
