rm colores.txt
for f in ./data/*
do
    python3 solver.py $f greedy
done