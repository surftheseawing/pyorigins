from pyorigins.action import CallbackAction
from pyorigins.common import normalise
from pyorigins.power import Power
from pyorigins.resource import ActionOverTime, Resource

class StageTransitions(Power):
  def __init__(
      self, resource_name, stages):
    super().__init__(
      resource_name + " Transitions",
      type="origins:multiple")
    self.resource_name = resource_name
    self.stages = stages
    self.path = None
    self.verbose = False
    self.callback = None
    self.revoke_all_source = None
    self.previous_stage = Resource(0, len(stages) - 1)
    self.grant_actions = []
    self.revoke_actions = []

  def finalise(self):
    super().finalise()
    if self.callback:
      self.callback.finalise()
      super().with_data(
        {
          "callback": self.callback.data
        }
      )
    super().with_data(
      {
        "previous_stage": self.previous_stage.data,
      }
    )
    for index in range(len(self.stages)):
      super().with_data(
        {
          "stage_" + str(index) + "_grant": self.grant_actions[index].data,
          "stage_" + str(index) + "_revoke": self.revoke_actions[index].data,
        }
      )
    return self

  def with_verbose(self, verbose):
    self.verbose = verbose
    return self

  def with_revoke_all_source(self, source):
    self.revoke_all_source = source
    return self

  def make_stage_transitions(
      self, interval, resource_min, resource_max, source="*:*"):
    resource_diff = resource_max - resource_min
    resource_step = resource_diff / len(self.stages)
    self.callback_actions = []
    for index, stage in enumerate(self.stages):
      grant_low = int(resource_min +
        index * resource_step)
      grant_high = int(resource_min +
        resource_step * ((index + 1) * 0.4 + index * 0.7))
      revoke_low = int(resource_min +
        resource_step * (index * 0.4 + max(0, index - 1) * 0.7))
      revoke_high = int(resource_min +
        (index + 1) * resource_step)
      if self.verbose:
        print("{:>4} {:>4} {:>4} {:>4}".format(
          int(grant_low), int(grant_high),
          int(revoke_low), int(revoke_high)))
      grant_condition = StageCondition(
        self.resource_name, grant_low, grant_high)
      grant_action = StageGrantAction(
        self.resource_name, stage.key, source) \
        .with_messages(index, stage.msg_up, stage.msg_down)
      # do not print messages on callback action
      callback_action = StageGrantAction(
        self.resource_name, stage.key, source)
      revoke_condition = StageCondition(
        self.resource_name, revoke_low, revoke_high)
      revoke_action = StageRevokeAction(
        self.resource_name, stage.key, source, index)
      callback_condition = StageCondition(
        self.resource_name, grant_low, revoke_high)
      grant = ActionOverTime() \
        .with_interval(interval) \
        .with_condition(grant_condition.data) \
        .with_rising_action(grant_action.data)
      revoke = ActionOverTime() \
        .with_interval(interval) \
        .with_condition(revoke_condition.data) \
        .with_falling_action(revoke_action.data)
      self.grant_actions.append(grant)
      self.revoke_actions.append(revoke)
      self.callback_actions.append(
        {
          "condition": callback_condition.data,
          "action": callback_action.data
        }
      )
    # end loop
    self.callback = CallbackAction() \
    .with_entity_action_gained(
      {
        "type": "origins:if_else_list",
        "actions": self.callback_actions
      }
    )
    if self.revoke_all_source:
      self.callback.with_entity_action_lost(
        {
          "type": "origins:execute_command",
          "command": "power revokeall @s " + self.revoke_all_source
        }
      )
    return self

class StageCondition():
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

class StageGrantAction():
  def __init__(self, resource_name, stage_key, source):
    self.data = {
      "type": "origins:delay",
      "ticks": 1,
      "action": {
        "type": "origins:and",
        "actions": [
          {
            "type": "origins:grant_power",
            "power": "*:" + normalise(resource_name) + "/" + stage_key,
            "source": source
          }
        ]
      }
    }

  def with_messages(self, stage_index, msg_up, msg_down):
    self.data["action"]["actions"].append(
      {
        "type": "origins:if_else",
        "condition": {
          "type": "origins:resource",
          "resource": "*:*_previous_stage",
          "comparison": ">",
          "compare_to": stage_index
        },
        "if_action": {
          "type": "origins:execute_command",
          "command": "tellraw @s \"" + msg_down +"\""
        },
        "else_action": {
          "type": "origins:execute_command",
          "command": "tellraw @s \"" + msg_up +"\""
        }
      }
    )
    return self

class StageRevokeAction():
  def __init__(self, resource_name, stage_key, source, stage_index):
    self.data = {
      "type": "origins:and",
      "actions": [
        {
          "type": "origins:revoke_power",
          "power": "*:" + normalise(resource_name) + "/" + stage_key,
          "source": source
        },
        {
          "type": "origins:change_resource",
          "resource": "*:*_previous_stage",
          "operation": "set",
          "change": stage_index
        }
      ]
    }
