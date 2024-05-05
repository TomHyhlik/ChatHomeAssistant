LOGFILE_STDOUT=/home/pi/Repos/ChatHomeAssistant/logs/log_main_stdout.txt
LOGFILE_STDERR=/home/pi/Repos/ChatHomeAssistant/logs/log_main_stderr.txt

python3 /home/pi/Repos/ChatHomeAssistant/main.py >> $LOGFILE_STDOUT 2> $LOGFILE_STDERR 

