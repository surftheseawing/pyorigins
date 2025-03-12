import os

class OriginPack:
  def __init__(self, src_path, namespace):
    # content
    self.archive = None
    self.functions = None
    self.meta = None
    self.namespace = namespace
    self.origin_layers = None
    self.origins = None
    self.powers = None
    self.predicates = None
    self.tags = None
    # primary paths
    self.src_path = src_path
    self.data_path = os.path.join(
      self.src_path, "data")
    self.namespace_path = os.path.join(
      self.data_path, self.namespace)
    # secondary paths
    self.functions_path = os.path.join(
      self.namespace_path, "functions")
    self.origins_path = os.path.join(
      self.namespace_path, "origins")
    self.powers_path = os.path.join(
      self.namespace_path, "powers")
    self.predicates_path = os.path.join(
      self.namespace_path, "predicates")
    self.tags_path = os.path.join(
      self.namespace_path, "tags")

  def with_meta(self, meta):
    self.meta = meta
    return self

  def with_functions(self, functions):
    self.functions = functions
    return self

  def with_origin_layers(self, origin_layers):
    self.origin_layers = origin_layers
    return self

  def with_origins(self, origins):
    self.origins = origins
    return self

  def with_powers(self, powers):
    self.powers = powers
    return self

  def with_predicates(self, predicates):
    self.predicates = predicates
    return self

  def with_tags(self, tags):
    self.tags = tags
    return self

  def with_archive(self, archive):
    self.archive = archive
    return self

  def build(self):
    if self.functions:
      for function in self.functions:
        function.build(self.functions_path)

    if self.meta:
      self.meta.build(self.src_path)

    if self.origin_layers:
      for origin_layer in self.origin_layers:
        origin_layer.build(self.data_path)

    if self.origins:
      for origin in self.origins:
        origin.build(self.origins_path) 

    if self.powers:
      for power in self.powers:
        power.finalise().build(self.powers_path)

    if self.predicates:
      for predicate in self.predicates:
        predicate.build(self.predicates_path)

    if self.tags:
      for tag in self.tags:
        tag.build(self.tags_path)

    if self.archive:
      self.archive.build()
