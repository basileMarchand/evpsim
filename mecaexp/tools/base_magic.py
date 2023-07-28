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
    def __init__(self, rename=None):
        self._instance_var = {name: copy.deepcopy(
            value) for name, value in self._variables.items()}
        for key, value in self._instance_var.items():
            setattr(self, key, value)

        if rename:
            for key, value in rename.items():
                var = self._instance_var[key]
                var.name = value
                self._instance_var[value] = var
                del self._instance_var[key]

        self._all_variables = self._instance_var.copy()

    def link_to(self, parent):
        for key in self._all_variables.keys():
            if key in parent._all_variables.keys():
                raise Exception(
                    "A variable {key} already registered in {parent}, you need to rename it I thing")
        parent._all_variables.update(self._all_variables)
