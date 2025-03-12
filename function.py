from pyorigins.common import normalise
from pyorigins.text_file import TextFile
import os

class Function:
  def __init__(self, name):
    self.path = None
    self.name = name
    self.lines = []

  def build(self, functions_path):
    file_name = normalise(self.name) + ".mcfunction"
    file_path = os.path.join(
        functions_path,
        self.path,
        file_name,
      ) if self.path else os.path.join(
        functions_path,
        file_name)
    TextFile(file_path, self.lines).build()

  def with_lines(self, lines):
    self.lines = self.lines + lines
    return self
