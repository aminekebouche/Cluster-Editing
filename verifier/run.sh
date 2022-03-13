#!/bin/bash
for((i=1;i<10;i+=2)); do ./verifier ../heur/heur00"$i".gr ../solutionsHeur/solution00"$i".gr; done
for((i=11;i<100;i+=2)); do ./verifier ../heur/heur0"$i".gr ../solutionsHeur/solution0"$i".gr; done
for((i=101;i<200;i+=2)); do ./verifier ../heur/heur"$i".gr ../solutionsHeur/solution"$i".gr; done
