from easy import Matrix, save_to_file


class HashMixin:
    def __hash__(self):
        """Alternating sign sum of matrix elements"""
        res, sgn = 0, 1
        for row in self._data:
            for elem in row:
                res += elem * sgn
                sgn *= -1
        return res


class HashableMatrix(Matrix, HashMixin):
    _matmul_cache = {}

    @classmethod
    def invalidate_caches(cls):
        cls._matmul_cache = {}

    def __matmul__(self, other):
        key = hash(self), hash(other)
        if key not in HashableMatrix._matmul_cache:
            HashableMatrix._matmul_cache[key] = HashableMatrix(super().__matmul__(other)._data)
        return HashableMatrix._matmul_cache[key]


def main():
    a = HashableMatrix([[1, 1], [1, 1]])
    b = HashableMatrix([[1, 2], [3, 4]])
    c = HashableMatrix([[2, 2], [2, 2]])
    d = HashableMatrix([[1, 2], [3, 4]])

    assert hash(a) == hash(c)

    ab = a @ b
    HashableMatrix.invalidate_caches()  # otherwise, we use cached version
    cd = c @ d

    prefix = "artifacts/hard"
    save_to_file(a, f"{prefix}/A.txt")
    save_to_file(b, f"{prefix}/B.txt")
    save_to_file(c, f"{prefix}/C.txt")
    save_to_file(d, f"{prefix}/D.txt")
    save_to_file(ab, f"{prefix}/AB.txt")
    save_to_file(cd, f"{prefix}/CD.txt")
    with open(f"{prefix}/hash.txt", "w") as file:
        file.write(str(hash(ab)) + "\n" + str(hash(cd)) + "\n")


if __name__ == "__main__":
    main()
