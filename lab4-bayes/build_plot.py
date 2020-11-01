import pandas as pd
from matplotlib import pyplot as plt

def main():
    bds = pd.read_csv('broot.csv')
#    print(bds)
#    print(bds['tpr'])
    plt.scatter(bds['fpr'], bds['tpr'])
    plt.show()

if __name__ == '__main__':
    main()
