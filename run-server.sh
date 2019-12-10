while true
do
	python3 main.py
	if [ ! $? -eq 0 ]
	then
	    echo "Server error."
	    echo -n "Press ENTER to retry."
	    read
	fi
	sleep 1
done




