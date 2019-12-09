while true
do
	python main.py
	if [ ! -z $? ]
	then
	    echo "Server error."
	    echo -n "Press ENTER to retry."
	    read
	fi
	sleep 1
done




