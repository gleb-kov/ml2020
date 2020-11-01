import os

# returns (ok, err)
def compare_files(lhs, rhs):
    lres = []
    rres = []
    with open(lhs, 'r') as lfd:
        lres = lfd.readlines()
    with open(rhs, 'r') as rfd:
        rres = rfd.readlines()
    if len(lres) != len(rres):
        raise ValueError("Invalid files comparing")
    
    ok = 0
    err = 0
    for i in range(len(lres)):
        if lres[i] == rres[i]:
            ok += 1
        else:
            err += 1
    return (ok, err)

def main(home_path):
    ans_path = home_path + "answers"
    bayes_output = home_path + "bayes_output"

    ok = 0
    err = 0

    for _, _, files in os.walk(ans_path):
        for filename in files:
            lhs_name = ans_path + '/' + filename
            rhs_name = bayes_output + '/' + filename

            part_res = compare_files(lhs_name, rhs_name)
            ok += part_res[0]
            err += part_res[1]
    print("OK: ", ok, ", err:", err)

if __name__ == "__main__":
    home_path = "/home/gleb/github/ml2020/lab4-bayes/"
    main(home_path)

