class Resource:
  def __init__(self, min, max):
    self.min = min
    self.max = max
    self.data = {
      "type": "origins:resource",
      "min": self.min,
      "max": self.max,
      "start_value": self.min,
      "hud_render": {
        "should_render": False
      }
    }

  def with_min_value(self, value):
    self.data = self.data | {
      "min": value
    }
    return self

  def with_max_value(self, value):
    self.data = self.data | {
      "max": value
    }
    return self

  def with_start_value(self, value):
    self.data = self.data | {
      "start_value": value
    }
    return self

  def with_hud_render(self, hud_render):
    self.data["hud_render"] = hud_render
    return self

  def with_min_action(self, min_action):
    self.data = self.data | {
      "min_action": min_action
    }
    return self

  def with_max_action(self, max_action):
    self.data = self.data | {
      "max_action": max_action
    }
    return self

class ActiveSelf:
  def __init__(self, entity_action):
    self.data = {
      "type": "origins:active_self",
      "entity_action": entity_action,
      "hud_render": {
        "should_render": False
      }
    }
  
  def with_cooldown(self, cooldown):
    self.data = self.data | {
      "cooldown": cooldown
    }
    return self

  def with_hud_render(self, hud_render):
    self.data["hud_render"] = hud_render
    return self

  def with_key(self, key):
    self.data = self.data | {
      "key": key
    }
    return self

  def with_condition(self, condition):
    self.data = self.data | {
      "condition": condition
    }
    return self

class ActionOverTime:
  def __init__(self):
    self.data = {
      "type": "origins:action_over_time"
    }

  def with_interval(self, interval):
    self.data = self.data | {
      "interval": interval
    }
    return self

  def with_entity_action(self, entity_action):
    self.data = self.data | {
      "entity_action": entity_action
    }
    return self

  def with_rising_action(self, action):
    self.data = self.data | {
      "rising_action": action
    }
    return self

  def with_falling_action(self, action):
    self.data = self.data | {
      "falling_action": action
    }
    return self

  def with_condition(self, condition):
    self.data = self.data | {
      "condition": condition
    }
    return self

class Component():
  def __init__(self, type):
    self.data = {
      "type": type
    }

  def with_data(self, data):
    self.data = self.data | data
    return self

class ChargeComponents:
  def __init__(self):
    self.delay_direction = Resource(0, 1).with_start_value(1)
    self.delay = Resource(0, 20).with_hud_render(
      {
        "sprite_location": "origins:textures/gui/community/spiderkolo/resource_bar_03.png",
        "bar_index": 22,
        "condition": {
          "type": "origins:resource",
          "resource": "*:*_delay",
          "comparison": ">",
          "compare_to": 0
        }
      }
    ).with_min_action(
      {
        "type": "origins:change_resource",
        "resource": "*:*_delay_direction",
        "operation": "set",
        "change": 1
      }
    ).with_max_action(
      {
        "type": "origins:and",
        "actions": [
          {
            "type": "origins:change_resource",
            "resource": "*:*_delay_direction",
            "operation": "set",
            "change": 0
          }
        ]
      }
    )
    self.charge = ActiveSelf(
      {
        "type": "origins:change_resource",
        "resource": "*:*_delay",
        "change": 1
      }
    ).with_cooldown(1).with_key(
      {
        "key": "key.origins.primary_active",
        "continuous": True
      }
    ).with_condition(
      {
        "type": "origins:and",
        "conditions": [
          {
            "type": "origins:sneaking",
            "inverted": True
          },
          {
            "type": "origins:resource",
            "resource": "*:*_delay_direction",
            "comparison": "==",
            "compare_to": 1
          },
          {
            "type": "origins:equipped_item",
            "equipment_slot": "mainhand",
            "item_condition": {
              "type": "origins:empty"
            },
            "inverted": True
          }
        ]
      }
    )
    self.discharge = ActionOverTime(
    ).with_interval(4).with_entity_action(
      {
        "type": "origins:change_resource",
        "resource": "*:*_delay",
        "change": -1
      }
    ).with_condition(
      {
        "type": "origins:resource",
        "resource": "*:*_delay",
        "comparison": ">",
        "compare_to": 0
      }
    )

  def finalise(self):
    self.data = {
      "delay_direction": self.delay_direction.data,
      "delay": self.delay.data,
      "charge": self.charge.data,
      "discharge": self.discharge.data,
    }
    return self
  
  def with_discharge_interval(self, interval):
    self.discharge.with_interval(interval)
    return self

  def with_charge_condition(self, condition):
    self.charge.data["condition"]["conditions"] = \
      self.charge.data["condition"]["conditions"] + [condition]
    return self
