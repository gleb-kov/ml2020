input_dir=$PWD/bayes_input
output_dir=$PWD/bayes_output
idx=0

# Prepare infra in directory
g++ bayes.cpp -o bayes
mkdir "$input_dir" &> /dev/null
mkdir "$output_dir" &> /dev/null
mkdir "answers" &> /dev/null

# echo "Prepare dataset for bayes cpp code"
python3 walker.py $1

# echo "Run bayes cpp code"
for infile in "$input_dir"/*
do
  cat $infile | ./bayes > "$output_dir"/"$idx".txt
  idx=$(( idx + 1 ))
done

rm bayes

echo "Evaluate accuracy"
python3 aggregator.py
