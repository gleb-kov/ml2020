import math

import numpy
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.tree import DecisionTreeClassifier


def classify(h):
    return 1 if h >= 0 else -1


def predict(model, entry):
    return sum([alpha * tree.predict([entry])[0] for tree, alpha in model])


def calculate_accuracy(model, x, y):
    accuracy = 0
    D = len(y)
    for idx in range(D):
        h = predict(model, x.iloc[idx])
        if classify(h) == y.iloc[idx]:
            accuracy += 1
    return accuracy / len(y)


def draw_plots(legend, model, x, y):
    x_tp, y_tp = [], []
    x_tn, y_tn = [], []

    x_fp, y_fp = [], []
    x_fn, y_fn = [], []

    D = len(y)
    for idx in range(D):
        h = predict(model, x.iloc[idx])
        if classify(h) == y.iloc[idx]:
            if y.iloc[idx] == 1:
                x_tp.append(x['x'][idx])
                y_tp.append(x['y'][idx])
            else:
                x_tn.append(x['x'][idx])
                y_tn.append(x['y'][idx])
        else:
            if y.iloc[idx] == 1:
                x_fn.append(x['x'][idx])
                y_fn.append(x['y'][idx])
            else:
                x_fp.append(x['x'][idx])
                y_fp.append(x['y'][idx])

    plt.scatter(x_tp, y_tp, color=['red'], label="right 1")
    plt.scatter(x_tn, y_tn, color=['blue'], label="right -1")

    plt.scatter(x_fp, y_fp, color=['red'], marker='s', label="wrong 1")
    plt.scatter(x_fn, y_fn, color=['blue'], marker='s', label="wrong -1")

    plt.legend(loc="upper right", title='Classes')
    plt.savefig("plots/" + legend + '.png')
    plt.close()

def process_dataset(filename, steps=56):
    dataset = pd.read_csv(filename)

    D = len(dataset)
    w = pd.array([1 / D] * D)
    x = dataset.drop(columns='class')
    dataset['class'] = dataset['class'].apply(lambda x: 1 if x == 'P' else -1)
    y = dataset['class']

    accuracy = []
    model = []

    for step in range(1, steps):
        tree = DecisionTreeClassifier(max_depth=4)
        tree.fit(x, y, sample_weight=w)

        prediction = tree.predict(x)

        error = sum(w * [x != 0 for x in prediction - y])
        alpha = 1 / 2 * math.log((1 - error) / error)
        for j in range(D):
            w[j] *= math.exp(-alpha * y[j] * prediction[j])
        norm = sum(w)
        for j in range(D):
            w[j] /= norm

        model.append((tree, alpha))
        accuracy.append(calculate_accuracy(model, x, y))
        print(accuracy[-1], len(accuracy))

        if step in [1, 2, 3, 5, 8, 13, 21, 34, 55]:
            draw_plots(f"{filename[:-4]}_{step}", model, x, y)

    plt.plot(accuracy, 'g')
    plt.grid(True)
    plt.xlabel("steps")
    plt.ylabel("accuracy")
    plt.savefig("plots/" + filename[:-4] + '_accuracy.png')
    plt.close()


def main():
    process_dataset('chips.csv')
    process_dataset('geyser.csv')


if __name__ == '__main__':
    main()
