#!/bin/bash

#Delete old data

directories=("dist/" "build/" "insta_scrape.egg-info/")

for d in ${directories[@]};
do
	if [ -d $d ];
	then
		rm -rf $d
		echo "$d deleted!"
	fi
done

python3 setup.py sdist bdist_wheel
twine upload dist/*

