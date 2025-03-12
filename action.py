
class CallbackAction():
  def __init__(self):
    self.entity_actions = {
      "entity_action_added": None,
      "entity_action_gained": None,
      "entity_action_lost": None,
      "entity_action_respawned": None,
    }
    self.data = {
      "type": "origins:action_on_callback"
    }
  
  def __with_action(self, key, action):
    entity_action = self.entity_actions[key]
    if not entity_action:
      entity_action = {
        "type": "origins:and",
        "actions": []
      }
    entity_action["actions"].append(action)
    self.entity_actions[key] = entity_action

  def finalise(self):
    for key, value in self.entity_actions.items():
      if value:
        self.data = self.data | {
          key: value
        }
    return self

  def merge(self, entity_actions):
    for key, value in entity_actions.items():
      if value:
        for action in value["actions"]:
          self.__with_action(key, action)
    return self

  def with_entity_action_added(self, action):
    self.__with_action("entity_action_added", action)
    return self

  def with_entity_action_gained(self, action):
    self.__with_action("entity_action_gained", action)
    return self

  def with_entity_action_lost(self, action):
    self.__with_action("entity_action_lost", action)
    return self

  def with_entity_action_respawned(self, action):
    self.__with_action("entity_action_respawned", action)
    return self

class IfElseListAction():
  def __init__(self):
    self.actions = []
    self.data = {
      "type": "origins:if_else_list",
    }

  def finalise(self):
    self.data = self.data | {
      "actions": self.actions
    }
    return self

  def with_action(self, condition, action):
    self.actions.append(
      {
        "condition": condition,
        "action": action
      }
    )
    return self

class AnimateAction():
  def __init__(self, name, value):
    self.data = {
      "type": "origins:execute_command",
      "command": "cpm animate @s " + name + " " + str(value)
    }

class SoundAction():
  def __init__(self, name):
    self.data = {
      "type": "origins:play_sound",
      "sound": name
    }
