echo "lambda_legit,accuracy" > broot.csv

./run.sh 0.00001    >> broot.csv
./run.sh 0.0001     >> broot.csv
./run.sh 0.001      >> broot.csv
./run.sh 0.01       >> broot.csv
./run.sh 0.1        >> broot.csv

START=1
for (( i=1; i <= 36; i++ ))
do
  ./run.sh "$START" >> broot.csv
  START="$START"0
  echo "$i iteration"
done

./cleanup.sh
python3 build_plot.py

