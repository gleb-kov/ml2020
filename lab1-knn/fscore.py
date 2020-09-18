def totalsum(cm):
    total = 0.0
    for row in cm:
        for el in row:
            total += el
    return total

def fillTP(cm):
    tp = []
    for i in range(len(cm)):
        tp.append(cm[i][i])
    return tp

def fillFP(cm):
    fp = [0]*len(cm)
    for i in range(len(cm)):
        for j in range(len(cm[i])):
            if i != j:
                fp[j] += cm[i][j]
    return fp

def fillFN(cm):
    fn = [0]*len(cm)
    for i in range(len(cm)):
        for j in range(len(cm[i])):
            if i != j:
                fn[i] += cm[i][j]
    return fn

def calc_fscore(cm):
    total = totalsum(cm)
    tp = fillTP(cm)
    fn = fillFN(cm)
    fp = fillFP(cm)

    micro_f = 0.0
    macro_f = 0.0
    recall_w = 0.0
    prec_w = 0.0
   
    for i in range(len(cm)):
        if tp[i] == 0:
            continue
        cc = tp[i] + fn[i]
        recall_i = tp[i] / cc
        prec_i = tp[i] / float(tp[i] + fp[i])
        f1 = 2.0 * recall_i * prec_i / (recall_i + prec_i)

        micro_f = micro_f + f1 * cc / total
        recall_w = recall_w + float(tp[i]) / total
        prec_w = prec_w + prec_i * cc / total

    macro_f = 2.0 * prec_w * recall_w / (prec_w + recall_w)
    return (macro_f, micro_f)

def main():
    k = int(input())
    cm = []
    for i in range(k):
        row = list(map(int, input().split()))
        cm.append(row)
    #print(cm)
    score = calc_fscore(cm)
    print(score[0])
    print(score[1])

if __name__ == '__main__':
    main()
