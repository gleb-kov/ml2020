import random
import math
from matplotlib import pyplot as plt

###############################################################################

def clamp(v, lo, hi):
    if v <= lo and v <= hi:
        return min(hi, lo)
    if hi <= v and lo <= v:
        return max(hi, lo)
    return v
 
def tricky_rand(i, m):
    candidate = i
    while candidate == i:
        candidate = random.randint(0, m - 1)
    return candidate

def predict(k, y, a, b):
    n = len(k)
    p = []
    for i in range(n):
        res = b
        for j in range(n):
            res += a[j] * y[j] * k[j][i]
        p.append(res)
    return p

def prec(k, y, a, b):
    p = predict(k, y, a, b)
    n, errors = len(k), 0
    for i in range(n):
        if p[i] * y[i] < 0:
            errors += 1
    return 1 - errors / n
 
# k[i][j] = kernel(i, j)
# y = classes
# c = 
# max_passes = iter limit
# tol = tolerance hyper-param
def smo(k, y, c, max_passes, tol = -1e-8, enable_pred = False, pred_period = 100, pred_ratio = 0.05):
    n = len(k)
 
    def f(k, y, a, ind):
        res = b
        for i in range(n):
            res += a[i] * y[i] * k[i][ind]
        return res
 
    def L(y, a, i, j):
        if y[i] != y[j]:
            return max(0.0, a[j] - a[i])
        return max(0.0, a[i] + a[j] - c)
 
    def H(y, a, i, j):
        if y[i] != y[j]:
            return min(c, c + a[j] - a[i])
        return min(c, a[i] + a[j])
 
    a = [0.0] * n
    b = 0.0
 
    best_pred = n + n
    best_a, best_b = a, b
 
    for passes in range(max_passes):
        for i in range(n):
            e_i = f(k, y, a, i) - y[i]
            if (y[i] * e_i < -tol and a[i] < c) or (y[i] * e_i > tol and a[i] > 0):
                j = tricky_rand(i, n)
                e_j = f(k, y, a, j) - y[j]
                a_i_old, a_j_old = a[i], a[j]
                l, h = L(y, a, i, j), H(y, a, i, j)
                if l == h:
                    continue
                eta = 2 * k[i][j] - k[i][i] - k[j][i]
                if eta >= 0:
                    continue
                a[j] -= y[j] * (e_i - e_j) / eta
                a[j] = clamp(a[j], l, h)
                if abs(a[j] - a_j_old) < 1e-5:
                    continue
                a[i] += y[i] * y[j] * (a_j_old - a[j])
                b1 = b - e_i - y[i] * (a[i] - a_i_old) * k[i][i] - y[j] * (a[j] - a_j_old) * k[i][j]
                b2 = b - e_j - y[i] * (a[i] - a_i_old) * k[i][j] - y[j] * (a[j] - a_j_old) * k[j][j]
                if 0 < a[i] < c:
                    b = b1
                elif 0 < a[j] < c:
                    b = b2
                else:
                    b = (b1 + b2) / 2

        if enable_pred and passes % pred_period == 0:
                p = prec(k, y, a, b)
                if p > best_pred:
                    best_pred = p
                    best_a, best_b = a, b
                if p >= pred_ratio:
                    return best_a, best_b
 
    if enable_pred:
        p = prec(k, y, a, b)
        if p > best_pred:
            best_pred = p
            best_a, best_b = a, b

    if enable_pred:
        return best_a, best_b
    return a, b

###############################################################################

def poly_kernel(x1, x2, d = 2, add = 0):
    res = 0.0
    for i in range(len(x1)):
        res += x1[i] * x2[i]
    return (res + add) ** d

def exp_kernel(x1, x2, b = 1):
    norm = 0.0
    for i in range(len(x1)):
        norm += (x1[i] - x2[i]) ** 2
    norm = math.sqrt(norm)
    return math.exp(-b * norm)

def square_kernel(x1, x2):
    return poly_kernel(x1, x2)

def build_kernel_matrix(params, kernel):
    n = len(params)
    k = []
    for i in range(n):
        k_i = []
        for j in range(n):
            k_i.append(kernel(params[i], params[j]))
        k.append(k_i)
    return k

###############################################################################

def build_plot(params, values, label_suffix, plt_title="Labels"):
    x_n, x_p = [], []
    y_n, y_p = [], []
    for i in range(len(values)):
        if values[i] <= 0:
            x_n.append(params[i][0])
            y_n.append(params[i][1])
        else:
            x_p.append(params[i][0])
            y_p.append(params[i][1])
    plt.scatter(x_n, y_n, color=['blue'], label='$N_{{' + label_suffix + '}}$')
    plt.scatter(x_p, y_p, color=['red'], label='$P_{{' + label_suffix + '}}$')
    plt.legend(title=plt_title)
    plt.show()

###############################################################################

def main():
    filename = "chips.csv" #'geyser.csv'

    params, values = [], []
    with open(filename) as fp:
        columns = fp.readline()
        for line in fp:
            item = line.split(',')
            p = list(map(float, item[:-1]))
            params.append(p)
            if item[-1][0] == 'P':
                values.append(-1)
            else:
                values.append(1)

    k = build_kernel_matrix(params, square_kernel)
    build_plot(params, values, 'real', 'Real classes')
    a, b = smo(k, values, 5.0, 200)
    p = predict(k, values, a, b)
    build_plot(params, p, 'predict', 'Predicted classes')

    print(prec(k, values, a, b))

if __name__ == "__main__":
    main()
