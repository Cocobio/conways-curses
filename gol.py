import numpy as np
from collections.abc import Sequence


class GOL:
    def __init__(self, dims=(5, 5)):
        if not isinstance(dims, Sequence) or len(dims) < 2:
            raise ValueError("dims debe ser un iterable de largo a lo menos 2")

        self._N = dims[0]
        self._M = dims[1]
        self.gen = np.random.randint(0, 2, (self._N, self._M), dtype=np.int8)
        self.buffer = np.copy(self.gen)
        self.old_gen = np.zeros(self.gen.shape, dtype=np.int8)

    def next_gen(self):
        for i in range(self._N):
            for j in range(self._M):
                neig = sum(self.gen[ii % self._N][jj % self._M]
                           for ii in range(i-1, i+2)
                           for jj in range(j-1, j+2))
                neig -= self.gen[i][j]

                if self.gen[i][j]:
                    if neig < 2 or neig > 3:
                        self.buffer[i][j] = 0
                else:
                    if neig == 3:
                        self.buffer[i][j] = 1

        np.copyto(self.old_gen, self.gen)
        np.copyto(self.gen, self.buffer)

    def __repr__(self):
        return self.gen.__repr__()

    def __str__(self):
        return self.gen.__str__()

    @property
    def width(self):
        return self._N

    @property
    def height(self):
        return self._M
