import random
 
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
 
def prec(k, y, a, b):
    n = len(k)
    errors = 0
    for i in range(n):
        res = b
        for j in range(n):
            res += a[j] * y[j] * k[j][i]
        if y[i] * res < 0:
            errors += 1
    return errors
 
# k[i][j] = kernel(i, j)
# y = classes
# c = 
# max_passes = iter limit
# tol = tolerance hyper-param
def smo(k, y, c, max_passes, tol, enable_prec, prec_period, prec_ratio):
    n, m = len(k), len(k[0])
 
    def f(k, y, a, ind):
        res = b
        for i in range(m):
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
 
    a = [0.0] * m
    b = 0.0
 
    best_prec = n + n
    best_a, best_b = a, b
 
    for passes in range(max_passes):
        for i in range(m):
            e_i = f(k, y, a, i) - y[i]
            if (y[i] * e_i < -tol and a[i] < c) or (y[i] * e_i > tol and a[i] > 0):
                j = tricky_rand(i, m)
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
        if enable_prec and passes % prec_period == 0:
                p = prec(k, y, a, b)
                if p < best_prec:
                    best_prec = p
                    best_a, best_b = a, b
                if p <= prec_ratio * n:
                    return best_a, best_b
 
    if enable_prec:
        p = prec(k, y, a, b)
        if p < best_prec:
            best_prec = p
            best_a, best_b = a, b
    if enable_prec:
        return best_a, best_b
    return a, b
 
def acc(a, y):
    n = len(a)
    delta = 0.0
    for i in range(n):
        delta += a[i] * y[i]
    return delta
 
def main():
    n = int(input())
    coef = [] # [[]]
    values = []
    for i in range(n):
        item = list(map(int, input().split()))
        coef.append(item[:-1])
        values.append(item[-1])
    c = float(input())
    a, b = smo(coef, values, c, 20000, -1e-8, True, 100, 0.04)
 
    tol = 100000000
    aint = []
    for i in range(n):
        aint.append(round(a[i] * tol))
    delta = acc(aint, values)
 
    for i in range(n):
        dd = aint[i] - delta * values[i]
        if 0 <= dd and dd <= c * tol:
            aint[i] = dd
            delta = 0
            break
        if aint[i] < 0 and aint[i] > c * tol:
            raise Exception("unbeliavable")
    if delta != 0:
        raise Exception("unbeliavable")
 
    for i in range(n):
        print(format(1.0 * aint[i] / tol, ".8f"))
    print(format(b, ".8f"))
    print(prec(coef, values, a, b))
 
if __name__ == "__main__":
    main()
