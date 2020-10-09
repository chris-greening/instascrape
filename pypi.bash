#!/bin/bash

#Automate the process of uploading package to PyPI

#Delete older version build directories
directories=("dist/" "build/" "insta_scrape.egg-info/")
for d in ${directories[@]};
do
	if [ -d $d ];
	then
		rm -rf $d
		echo "$d deleted!"
	fi
done

#Setup package and initiate upload to PyPI
python3 setup.py sdist bdist_wheel
twine upload dist/*
