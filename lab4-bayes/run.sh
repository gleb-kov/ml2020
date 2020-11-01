mydir=$PWD/inputs

g++ bayes.cpp -o bayes

for infile in "$mydir"/*
do
  echo "$infile"
  cat $infile | ./bayes > tmp.txt
done
