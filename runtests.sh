#!/bin/bash

if [ $# -eq 0 ]; then
    export TESTCHOICE="all"
else
    case $1 in
	"ft")
	    export TESTCHOICE="ft"
	    ;;
	"ut")
	    export TESTCHOICE="ut"
	    ;;
	"sm")
	    export TESTCHOICE="sm"
	    ;;
	"all")
	    export TESTCHOICE="all"
	    ;;
	*)
	    export TESTCHOICE="all"
	    ;;
    esac
fi

set RECREATEDB = "x"
while [ "${RECREATEDB}" != "Y" -a "${RECREATEDB}" != "y" -a "${RECREATEDB}" != "N" -a "${RECREATEDB}" != "n" ]
do
    read -s -n1 -p "Do you want to recreate db in couch (*** recommended y ***)? [Y/n]" RECREATEDB
    echo
    if [ -z ${RECREATEDB} ]; then
	break
    fi
done

cd src/datawinners

if [ "${RECREATEDB}" != "N" -a "${RECREATEDB}" != "n" ]; then
    python manage.py recreatedb
fi

python manage.py flush --noinput

case "${TESTCHOICE}" in
"ft")
     echo "-------- Funtional test execution Started --------"
     xterm -e "python manage.py runserver" &
     cd ../../func_tests
     nosetests -a 'functional_test'
     ;;
"sm")
     echo "-------- Funtional test execution Started --------"
     xterm -e "python manage.py runserver" &
     cd ../../func_tests
     nosetests -a 'smoke'
     ;;
"ut") echo "-------- Unit test execution Started --------"
     cd ../..
     nosetests -a '!functional_test'
     ;;
"all") echo "-------- All test execution Started --------"
     xterm -e "python manage.py runserver" &
     cd ../..
     nosetests
     ;;
esac

exit 0
