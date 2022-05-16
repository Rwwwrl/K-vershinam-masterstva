class DescBaseClass:


  def __init__(self):
    self.prefix = 'some_prefix'

  def __get__(self, instance, owner):
    if instance is None:
      return self
    return getattr(instance, self.prefix)

  def __set__(self, instance, value):
    setattr(instance, self.prefix, value)


class Validator(DescBaseClass):

  def __set__(self, instance, value):
    self.validate(value=value)
    super().__set__(instance, value)

  @staticmethod
  def validate(value):
    raise NotImplementedError


class PositiveInteger(Validator):

  @staticmethod
  def validate(value):
    if value <= 0:
      raise ValueError('value must be > 0')


class ModelBaseClass(type):


  _desc_fields = []

  def __init__(cls, *args, **kwargs):
    for key, attr in cls.__dict__.items():
      if isinstance(attr, Validator):
        attr_cls = attr.__class__.__name__
        attr.prefix = f'{attr_cls}#{key}'
        cls._desc_fields.append(key)


class Model(metaclass=ModelBaseClass):

  def __init__(self, *args, **kwargs):
    desc_field = type(self)._desc_fields
    for field in desc_field:
      setattr(self, field, kwargs.get(field))
