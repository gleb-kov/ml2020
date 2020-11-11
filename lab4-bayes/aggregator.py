import os
import pandas as pd
from matplotlib import pyplot as plt

def compare_files(lhs, rhs):
    lres = []
    rres = []
    with open(lhs, 'r') as lfd:
        lres = lfd.readlines()
    with open(rhs, 'r') as rfd:
        rres = rfd.readlines()
    if len(lres) != len(rres):
        raise ValueError("Invalid files comparing")

    part = []

    for i in range(len(lres)):
        part.append([float(rres[i]), int(lres[i])])

    return part


def main(home_path):
    ans_path = home_path + "answers"
    bayes_output = home_path + "bayes_output"

    pred_list = [] # real class and prediction
    m_minus = 0
    m_plus = 0

    for _, _, files in os.walk(ans_path):
        for filename in files:
            lhs_name = ans_path + '/' + filename
            rhs_name = bayes_output + '/' + filename

            pred_list = compare_files(lhs_name, rhs_name)
            
            #fpr += cm[0][1] / (cm[0][1] + cm[1][1])
            #tpr += cm[0][0] / (cm[0][0] + cm[1][0])
            #accuracy += (cm[0][0] + cm[1][1]) / (sum(cm[0]) + sum(cm[1]))

    fpr = 0.0
    tpr = 0.0

    trust_level = 0.5

    accuracy = 0

    pred_list.sort(reverse=True)
    for item in pred_list:
        if item[1] == 1:
            m_minus += 1
        else:
            m_plus += 1 
   
    x = [0.0]
    y = [0.0]
    for item in pred_list:
        if item[1] == 1:
            fpr += 1.0 / m_minus
            if item[0] < trust_level:
                accuracy += 1
        else:
            tpr += 1.0 / m_plus
            if item[0] >= trust_level:
                accuracy += 1
        x.append(fpr)
        y.append(tpr)
    
    
    print("Accuracy", accuracy / (m_minus + m_plus))

    pdx = pd.DataFrame(data={'fpr': x})
    pdy = pd.DataFrame(data={'tpr': y})
    plt.scatter(pdx, pdy)
    plt.show() 

if __name__ == "__main__":
    home_path = "/home/gleb/github/ml2020/lab4-bayes/"
    main(home_path)

