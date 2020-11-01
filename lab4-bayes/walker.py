import os

class Letter:
    def __init__(self, filename):
        self.filename = filename
        self.is_legit = 'legit' in filename
        self.subject = ""
        self.text = ""

        with open(filename, 'r') as fd:
            lines = fd.readlines()
            subj, lines = lines[0], lines[1:]

            if subj.startswith("Subject:"):
                subj = subj[8:]
            self.subject = subj.strip()

            for line in lines:
                line = line.strip()
                if len(line) > 0:
                    self.text += line + " "

    def get_full_letter(self):
        return self.subject + ' ' + self.text

class DatasetPart:
    def __init__(self, path):
        self.letters = []
        
        for _, _, files in os.walk(path):
            for filename in files:
                filepath = path + '/' + filename
                self.letters.append(Letter(filepath))

        self.size = len(self.letters)

class Dataset:
    def __init__(self, path):
        self.parts = []

        for root, dirs, _ in os.walk(path):
            for dirname in dirs:
                if root == '.':
                    continue
                dirpath = path + '/' + dirname
                self.parts.append(DatasetPart(dirpath))

    def get_parts(self):
        return self.parts

class BayesSetup:
    def __init__(self):
        self.alpha = 0.001
        self.lambda_legit = 1
        self.lambda_spam = 1

# Contract: legit is 1, spam is 2
def prepare_input(train_parts, test_parts, bayes_setup, home_path, idx):
    inp_filename = home_path + "/bayes_input/" + str(idx) + ".txt"
    ans_filename = home_path + "/answers/" + str(idx) + ".txt"

    total_train_letters = sum([p.size for p in train_parts])
    total_test_letters = sum([p.size for p in test_parts])

    # fill input file
    with open(inp_filename, 'w') as fd:
        fd.write('2\n')
        fd.write(str(bayes_setup.lambda_legit) + " " + str(bayes_setup.lambda_spam))
        fd.write('\n')
        fd.write(str(bayes_setup.alpha))
        fd.write('\n')
        fd.write(str(total_train_letters))
        fd.write('\n')
        for tp in train_parts:
            for let in tp.letters:
                fd.write("1 " if let.is_legit else "2 ")
                txt = let.get_full_letter()
                fd.write(str(len(txt.split())))
                fd.write(" ")
                fd.write(txt)
                fd.write('\n')
        fd.write(str(total_test_letters))
        fd.write('\n')
        for tp in test_parts:
            for let in tp.letters:
                txt = let.get_full_letter()
                fd.write(str(len(txt.split())))
                fd.write(" ")
                fd.write(txt)
                fd.write('\n')
    # fill answer file
    with open(ans_filename, 'w') as fd:
        for tp in test_parts:
            for let in tp.letters:
                fd.write("1" if let.is_legit else "2")
                fd.write('\n')

def main(ds_path, home_path):
    ds = Dataset(ds_path)
    parts = ds.get_parts()
    
#    print("NGrams") TODO

    print("Cross")
    bayes_setup = BayesSetup()
    for part_idx in range(len(parts)):
        train = [x for i,x in enumerate(parts) if i != part_idx]
        test = [parts[part_idx]]
        prepare_input(train, test, bayes_setup, home_path, part_idx)

    print("Walker finished")

if __name__ == "__main__":
    home_path = "/home/gleb/github/ml2020/lab4-bayes/"
    main(home_path + "dataset", home_path)


