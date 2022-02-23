import numpy as np
from numpy.lib.mixins import NDArrayOperatorsMixin


class WriteToFileMixin:
    def save_to_file(self, path):
        with open(path, "w") as file:
            file.write(str(self))


class StrMixin:
    def __str__(self):
        return "[" + ",\n".join(map(lambda row: "[" + ", ".join([str(e) for e in row]) + "]", self.data)) + "]\n"


class GetterSetterMixin:
    def __init__(self):
        self._data = None

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = np.asarray(data)


class Matrix(NDArrayOperatorsMixin, WriteToFileMixin, StrMixin, GetterSetterMixin):
    def __init__(self, data=None):
        super().__init__()
        self.data = np.asarray(data)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get("out", ())

        inputs = tuple(x.data if isinstance(x, Matrix) else x for x in inputs)
        if out:
            kwargs["out"] = tuple(x.data if isinstance(x, Matrix) else x for x in out)
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            return tuple(type(self)(x) for x in result)
        elif method == "at":
            return None
        else:
            return type(self)(result)


def main():
    np.random.seed(0)
    a = Matrix(np.random.randint(0, 10, (10, 10)))
    b = Matrix(np.random.randint(0, 10, (10, 10)))
    prefix = "artifacts/medium/matrix"
    (a + b).save_to_file(f"{prefix}+.txt")
    (a * b).save_to_file(f"{prefix}*.txt")
    (a @ b).save_to_file(f"{prefix}@.txt")


if __name__ == "__main__":
    main()
