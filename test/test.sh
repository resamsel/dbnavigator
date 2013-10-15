#!/bin/bash

while (( "$#" )); do
	TESTCASE=$(basename ${1%.sh})
	ACTUAL=/tmp/test-$TESTCASE.actual
	EXPECTED=test/resources/$TESTCASE.expected
	SCRIPT=$(cat test/resources/$TESTCASE.sh)

	echo -n "Testing $TESTCASE... "
	sh -c "build/files/$SCRIPT" > $ACTUAL

	DIFF=$(diff -u $EXPECTED $ACTUAL)

	if [ "$DIFF" != "" ]; then
		echo FAILED
		if [ "$(which colordiff)" != "" ]; then
			echo colordiff $EXPECTED $ACTUAL
			colordiff $EXPECTED $ACTUAL
		else
			echo diff -u $EXPECTED $ACTUAL
			echo $DIFF
		fi
		exit -1
	else
		echo OK
	fi

	shift
done
