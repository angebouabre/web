#!/bin/bash


count=0

#mkdir -p principal 

for file in $( ls -1p *.asf )
do
	avconv -i ${file} ${file%.*}".ogg" 
	count=$((count + 1))
done

rm *.asf
printf '... %d\n' ${count}
