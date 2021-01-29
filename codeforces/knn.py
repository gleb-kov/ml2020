import math
 
## distance
 
def manhattan(v1, v2):
    dist = 0;
    for i in range(len(v1)):
        dist += abs(v1[i] - v2[i])
    return dist;
 
def euclidean(v1, v2):
    dist = 0;
    for i in range(len(v1)):
        dist += (v1[i] - v2[i]) ** 2
    return math.sqrt(dist)
 
def chebyshev(v1, v2):
    dist = 0;
    for i in range(len(v1)):
        dist = max(dist, abs(v1[i] - v2[i]))
    return dist
 
def evalDist(name):
    if name == "manhattan":
        return manhattan
    if name == "euclidean":
        return euclidean
    if name == "chebyshev":
        return chebyshev
 
## kernels
 
def uniform(d):
    return 0 if d <= -1 or 1 <= d else 0.5
 
def triangular(d):
    return 0 if d <= -1 or 1 <= d else 1 - abs(d)
 
def epanechnikov(d):
    return 0 if d <= -1 or 1 <= d else 0.75 * (1 - d * d)
 
def quartic(d):
    h = (1 - d * d)
    return 0 if d <= -1 or 1 <= d else 15.0 * h * h / 16.0
 
def triweight(d):
    h = 1 - d * d
    return 0 if d <= -1 or 1 <= d else 35.0 * h * h * h / 32.0
 
def tricube(d):
    h1 = abs(d)
    h2 = 1.0 - h1 ** 3
    return 0 if d <= -1 or 1 <= d else 70.0 * h2 * h2 * h2 / 81.0
 
def gaussian(d):
    s = math.sqrt(2.0 * math.pi)
    return math.exp(-0.5 * d * d) / s
 
def cosine(d):
    return 0 if d <= -1 or 1 <= d else math.pi * math.cos(math.pi * d / 2.0) / 4.0
 
def logistic(d):
    return 1.0 / (math.exp(d) + 2.0 + math.exp(-d))
 
def sigmoid(d):
    return 2.0 / (math.pi * (math.exp(d) + math.exp(-d)))
 
 
def evalKernel(name):
    if name == "uniform":
        return uniform
    if name == "triangular":
        return triangular
    if name == "epanechnikov":
        return epanechnikov
    if name == "quartic":
        return quartic
    if name == "triweight":
        return triweight
    if name == "tricube":
        return tricube
    if name == "gaussian":
        return gaussian
    if name == "cosine":
        return cosine
    if name == "logistic":
        return logistic
    if name == "sigmoid":
        return sigmoid
 
def nonParamReg(dataset, query, distStr, kernelStr, windowStr, window):
    n = len(dataset)
    params = []
    values = []
    for row in dataset:
        params.append(row[:-1])
        values.append(row[-1])
 
    dist = evalDist(str(distStr))
    kernel = evalKernel(str(kernelStr))
    window = float(window)
 
    aggr = []
    for i in range(n):
        aggr.append((dist(params[i], query), values[i]))
    aggr.sort()
 
    if str(windowStr) != "fixed":
        window = aggr[int(window)][0]
 
    topsum = 0
    botsum = 0
    total = 0
    eps = 1e-7
    if window < eps:
        for p in aggr:
            total += p[1]
            if p[0] < eps:
                tmp = kernel(0.0)
                topsum += tmp * p[1]
                botsum += tmp
    else:
        for p in aggr:
            total += p[1]
            topsum += kernel(p[0] / window) * p[1]
            botsum += kernel(p[0] / window)
 
    res = total / n
    if abs(botsum) > eps:
        res = topsum / botsum
    return res
 
def main():
    n, m = map(int, input().split())
    
    dataset = []
    
    for i in range(n):
        row = list(map(int, input().split()))
        dataset.append(row)
 
    query = list(map(int, input().split()))
    distStr = str(input())
    kernelStr = str(input())
    windowStr = str(input())
    window = float(input())
 
    res = nonParamReg(dataset, query, distStr, kernelStr, windowStr, window)
 
    print(res)
 
if __name__ == "__main__":
    main()
