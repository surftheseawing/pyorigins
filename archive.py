import os
import shutil

class Archive:
  def __init__(self, type, name, dst, src):
    self.type = type
    self.name = name
    self.dst = dst
    self.src = src
  def build(self):
    shutil.make_archive(os.path.join(self.dst, self.name), self.type, self.src)
