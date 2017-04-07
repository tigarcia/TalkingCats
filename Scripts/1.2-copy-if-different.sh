#!/bin/bash
# see if txt files differ -- if so, change the name (append _xxx before suffix)
for i in *.txt; do
  sed -e "s?<bookmark mark='0'/> ??g" < C:/Dev/MathData/algebra/books/col12116_1.2_complete/MathML/$i > C:/Dev/MathData/algebra/books/col12116_1.2_complete/MathML/$i.cleaned
  cmp -s $i C:/Dev/MathData/algebra/books/col12116_1.2_complete/MathML/$i.cleaned
  if [[ $? == 1 ]]; then    # $? is result of last command
    echo $i differs
	 mv C:/Dev/MathData/algebra/books/col12116_1.2_complete/MathML/$i.cleaned C:/Dev/MathData/algebra/books/col12116_1.2_complete/MathML/${i%.txt}_times.txt
  else
    rm C:/Dev/MathData/algebra/books/col12116_1.2_complete/MathML/$i.cleaned
  fi
done

read -rsp $'Press any key to continue...\n' -n1 key