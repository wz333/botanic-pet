#!/bin/bash

process=$(lsof -t -i :15316)

if [-n "$process" ]; then
	kill -9 "$process"
	echo "process on 15316 terminated"
else
	echo "no process on 15316"
fi


command1="make run &"
command2="ngrok http 15316 &"

eval "$command1"
eval "$command2"
wait
echo "Server running!"