class ModifyExhaustion:
  def __init__(self, debug_mode=False):
    exhaustion_modifier = -0.99 if debug_mode else -0.999
    self.data = {
        "type": "origins:modify_exhaustion",
        "modifier": {
          "operation": "multiply_base_multiplicative",
          "resource": "*:*_resource",
          "value": 0,
          "modifier": {
            "operation": "multiply_base_multiplicative",
            "value": exhaustion_modifier
          }
        }
      }

class ModifyVelocity:
  def __init__(self, debug_mode=False):
    velocity_modifier = -1.000467 if debug_mode else -1.000267
    self.data = {
      "type": "origins:modify_velocity",
      "axes": [
        "x",
        "z"
      ],
      "condition": {
        "type": "origins:or",
        "conditions": [
          {
            "type": "origins:on_block"
          },
          {
            "type": "origins:submerged_in",
            "fluid": "minecraft:water"
          }
        ]
      },
      "modifier": {
        "operation": "multiply_base_multiplicative",
        "resource": "*:*_resource",
        "value": 0,
        "modifier": {
          "operation": "multiply_base_multiplicative",
          "value": velocity_modifier
        }
      }
    }