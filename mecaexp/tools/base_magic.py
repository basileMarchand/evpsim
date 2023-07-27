from collections import OrderedDict
from .variables import StateVariable


class MetaMagic(type):
    def __new__(mcs, cls, bases, dct):
        variables = OrderedDict()

        for base in bases:
            variables.update(base._variables)

        # Now we loop on the class attributes store the components where they should be and
        # delete the first-hand class attribute
        to_remove = []
        for key, value in dct.items():
            if isinstance(value, StateVariable):
                if key in variables.keys():
                    raise ValueError(
                        f"Variable {key} is already inherited for object {cls}.")
                value.name = key
                variables[key] = value
                to_remove.append(key)
        for name in to_remove:
            del dct[name]
        dct['_variables'] = variables
        dct['_all_variables'] = variables.copy()
        return super().__new__(mcs, cls, bases, dct)


class BaseMagic(metaclass=MetaMagic):
    def __init__(self):
        for key, value in self._variables.items():
            setattr(self, key, value)

    def link_to(self, parent):
        parent._all_variables.update(self._all_variables)
