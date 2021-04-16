#!/bin/sh
echo "Press ^C (Ctrl+C) to quit."
log stream --predicate 'sender CONTAINS "_os_log"' --debug --info --style ndjson | bats -p tests/test.bats