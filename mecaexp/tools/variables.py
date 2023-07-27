import numpy as np
from enum import Enum

MathType = Enum("MathType", ["Scalar", "Tensor1",
                "Tensor2", "Tensor3", "Tensor4"])
VarStatus = Enum("VarType", ["Vin", "Vout", "Vint", "Vaux"])

ARRAY_SHAPE = {MathType.Scalar: (1, 1), MathType.Tensor1: (3,), MathType.Tensor2: (
    3, 3), MathType.Tensor3: (3, 3, 3), MathType.Tensor4: (3, 3, 3, 3)}


class StateVariable:
    __slots__ = ("_name", "_value", "_rate", "_type", "_status", "_start_pos", "_size", "_shape")

    def __init__(self, math_type_: MathType, var_type_: VarStatus):
        self._name = ""
        self._value = None
        self._rate = None
        # self._ini = None
        self._type = math_type_
        self._status = var_type_
        self._start_pos = None
        self._size = None
        self._shape = None

        self.initialize()

    def shape(self):
        return self._shape

    def size(self):
        return self._size

    def initialize(self):
        shape = ARRAY_SHAPE[self._type]
        self._size = np.prod(shape)
        self._shape = shape
        # self._ini = np.zeros(shape)
        self._value = np.zeros(shape)
        self._rate = np.zeros(shape)

    @property
    def start_pos(self):
        return self._start_pos

    @start_pos.setter
    def start_pos(self, idx):
        self._start_pos = idx

    @property
    def status(self):
        return self._status

    @property
    def type(self):
        return self._type

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, n):
        self._name = n

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, x):
        if self._type == MathType.Scalar:
            assert(isinstance(x, float) or isinstance(x, int) or isinstance(x, np.ndarray))
        elif self._type == MathType.Tensor2:
            assert(x.shape[0] == 3 and x.shape[1] == 3)
        elif self._type == MathType.Tensor3:
            assert(x.shape[0] == 3 and x.shape[1] == 3 and x.shape[2] == 3)
        elif self._type == MathType.Tensor4:
            assert(x.shape[0] == 3 and x.shape[1] ==
                   3 and x.shape[2] == 3 and x.shape[3] == 3)

        self._value = x

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, x):
        if self._type == MathType.Scalar:
            assert(isinstance(x, float) or isinstance(x, int) or isinstance(x, np.ndarray))
        elif self._type == MathType.Tensor2:
            assert(x.shape[0] == 3 and x.shape[1] == 3)
        elif self._type == MathType.Tensor3:
            assert(x.shape[0] == 3 and x.shape[1] == 3 and x.shape[2] == 3)
        elif self._type == MathType.Tensor4:
            assert(x.shape[0] == 3 and x.shape[1] ==
                   3 and x.shape[2] == 3 and x.shape[3] == 3)

        self._rate[:] = x

    def fill_value_from_vector(self, y: np.ndarray) -> None:
        self.value = y[self._start_pos:self._start_pos+self._size].reshape( self.shape() )

    def fill_vector_from_rate(self, y: np.ndarray) -> None:
        y[self._start_pos:self._start_pos+self._size] = self._rate.ravel()

        