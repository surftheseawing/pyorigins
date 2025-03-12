from pyorigins.json_file import JsonFile
import os

class PackMeta:
  def __init__(self, format, desc):
    self.format = format
    self.desc = desc
    self.file = "pack.mcmeta"
    self.data = {
      "pack": {
        "pack_format": self.format,
        "description": self.desc
      }
    }

  def build(self, src_path):
    JsonFile(
      os.path.join(src_path, self.file),
      self.data
    ).build()
    return self
