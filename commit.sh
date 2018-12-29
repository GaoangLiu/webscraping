#!/bin/bash 
comments=$1
echo '*' `date +"%a %D/%T":` $comments | tee -a log/c.log 
readme='log/log.md'

cat log/c.log >> $readme
echo '```' >> $readme 

git add .
git commit -m "$comments"
git push 