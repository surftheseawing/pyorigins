def normalise(text):
  return text.lower().replace(" ", "_")

def join_desc(desc, stage_names):
  for index, name in enumerate(stage_names):
    desc = desc + name
    if index < len(stage_names) - 2:
      desc = desc + ", "
    elif index < len(stage_names) - 1:
      desc = desc + ", and "
    else:
      desc = desc + "."
  return desc

# v = b + b * m
# m = (b - v) / b
def multiply_base_additive(base_value, modifier_value):
  return base_value + base_value * modifier_value

# v = b * (1 + m)
# m = (b - v) / b
def multiply_base_multiplicative(base_value, modifier_value):
  return base_value * (1 + modifier_value)
