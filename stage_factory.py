from pyorigins.common import normalise
from pyorigins.power import Power
import os

class StageFactory(Power):
  def __init__(
      self, resource_name, stages,
      type="origins:simple"):
    desc = "You have " + str(len(stages)) + \
      " stages of " + resource_name + ": "
    for index, stage in enumerate(stages):
      desc = desc + stage.name
      if index < len(stages) - 2:
        desc = desc + ", "
      elif index < len(stages) - 1:
        desc = desc + ", and "
      else:
        desc = desc + "."
    super().__init__(
      resource_name + " Stages",
      desc=desc, type=type)
    self.resource_name = resource_name
    self.has_callback = False
    self.stages = stages
    self.verbose = False
    for index, stage in enumerate(self.stages):
      stage.set_key(str(index))

  def with_animation_callbacks(self, animation_name):
    # TODO CPM changed max value layer from 255 to 100
    animation_step = 255 / (len(self.stages) - 1)
    for index, stage in enumerate(self.stages):
      animation_value = int(index * animation_step)
      if self.verbose:
        print("{:>4}".format(animation_value))
      stage.add_animation_callback(
        animation_name, animation_value)
    return self

  def with_sound_callbacks(self, sound_name):
    for stage in self.stages:
      stage.add_sound_callback(sound_name)
    return self

  def with_debug_callbacks(self):
    for stage in self.stages:
      stage.add_debug_callback()
    return self

  def build(self, power_path):
    super().build(power_path)
    resource_path = os.path.join(power_path, normalise(self.resource_name))
    if not os.path.exists(resource_path):
      os.mkdir(resource_path)
    for stage in self.stages:
      stage.build(resource_path)

  def with_verbose(self, verbose):
    self.verbose = verbose
    return self

  def finalise(self):
    super().finalise()
    for stage in self.stages:
      stage.finalise()
    return self
