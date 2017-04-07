#!/bin/bash
# see if txt files differ -- if so, change the name (append _xxx before suffix)
for i in *.txt; do
  sed -e "s?<bookmark mark='0'/> ??g" < C:/Dev/MathData/algebra/NROC-questions/$i > C:/Dev/MathData/algebra/NROC-questions/$i.cleaned
  cmp -s $i C:/Dev/MathData/algebra/NROC-questions/$i.cleaned
  if [[ $? == 1 ]]; then    # $? is result of last command
    echo $i differs
	 mv C:/Dev/MathData/algebra/NROC-questions/$i.cleaned C:/Dev/MathData/algebra/NROC-questions/${i%.txt}_terse.txt
  else
    rm C:/Dev/MathData/algebra/NROC-questions/$i.cleaned
  fi
done

read -rsp $'Press any key to continue...\n' -n1 key