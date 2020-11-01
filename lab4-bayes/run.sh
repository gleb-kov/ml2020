input_dir=$PWD/bayes_input
output_dir=$PWD/bayes_output
idx=0

# Prepare infra in directory
g++ bayes.cpp -o bayes
mkdir "$input_dir" &> /dev/null
mkdir "$output_dir" &> /dev/null
mkdir "answers" &> /dev/null

# Prepare dataset for bayes cpp code
python3 walker.py

# Run bayes cpp code
for infile in "$input_dir"/*
do
  echo "Processing file: $infile"
  cat $infile | ./bayes > "$output_dir"/"$idx".txt
  echo "Result in $output_dir/$idx.txt"
  idx=$(( idx + 1 ))
done

rm bayes

# Evaluate accuracy and build plots
python3 aggregator.py
