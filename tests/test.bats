#!/usr/bin/env bats -p

# load '/usr/local/lib/bats-support/load.bash'
# load '/usr/local/lib/bats-assert/load.bash'
# load '/usr/local/lib/bats-file/load.bash'

# function setup {
	# load '/usr/local/lib/bats-support/load.bash'
	# load '/usr/local/lib/bats-assert/load.bash'
# 	named_pipe=/tmp/namedPipe
# 	# rm $named_pipe
# 	mkfifo -m 0666 $named_pipe
# 	log stream --predicate python --debug --info --style ndjson > $named_pipe &
# }

# function teardown() {
# 	killall log
# 	rm $named_pipe
# }

@test "read first line" {
	read line
	[[ "$line" == "Filtering"* ]]
}

@test "default logger" {
	python -m os_log.loguru debug 'This message should go to the Apple OSLog(unified logging system)'
	read line
	[[ "$line" == *"Debug"* && "$line" == *"This message should go to the Apple OSLog(unified logging system)"* ]]

	python -m os_log.loguru info 'So should this'
	read line
	[[ "$line" == *"Info"* && "$line" == *"So should this"* ]]

	python -m os_log.loguru error 'And non-ASCII stuff, too, like Øresund and Malmö'
	read line
	[[ "$line" == *"Error"* && "$line" == *"And non-ASCII stuff, too, like Øresund and Malmö"* ]]

	python -m os_log.loguru critical '심각한 오류가 발생했습니다!'
	read line
	[[ "$line" == *"Fault"* && "$line" == *"심각한 오류가 발생했습니다!"* ]]
}

@test "specify subsystem and category" {
	python -m os_log.loguru --subsystem 'org.python.macos' --category 'Development' debug 'This message should go to the Apple OSLog(unified logging system)'
	read line
	[[ "$line" == *"org.python.macos"* && "$line" == *"Development"* ]]
	[[ "$line" == *"Debug"* && "$line" == *"This message should go to the Apple OSLog(unified logging system)"* ]]

	python -m os_log.loguru --subsystem 'org.python.macos' --category 'Development' info 'So should this'
	read line
	[[ "$line" == *"org.python.macos"* && "$line" == *"Development"* ]]
	[[ "$line" == *"Info"* && "$line" == *"So should this"* ]]

	python -m os_log.loguru --subsystem 'org.python.macos' --category 'Development' error 'And non-ASCII stuff, too, like Øresund and Malmö'
	read line
	[[ "$line" == *"org.python.macos"* && "$line" == *"Development"* ]]
	[[ "$line" == *"Error"* && "$line" == *"And non-ASCII stuff, too, like Øresund and Malmö"* ]]

	python -m os_log.loguru --subsystem 'org.python.macos' --category 'Development' critical '심각한 오류가 발생했습니다!'
	read line
	[[ "$line" == *"org.python.macos"* && "$line" == *"Development"* ]]
	[[ "$line" == *"Fault"* && "$line" == *"심각한 오류가 발생했습니다!"* ]]
}