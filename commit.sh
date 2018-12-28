#!/bin/bash 
comments=$1
echo '*' `date +"%a %D/%T":` $comments | tee -a c.log 
readme='log.md'

cat c.log >> $readme
echo '```' >> $readme 

git add .
git commit -m "$comments"
git push 