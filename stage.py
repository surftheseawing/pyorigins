from pyorigins.action import AnimateAction, CallbackAction, SoundAction
from pyorigins.power import Power
from pyorigins.json_file import JsonFile
import os

class Stage(Power):
  def __init__(self, name, msg_up, msg_down=None):
    super().__init__(name, type="origins:multiple")
    self.msg_up = msg_up
    if msg_down:
      self.msg_down = msg_down
    else:
      self.msg_down = msg_up
    self.index = None
    self.key = None
    self.callback = None

  def set_message(self, msg):
    self.msg_up = msg
    self.msg_down = msg

  def set_key(self, index):
    self.index = index
    self.key = "stage" + self.index + "-" + self.name.lower()
    self.name = "Stage " + self.index + ": " + self.name
    return self

  def finalise(self):
    super().finalise()
    if self.callback:
      self.callback.finalise()
      self.data = self.data | {
        "callback": self.callback.data
      }
    return self

  def build(self, power_path):
    json_name = self.key + ".json"
    json_path = os.path.join(power_path, json_name)
    JsonFile(json_path, self.data).build()

  def add_debug_callback(self):
    gain_msg = "+ " + self.key
    lost_msg = "- " + self.key
    if not self.callback:
      self.callback = CallbackAction()
    self.callback.with_entity_action_gained(
      {
        "type": "origins:execute_command",
        "command": "tellraw @s \"" + gain_msg +"\""
      }
    )
    self.callback.with_entity_action_lost(
      {
        "type": "origins:execute_command",
        "command": "tellraw @s \"" + lost_msg +"\""
      }
    )
    return self

  def add_animation_callback(self, name, value):
    if not self.callback:
      self.callback = CallbackAction()
    self.animate_action = AnimateAction(name, value)
    self.callback.with_entity_action_added(
      {
        "type": "origins:delay",
        "ticks": 10,
        "action": self.animate_action.data
      }
    )
    self.callback.with_entity_action_gained(self.animate_action.data)
    return self

  def add_sound_callback(self, name):
    if not self.callback:
      self.callback = CallbackAction()
    self.sound_action = SoundAction(name)
    self.callback.with_entity_action_gained(self.sound_action.data)
    return self

  def add_shaking(self):
    self.data = self.data | {
      "shake": {
        "type": "origins:shaking"
      }
    }
    return self
