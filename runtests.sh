#!/bin/sh

if [ $# -eq 0 ]; then
    echo "Please specify test to execute. e.g. ft for functional tests, ut for unit tests, all for all the tests"
    exit 1
fi

case $1 in
"ft")
     export TESTCHOICE="ft"
     ;;
"ut")
     export TESTCHOICE="ut"
     ;;
"all")
     export TESTCHOICE="all"
     ;;
*) echo "Please specify proper test type to execute. e.g. ft for functional tests, ut for unit tests, all for all the tests"
   exit 1
;;
esac

set RECREATEDB = "x"
while [ "${RECREATEDB}" != "Y" -a "${RECREATEDB}" != "y" -a "${RECREATEDB}" != "N" -a "${RECREATEDB}" != "n" ]
do
echo "Do you want to recreate db in couch (*** recommended y ***)? [Y/N]"
read RECREATEDB
done

cd src/datawinners

if [ "${RECREATEDB}" = "Y" -o "${RECREATEDB}" = "y" ]; then
    python manage.py recreatedb
fi

python manage.py syncdb

case "${TESTCHOICE}" in
"ft")
     echo "-------- Funtional test execution Started --------"
     xterm -e "python manage.py runserver" &
     cd ../../func_tests
     nosetests -a 'functional_test'
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
