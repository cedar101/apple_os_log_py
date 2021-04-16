#!/usr/bin/env zsh
emulate -LR bash
echo "Press ^C (Ctrl+C) to quit."
log stream --predicate 'sender CONTAINS "_os_log"' --debug --info --style ndjson | zunit tests/os_log.zunit