import copy
from typing import Optional

class MatrixError(Exception):
    def __init__(self, matrix1, matrix2):
        self.matrix1 = matrix1
        self.matrix2 = matrix2

class Matrix:
    def __init__(self, data):
        self.data = copy.deepcopy(data)

    def __eq__(self, other):
        return self.data == other.data

    def __str__(self):
        result = ''
        for i in self.data:
            i = map(str, i)
            l = '\t'.join(i)
            result += l + '\n'
        s = result.strip()
        return s

    def size(self):
        i = len(self.data)
        j = len(self.data[0])
        return f'{i} x {j}'

    def __add__(self, other):
        if self.size() != other.size():
            raise MatrixError(self, other)
        res = copy.deepcopy(self.data)
        for i in range(len(other.data)):
            for j in range(len(other.data[i])):
                res[i][j] += other.data[i][j]
        return Matrix(res)

    def __mul__(self, other):
        ress = copy.deepcopy(self.data)
        new = []
        line = []
        if isinstance(other, (int, float)):
            for i in range(len(ress)):
                for j in range(len(ress[i])):
                    ress[i][j] = ress[i][j] * other
            return Matrix(ress)
        elif isinstance(other, Matrix):
            if len(self.data[0]) != len(other.data):
                raise MatrixError(self, other)
            else:
                for i in range(0, len(ress)):
                    for j in range(0, len(other.data[0])):
                        sum = 0
                        for l in range(0, len(ress[0])):
                            sum += ress[i][l] * other.data[l][j]
                        line.append(sum)
                    new.append(line)
                    line = []
            return Matrix(new)
    __rmul__ = __mul__

    def transpose(self):
        M = []
        n = []
        for j in range(0, len(self.data[0])):
            for i in range(0, len(self.data)):
                n.append(self.data[i][j])
            M.append(n)
            n = []
        self.data = M
        return self

    def __pow__(self, pow):
        if self.data == [[]]:
            return self
        if isinstance(self, Matrix):
            if len(self.data[0]) != len(self.data):
                raise MatrixError(self, pow)
            elif len(self.data[0]) == len(self.data):
                if pow == 0:
                    ress = copy.deepcopy(self.data)

                    for i in range(0, len(ress)):
                        for j in range(0, len(ress[0])):
                            if i == j:
                                ress[i][j] = 1
                            else:
                                ress[i][j] = 0

                    return Matrix(ress)
                elif pow == 1:
                    return self
                elif pow % 2 == 0:
                    m = self.__pow__(pow / 2)
                    return m * m
                else:
                    m = self.__pow__(pow - 1) * self
                    return m

def parse_matrix(text: str) -> Optional[Matrix]:
    try:
        M = eval(text)
    except Exception:
        return None


    if isinstance(M, int):
        M = int(M)
        return M

    if isinstance(M, list):
        for i in range(0, len(M) - 1):
            if isinstance(M[i], list) and isinstance(M[i + 1], list):
                if len(M[i]) == len(M[i+1]) and len(M) > 1:
                    return Matrix(eval(text))
    if len(M) == 1 and isinstance(M[0], list):
        return Matrix(eval(text))

    return None
