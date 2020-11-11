import pandas as pd
from matplotlib import pyplot as plt

def main():
    e = -5
    bds = pd.read_csv('broot.csv')
    acc = bds['accuracy']

    lmlist = []
    for i in range(-5, 36):
        lmlist.append(i)

    lam = pd.DataFrame(data={'lambda_legit': lmlist})
    plt.scatter(lam, acc)
    plt.show()

if __name__ == '__main__':
    main()
