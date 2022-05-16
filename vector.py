from functools import reduce
import operator


class Vector:

  shortcut_names = ('x', 'y', 'z')

  def __init__(self, components):
    self._components = components

  def __len__(self):
    return len(self._components)

  def __repr__(self) -> str:
    return f'Vector: {self._components}'

  def __getitem__(self, index):
    cls = type(self)
    if type(index) == slice:
      return cls(self._components[index])
    return self._components[index]

  def __getattr__(self, name):
    attr_name_to_index = dict(zip(self.shortcut_names, (0, 1, 2)))
    return self._components[attr_name_to_index[name]]

  def __setattr__(self, name, value):
    if len(name) == 1:
      if name in self.shortcut_names:
        error = 'read only attrs'
      if name.islower():
        error = 'can set lower chars attrs'
      else:
        error = ''
      if error:
        raise AttributeError(error)
    super().__setattr__(name, value)


  def __eq__(self, other):
    return len(self) == len(other) and all(a == b for a, b in zip(self, other))

  def __hash__(self):
    hashes = map(hash, self._components)
    return reduce(operator.xor, hashes)

   

