from pyorigins.common import normalise
from pyorigins.badge import Badge
from pyorigins.json_file import JsonFile
from pyorigins.resource import ActiveSelf, ChargeComponents
from pyorigins.tooltip import Tooltip
import os

class Power:
  def __init__(
      self, name, desc=None, 
      type="origins:simple"):
    self.path = None
    self.name = name
    self.desc = desc
    self.type = type
    self.badges = []
    self.data = {
      "type": self.type,
    }

  def finalise(self):
    if self.badges:
      self.data = self.data | {
        "badges": self.badges
      }
    if self.desc:
      self.data = {
        "description": self.desc,
      } | self.data
    else:
      self.data = {
        "hidden": True
      } | self.data
    self.data = {
      "name": self.name,
    } | self.data
    return self

  def build(self, power_path):
    json_name = normalise(self.name) + ".json"
    json_path = os.path.join(
        power_path,
        self.path,
        json_name,
      ) if self.path else os.path.join(
        power_path,
        json_name)
    JsonFile(json_path, self.data).build()

  def with_data(self, data):
    self.data = self.data | data
    return self

  def with_path(self, path):
    self.path = path
    return self

  def with_badge(self, badge):
    self.badges.append(badge.data)
    return self

  def get_path(self, namespace):
    return ":".join([
      namespace,
      "/".join([
        self.path,
        normalise(self.name)
      ]) if self.path else normalise(self.name)
    ])

class ChargePower(Power):
  def __init__(self, name, desc):
    super().__init__(
      name, desc, "origins:multiple")
    self.charge = ChargeComponents()
    self.enabled = None

  def with_delay_max_value(self, value):
    self.charge.delay.with_max_value(value)
    return self

  def with_delay_hud_render(self, hud_render):
    self.charge.delay.data["hud_render"] = \
      self.charge.delay.data["hud_render"] | hud_render
    return self

  def with_delay_max_actions(self, actions):
    self.charge.delay.data["max_action"]["actions"] = \
      self.charge.delay.data["max_action"]["actions"] + actions
    return self

  def with_charge_condition(self, condition):
    self.charge.with_charge_condition(condition)
    return self

  def with_discharge_interval(self, interval):
    self.charge.with_discharge_interval(interval)
    return self

  def with_enabled(self, enabled):
    self.enabled = enabled
    return self

  def build(self, power_path):
    super().build(power_path)

  def finalise(self):
    super().finalise()
    self.data = self.data | {
      "enabled": self.enabled.data,
    } | self.charge.finalise().data
    return self

class EdiblePower(ChargePower):
  def __init__(self, name, desc):
    super().__init__(name, desc)
    self.items = []
    self.tooltip = Tooltip("Mmm, tasty!")
    self.enabled = ActiveSelf(
      {
        "type": "origins:if_else_list",
        "actions": []
      }
    ).with_cooldown(20).with_key(
      {
        "key": "key.origins.primary_active",
        "continuous": True
      }
    ).with_condition(
      {
        "type": "origins:resource",
        "resource": "*:*_delay_direction",
        "comparison": "==",
        "compare_to": 0
      }
    )

  def build(self, power_path):
    super().build(power_path)

  def finalise(self):
    super().finalise()
    self.tooltip.with_items(self.items)
    self.data = self.data | {
      "tooltip": self.tooltip.data,
    }
    return self

  def with_item(self, namespace, name, text, action, condition=None, type="item"):
    self.items.append(
      {
        "item": ':'.join([namespace, name])
      }
    )
    self.enabled.data["entity_action"]["actions"].append(
      {
        "condition": {
          "type": "origins:and",
          "conditions": [
            {
              "type": "origins:equipped_item",
              "equipment_slot": "mainhand",
              "item_condition": {
                "type": "origins:ingredient",
                "ingredient": {
                  "item": ':'.join([namespace, name])
                }
              }
            }
          ]
        },
        "action": {
          "type": "origins:and",
          "actions": [
            action,
            {
              "type": "origins:equipped_item_action",
              "equipment_slot": "mainhand",
              "action": {
                "type": "origins:consume"
              }
            },
            {
              "type": "origins:play_sound",
              "sound": "minecraft:entity.player.burp"
            }
          ]
        }
      }
    )

    if condition:
      self.enabled.data["entity_action"]["actions"][-1]["condition"]["conditions"].append(condition)

    return self.with_badge(Badge(
      "origins:tooltip"
      ).with_sprite(
        namespace + ":textures/" + type + "/"
        + name + ".png"
      ).with_text(text)
    )
