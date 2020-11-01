import copy
import math
 
 
class MatrixHelpers:
    @staticmethod
    def mul(lhs, rhs):
        data = []
        for i in range(lhs.rows):
            data.append([0] * rhs.cols)
        for i in range(lhs.rows):
            for j in range(rhs.cols):
                for k in range(lhs.cols):
                    data[i][j] += lhs.data[i][k] * rhs.data[k][j]
        return data
 
    @staticmethod
    def transpose(m):
        data = []
        for i in range(m.cols):
            line = []
            for j in range(m.rows):
                line.append(m.data[j][i])
            data.append(line)
        return Matrix(0, 0, data)
 
    @staticmethod
    def read(rows):
        return [list(map(float, input().split())) for _ in range(rows)]
 
    @staticmethod
    def show(data):
        for row in data:
            print(" ".join(map(str, row)))
 
 
class Graph:
    def __init__(self):
        self.nodes = []
 
    def add_node(self, node):
        self.nodes.append(node)
 
 
class Matrix:
    def __init__(self, rows, cols, data=None):
        if data is None:
            self.rows, self.cols = rows, cols
            self.data = []
            for r in range(rows):
                self.data.append([0] * cols)
        else:
            self.data = data
            self.update_state()
 
    def add(self, rhs):
        for i in range(self.rows):
            for j in range(self.cols):
                self.data[i][j] += rhs[i][j]
 
    def naive_mul(self, rhs):
        for i in range(self.rows):
            for j in range(self.cols):
                self.data[i][j] *= rhs[i][j]
 
    def get(self, r, c):
        return self.data[r][c]
 
    def set(self, r, c, val):
        self.data[r][c] = val
 
    def get_row(self, r):
        return self.data[r]
 
    def update_state(self):
        self.rows = len(self.data)
        if self.rows == 0:
            self.cols = 0
        else:
            self.cols = len(self.data[0])
 
    def copy(self):
        return copy.deepcopy(self.data)
 
    def read(self):
        self.data = MatrixHelpers.read(self.rows)
        self.update_state()
 
 
class Node:
    def __init__(self):
        super().__init__()
        self.df = []
        self.dfc = None
        self.rows, self.cols = None, None
 
    def calc_df(self):
        if self.dfc:
            return
        self.dfc = Matrix(self.rows, self.cols)
        for df_i in self.df:
            self.dfc.add(df_i)
 
 
class Var(Node):
    def __init__(self, rows, cols):
        super().__init__()
        self.m = Matrix(rows, cols)
        self.rows, self.cols = rows, cols
 
    def read(self):
        self.m.read()
 
    def calc(self):
        pass
 
    def calc_back(self):
        self.calc_df()
 
 
class Tnh(Node):
    def __init__(self, x):
        super().__init__()
        self.x = x
        self.rows, self.cols = x.rows, x.cols
 
    def calc(self):
        data = list(map(lambda row: list(map(math.tanh, row)), self.x.m.data))
        self.m = Matrix(0, 0, data)
 
    def calc_back(self):
        self.calc_df()
 
        result = self.dfc.copy()
        for i in range(self.rows):
            for j in range(self.cols):
                x = self.m.data[i][j]
                result[i][j] *= 1 - x * x
        self.x.df.append(result)
 
 
class Rlu(Node):
    def __init__(self, alpha, x):
        super().__init__()
        self.alpha, self.x = alpha, x
        self.rows, self.cols = x.rows, x.cols
 
    def calc(self):
        data = []
        for row in self.x.m.data:
            data.append(list(map(lambda x: self.alpha * x if x < 0 else x, row)))
        self.m = Matrix(self.rows, self.cols, data)
 
    def calc_back(self):
        self.calc_df()
 
        result = self.dfc.copy()
        for i in range(self.rows):
            for j in range(self.cols):
                if self.x.m.data[i][j] < 0:
                    result[i][j] *= self.alpha
        self.x.df.append(result)
 
 
class Mul(Node):
    def __init__(self, lhs, rhs):
        super().__init__()
        self.lhs, self.rhs = lhs, rhs
        self.rows, self.cols = lhs.rows, rhs.cols
 
    def calc(self):
        data = MatrixHelpers.mul(self.lhs.m, self.rhs.m)
        self.m = Matrix(0, 0, data)
 
    def calc_back(self):
        self.calc_df()
        self.lhs.df.append(MatrixHelpers.mul(self.dfc, MatrixHelpers.transpose(self.rhs.m)))
        self.rhs.df.append(MatrixHelpers.mul(MatrixHelpers.transpose(self.lhs.m), self.dfc))
 
 
class Sum(Node):
    def __init__(self, ops):
        super().__init__()
        self.ops = ops
        self.rows, self.cols = ops[0].rows, ops[0].cols
 
    def calc(self):
        self.m = Matrix(self.rows, self.cols, self.ops[0].m.copy())
        for op in self.ops[1:]:
            self.m.add(op.m.data)
 
    def calc_back(self):
        self.calc_df()
        for op in self.ops:
            op.df.append(self.dfc.data)
 
 
class Had(Node):
    def __init__(self, ops):
        super().__init__()
        self.ops = ops
        self.rows, self.cols = ops[0].rows, ops[0].cols
 
    def calc(self):
        self.m = Matrix(self.rows, self.cols, self.ops[0].m.copy())
        for op in self.ops[1:]:
            self.m.naive_mul(op.m.data)
 
    def calc_back(self):
        self.calc_df()
        for i in range(len(self.ops)):
            data = self.dfc.copy()
            for j in range(len(self.ops)):
                if i == j:
                    continue
                for r in range(self.rows):
                    for c in range(self.cols):
                        data[r][c] *= self.ops[j].m.data[r][c]
            self.ops[i].df.append(data)
 
 
def main():
    n, m, k = map(int, input().split())
    nodes = []
 
    for i in range(n):
        query = input().split()
        op = query[0]
        query = list(map(int, query[1:]))
 
        if op == 'var':
            nodes.append(Var(query[0], query[1]))
        elif op == 'tnh':
            nodes.append(Tnh(nodes[query[0] - 1]))
        elif op == 'rlu':
            nodes.append(Rlu(1 / query[0], nodes[query[1] - 1]))
        elif op == 'mul':
            nodes.append(Mul(nodes[query[0] - 1], nodes[query[1] - 1]))
        elif op == 'sum':
            nodes.append(Sum([nodes[q - 1] for q in query[1:]]))
        elif op == 'had':
            nodes.append(Had([nodes[q - 1] for q in query[1:]]))
        else:
            raise NotImplemented
 
    for i in range(m):
        nodes[i].read()
 
    for i in range(k):
        node = nodes[n - k + i]
        node.df.append(MatrixHelpers.read(node.rows))
 
    for i in range(n):
        nodes[i].calc()
 
    for i in range(n):
        nodes[-i - 1].calc_back()
 
    for i in range(k):
        MatrixHelpers.show(nodes[n - k + i].m.data)
 
    for i in range(m):
        MatrixHelpers.show(nodes[i].dfc.data)
  
main()

