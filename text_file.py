import os

class TextFile:
  def __init__(self, name, lines):
    self.name = name
    self.lines = lines

  def build(self):
    dirname = os.path.dirname(self.name)
    if not os.path.exists(dirname):
      os.makedirs(dirname)
    with open(self.name, "w") as file:
      for line in self.lines:
        file.write(line + "\n")
