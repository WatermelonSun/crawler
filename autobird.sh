for((sh=1;sh<=10;sh++))
do
	p="https://www.xeno-canto.org/"
	path=${p}${sh}
    python bird.py $path

    #echo $path
done
echo SUCCESS
