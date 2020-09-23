import pandas as pd
from matplotlib import pyplot as plt
from knn import non_param_reg
from fscore import calc_fscore
import math

###############################################################################

## Config
filename = 'seeds.csv'
target = [11.26,13.01,0.8355,5.186,2.71,5.335,5.092]
#target = [13.94,14.17,0.8728,5.585,3.15,2.124,5.012]
#target = [20.97,17.25,0.8859,6.563,3.991,4.677,6.316]
classes = 3

###############################################################################

def minmax(dataset, hidden = 0):
    minmax = list()
    for i in range(len(dataset[0])):
        if i == len(dataset[0]) - hidden:
            continue
        value_min = dataset[:, i].min()
        value_max = dataset[:, i].max()
        minmax.append([value_min, value_max])
    return minmax

def normalize(dataset, minmax, hidden = 0):
    result = []
    for row in dataset:
        result.append([])
        for i in range(len(row)):
            cc = row[i]
            if i < len(row) - hidden:
                cc = float(float(row[i] - minmax[i][0]) / float(minmax[i][1] - minmax[i][0]))
            result[-1].append(cc)
    return result

def get_column(dataset, num):
    result = []
    for row in dataset:
        result.append(row[num])
    return result

###############################################################################

def draw_plot(dataset, feature1N, feature2N, target):
    class_to_color = {
        1: "green",
        2: "blue",
        3: "red",
    }

    values = get_column(dataset, -1)

    colored_classes = list(map(lambda x: class_to_color[x], values))
    colored_classes.append("r")

    x = get_column(dataset, feature1N)
    y = get_column(dataset, feature2N)

    x.append(target[feature1N])
    y.append(target[feature2N])

    plt.scatter(x, y, c=colored_classes)
    plt.show()

###############################################################################

def fscore(dataset, classes, map_predict, distStr, kernelStr, windowStr, window):
    cm = []
    for i in range(classes):
        cm.append([0]*classes)

    for i in range(len(dataset)):
        predict = non_param_reg(dataset[:i] + dataset[i+1:], len(dataset[0]) - 1, dataset[i], distStr, kernelStr, windowStr, window)
        predict = map_predict(predict)
        cm[predict - 1][int(dataset[i][-1]) - 1] += 1
    return calc_fscore(cm)

def fscore_step(dataset, classes, score_index, map_predict, distStr, kernelStr, windowStr):
    x = []
    y = []
    for w in range(10):
        fs = fscore(dataset, classes, map_predict, distStr, kernelStr, windowStr, w)
        y.append(fs[score_index])
        x.append(w)
    plt.scatter(x, y)
    plt.show()

def naive_reg(dataset, target):
    distStr = "euclidean"
    kernelStr = "logistic"
    windowStr = "variable"
    window = 5

    def map_predict(p):
        p = round(p)
        p = max(p, 1)
        p = min(p, classes)
        return p

    predict = non_param_reg(dataset, len(dataset[0]) - 1, target, distStr, kernelStr, windowStr, window)
    predict = map_predict(predict)
    fscore_step(dataset, classes, 0, map_predict, distStr, kernelStr, windowStr)
    fscore_step(dataset, classes, 1, map_predict, distStr, kernelStr, windowStr)
    print("Naive regression: class# ", predict)

def onehot_reg(dataset, target):
    distStr = "euclidean"
    kernelStr = "logistic"
    windowStr = "variable"
    window = 5

    def map_predict(p):
        p = round(p)
        p = max(p, 1)
        p = min(p, classes)
        return p

    best = 1
    best_predict = 0
    newdata = []
    for row in dataset:
        newdata.append(row[:-1])

    last = get_column(dataset, -1)

    for i in range(len(newdata)):
        for c in range(1, classes+1):
            newdata[i].append(0)
            if last[i] == c:
                newdata[i][-1] = 1

    columns = len(newdata[0])

    for c in range(1, classes+1):
        predict = non_param_reg(newdata, columns - c, target, distStr, kernelStr, windowStr, window)
        if predict > best_predict:
            best_predict = predict
            best = classes + 1 - c
    #fscore_step(newdata, classes, map_predict, distStr, kernelStr, windowStr)
    print("Onehot regression: class# ", best, " prediction: ", predict)

def main():
    dataset = pd.read_csv(filename)
    min_max = minmax(dataset.values)
    dataset = normalize(dataset.values, min_max, 1)

    norm_target = target.copy()
    norm_target = normalize([norm_target], min_max)
    norm_target = norm_target[0]

    naive_reg(dataset, norm_target)
    onehot_reg(dataset, norm_target)

if __name__ == "__main__":
    main()
