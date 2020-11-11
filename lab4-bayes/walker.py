import os
import sys

class Letter:
    def __init__(self, filename):
        self.filename = filename
        self.is_legit = 'legit' in filename
        self.subject = ""
        self.text = ""
        self.sparse = None

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

    def get_ngrams(self, n):
        msg = self.get_full_letter().split()
        ngrams = []
        for i in range(0, len(msg) - n):
            gram = ""
            for j in range(n):
                gram += msg[i + j] + ' '
            ngrams.append(gram[:-1])
        return ngrams

    def build_mapping_ngrams_to_vector(self, ngram_map, n):
        if self.sparse is not None:
            return self.sparse
        sparse_vector = [0] * len(ngram_map)
        ngrams = self.get_ngrams(n)
        for gram in ngrams:
            idx = ngram_map[gram]
            sparse_vector[idx] += 1
        self.sparse = ' '.join(str(g) for g in sparse_vector)

class DatasetPart:
    def __init__(self, path):
        self.letters = []
        
        for _, _, files in os.walk(path):
            for filename in files:
                filepath = path + '/' + filename
                self.letters.append(Letter(filepath))

        self.size = len(self.letters)

    def get_ngrams(self, n):
        ngrams = []
        for let in self.letters:
            ngrams += let.get_ngrams(n)
        ngrams = list(set(ngrams))
        return ngrams

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
        self.lambda_legit = 1e-5 if len(sys.argv) < 2 else float(sys.argv[1])
        self.lambda_spam = 1e-5

# Contract: legit is 1, spam is 2
def prepare_input(train_parts, test_parts, bayes_setup, home_path, idx, use_ngrams=False):
    inp_filename = home_path + "/bayes_input/" + str(idx) + ".txt"
    ans_filename = home_path + "/answers/" + str(idx) + ".txt"

    #############################3

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

                if not use_ngrams:
                    txt = let.get_full_letter()
                else:
                    txt = let.sparse

                txt_len = len(txt.split())
                fd.write(str(txt_len))
                fd.write(" ")
                fd.write(txt)
                fd.write('\n')
        fd.write(str(total_test_letters))
        fd.write('\n')
        for tp in test_parts:
            for let in tp.letters:

                if not use_ngrams:
                    txt = let.get_full_letter()
                else:
                    txt = let.sparse

                txt_len = len(txt.split())
                fd.write(str(txt_len))
                fd.write(" ")
                fd.write(txt)
                fd.write('\n')
    # fill answer file
    with open(ans_filename, 'w') as fd:
        for tp in test_parts:
            for let in tp.letters:
                fd.write("1" if let.is_legit else "2")
                fd.write('\n')

def ngrams_to_dict(ngrams):
    ngrams_dict = {}
    ngrams = list(set(ngrams))
    idx = 0

    for gram in ngrams:
        ngrams_dict[gram] = idx
        idx += 1
    return ngrams_dict

def get_all_ngrams(parts, n):
    ngrams = []
    for part in parts:
        ngrams += part.get_ngrams(n)
    ngrams = list(set(ngrams))
    return ngrams

def main(ds_path, home_path, use_ngrams=False):
    ds = Dataset(ds_path)
    parts = ds.get_parts()

    if use_ngrams:
        print("NGrams")
        N_GRAM = 2
        ngrams_dict = ngrams_to_dict(get_all_ngrams(parts, N_GRAM))
        for part in parts:
            print("Build part")
            for let in part.letters:
                let.build_mapping_ngrams_to_vector(ngrams_dict, N_GRAM)

    bayes_setup = BayesSetup()
    for part_idx in range(len(parts)):
        train = [x for i,x in enumerate(parts) if i != part_idx]
        test = [parts[part_idx]]
        prepare_input(train, test, bayes_setup, home_path, part_idx, use_ngrams)

#    print("Walker finished")

if __name__ == "__main__":
    home_path = "/home/gleb/github/ml2020/lab4-bayes/"
    main(home_path + "dataset", home_path)


