import os

# returns confusion matrix for pair of files
def compare_files(lhs, rhs):
    lres = []
    rres = []
    with open(lhs, 'r') as lfd:
        lres = lfd.readlines()
    with open(rhs, 'r') as rfd:
        rres = rfd.readlines()
    if len(lres) != len(rres):
        raise ValueError("Invalid files comparing")
    
    cm = [[0, 0], [0, 0]]
    ok, err = 0, 0

    for i in range(len(lres)):
        real_res = int(lres[i].strip()) - 1
        pred_res = int(rres[i].strip()) - 1

#        if real_res == 0 and pred_res == 1:
#            raise ValueError("Found legit letter in spam")

        cm[real_res][pred_res] += 1

    return cm

def main(home_path):
    ans_path = home_path + "answers"
    bayes_output = home_path + "bayes_output"

    parts_cnt = 0
    fpr = 0.0
    tpr = 0.0
    accuracy = 0.0

    for _, _, files in os.walk(ans_path):
        for filename in files:
            lhs_name = ans_path + '/' + filename
            rhs_name = bayes_output + '/' + filename

            parts_cnt += 1
            cm = compare_files(lhs_name, rhs_name)
            
            fpr += cm[0][1] / (cm[0][1] + cm[1][1])
            tpr += cm[0][0] / (cm[0][0] + cm[1][0])
            accuracy += (cm[0][0] + cm[1][1]) / (sum(cm[0]) + sum(cm[1]))
        
    
    fpr /= parts_cnt
    tpr /= parts_cnt
    accuracy /= parts_cnt

#    print("fpr,tpr,accuracy")
#    print(fpr, tpr, accuracy, sep=',')
    print(accuracy)

if __name__ == "__main__":
    home_path = "/home/gleb/github/ml2020/lab4-bayes/"
    main(home_path)

