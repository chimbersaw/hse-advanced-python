import copy

import numpy as np


class Matrix:
    def __init__(self, data=None):
        if data is None or len(data) == 0:
            raise ValueError("Matrix cannot be empty")
        lens = [len(row) for row in data]
        if lens[0] == 0 or lens.count(lens[0]) < len(lens):
            raise ValueError("Matrix must be nonempty and rectangular")
        self._data = copy.deepcopy(data)

    def dims(self):
        return len(self._data), len(self._data[0])

    def _check_equal_dims(self, other):
        if self.dims() != other.dims():
            raise ValueError("Matrix dimensions must be equal")

    def __add__(self, other):
        """
        :type other: Matrix
        :rtype Matrix
        """
        self._check_equal_dims(other)
        n, m = self.dims()
        return Matrix([[self._data[i][j] + other._data[i][j] for j in range(m)] for i in range(n)])

    def __mul__(self, other):
        """
        :type other: Matrix
        :rtype Matrix
        """
        self._check_equal_dims(other)
        n, m = self.dims()
        return Matrix([[self._data[i][j] * other._data[i][j] for j in range(m)] for i in range(n)])

    def __matmul__(self, other):
        """
        :type other: Matrix
        :rtype Matrix
        """
        if self.dims()[1] != other.dims()[0]:
            raise ValueError("First matrix #cols must be equal to #rows in second matrix during matmul.")
        n, m = self.dims()
        _, k = other.dims()
        res = Matrix([[0] * m for _ in range(n)])
        for i in range(n):
            for j in range(k):
                for k in range(m):
                    res._data[i][j] += self._data[i][k] * other._data[k][j]
        return res


def save_to_file(matrix, path):
    pass


def main():
    np.random.seed(0)
    a = Matrix(np.random.randint(0, 10, (10, 10)))
    b = Matrix(np.random.randint(0, 10, (10, 10)))
    save_to_file(a + b, "artifacts/easy/matrix+.txt")
    save_to_file(a * b, "artifacts/easy/matrix+.txt")
    save_to_file(a @ b, "artifacts/easy/matrix+.txt")


if __name__ == "__main__":
    main()
