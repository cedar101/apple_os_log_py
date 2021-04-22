#!/usr/bin/env zsh -i
echo "Press ^C (Ctrl+C) to quit."
log stream --predicate 'sender CONTAINS "_os_log"' --debug --info --style ndjson | zunit tests/zunit/os_log.zunit