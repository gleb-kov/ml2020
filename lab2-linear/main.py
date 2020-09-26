import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from math import sqrt

###############################################################################

def read_file(istream, num):
    params, values = [], []
    for i in range(num):
        item = list(map(int, istream.readline().split()))
        params.append(item[:-1] + [1])
        values.append(item[-1])
    return (np.array(params), np.array(values))

class dataset_holder:
    def __init__(self, istream):
        self.n_params = int(istream.readline()) + 1 # add fake 1 in the end, @see read_file
        self.n_train_items = int(istream.readline())

        train = read_file(istream, self.n_train_items)

        self.train_params = train[0]
        self.train_values = train[1]

        self.n_test_items = int(istream.readline())
        test = read_file(istream, self.n_test_items)

        self.test_params = test[0]
        self.test_values = test[1]

###############################################################################

# loss function
def nrmse(x, y, w):
    return np.sqrt(np.sum(((x @ w) - y) ** 2) / x.shape[0]) / (np.max(y) - np.min(y))

def train_nrmse(dataset, w):
    return nrmse(dataset.train_params, dataset.train_values, w)

def test_nrmse(dataset, w):
    return nrmse(dataset.test_params, dataset.test_values, w)

def l1_norm(w):
    total = 0
    for val in w:
        total += abs(val)
    return total

###############################################################################

# First approach -- least squares with nrmse
# Xw = Y => X^{-1}Xw = X^{-1}Y => w = X^{-1}Y
def least_squares_nrmse(dataset):
    w = np.linalg.pinv(dataset.train_params) @ dataset.train_values
    train_q = train_nrmse(dataset, w)
    test_q = test_nrmse(dataset, w)
    return (train_q, test_q)

# threshold for delta of values
# limit for iterations
def gradient_descent(dataset, threshold, limit):
    train_q, test_q = [], []
    return (train_q, test_q)

def genetic(dataset, threshold, limit):
    def gen_noise(w, iter_num):
        iter_num += 1
        return np.random.uniform(low=0.001, high=1.0, size=(w.shape))
    def add_noise(w, iter_num):
        gen = gen_noise(w, iter_num)
        return np.add(gen, w)

    w = np.zeros(dataset.n_params, dtype=float)
    size = 10 # generation size
    train_q, test_q = [], []

    for i in range(int(limit)):
        best_q = train_nrmse(dataset, w)
        before_iter = best_q
        for j in range(size):
            gen = add_noise(w, i)
            q = train_nrmse(dataset, gen)
            if q < best_q:
                best_q = q
                w = gen
        train_q.append(best_q)
        test_q.append(test_nrmse(dataset, w))
        if abs(before_iter - best_q) < threshold:
            break
    return (train_q, test_q)

###############################################################################

def build_plot():
    plt.xlabel('iterations')
    plt.ylabel('NRMSE')
    plt.legend(title='Set')
    plt.show()

# threshold for delta of values
# limit for iterations
def process(istream, threshold, limit):
    dataset = dataset_holder(istream)

    first_approach = least_squares_nrmse(dataset)
    train_q1 = first_approach[0]
    test_q1 = first_approach[1]
    print("1) Least squares best: ", train_q1, test_q1)
    plt.plot([train_q1] * int(limit), label='train_squares')
    plt.plot([test_q1] * int(limit), label='test_squares')
    build_plot()

#    second_approach = gradient_descent(dataset, threshold, limit)
#    train_q2 = second_approach[0]
#    test_q2 = second_approach[1]
#    print("Gradient best: ", train_q2[-1], test_q2[-1])
#    plt.plot(train_q2, label='train_gradient')
#    plt.plot(test_q2, label='test_gradient')


    third_approach = genetic(dataset, threshold, limit)
    train_q3 = third_approach[0]
    test_q3 = third_approach[1]
    print("3) Genetic best: ", train_q3[-1], test_q3[-1])
    plt.plot(train_q3, label='train_genetic')
    plt.plot(test_q3, label='test_genetic')
    build_plot()

def main():
    with open("1.txt") as istream:
        process(istream, 1e-5, 1e6)

if __name__ == "__main__":
    main()
