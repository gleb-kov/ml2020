import math

m = int(input())
verd = []


def get_table_num(line, pos):
    a = 1 << (pos + 1)
    if line % a < (1 << pos):
        return 0
    return 1

def get_line(line):
    res = []
    for i in range(m):
        res.append(get_table_num(line, i))
    return res


def build_cnf():
    global verd

    result = []
    for i in range(1 << m):
        if verd[i] == 0:
            continue
        res_line = []
        cnt = 0
        line = get_line(i)
        for pos in line:
            if pos == 1:
                cnt += 1
                res_line.append(1)
            else:
                res_line.append(-1)
        res_line.append(-cnt + 0.1)
        result.append(res_line)
    return result

cnt = 0
for i in range(1 << m):
    verd.append(int(input()))
    cnt += verd[-1]

if cnt == 0:
    print(1)
    print(1)
    sres = ""
    for i in range(m):
        sres += "0 "
    sres += "-100"
    print(sres)
elif cnt == (1 << m):
    print(1)
    print(1)
    sres = ""
    for i in range(m):
        sres += "0 "
    sres += "100"
    print(sres)
elif m < 10 or cnt <= 512:
    cnf = build_cnf()
    print(2)
    print(len(cnf), 1)
    for line in cnf:
        sres = ""
        for pos in line:
            sres += str(pos) + ' '
        print(sres)
    sres = ""
    for i in range(len(cnf)):
        sres += "1 "
    sres += "-0.5"
    print(sres)
else:
    raise Exception("undef sorry man")
