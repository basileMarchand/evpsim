import copy
from collections import OrderedDict
from .variables import StateVariable, VarStatus


class MetaMagic(type):
    def __new__(mcs, cls, bases, dct):
        variables = OrderedDict()
        integ_variables = []

        for base in bases:
            variables.update(base._variables)

        # Now we loop on the class attributes store the components where they should be and
        # delete the first-hand class attribute
        to_remove = []
        for key, value_ in dct.items():
            if isinstance(value_, StateVariable):
                value = copy.deepcopy(value_)

                if key in variables.keys():
                    raise ValueError(
                        f"Variable {key} is already inherited for object {cls}.")
                value.name = key
                variables[key] = value
                to_remove.append(key)

        for name in to_remove:
            del dct[name]
        dct['_variables'] = variables
        # dct['_all_variables'] = variables.copy()
        new_cls = super().__new__(mcs, cls, bases, dct)
        # for key, value in variables.items():
        #     setattr(new_cls, f"_{key}", StateVariable(
        # value.type, value.status))
        return new_cls


class BaseMagic(metaclass=MetaMagic):
    def __init__(self):
        instance_var = {name: copy.deepcopy(
            value) for name, value in self._variables.items()}
        self._variables = instance_var

        self._all_variables = self._variables.copy()

        self._variables = instance_var
        for key, value in self._variables.items():
            setattr(self, key, value)

    def link_to(self, parent):
        parent._all_variables.update(self._all_variables)
