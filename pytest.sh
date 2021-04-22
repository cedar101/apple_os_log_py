#!/bin/sh
echo "Press ^C (Ctrl+C) to quit."
log stream --predicate 'sender CONTAINS "_os_log"' --debug --info --style ndjson | pytest -s --cov=os_log --cov-report term-missing