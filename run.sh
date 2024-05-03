

LOGFILE_STDOUT=/home/pi/Repos/rpiHomeBot/logs/log_main_stdout.txt
LOGFILE_STDERR=/home/pi/Repos/rpiHomeBot/logs/log_main_stderr.txt


python3 /home/pi/Repos/rpiHomeBot/main.py >> $LOGFILE_STDOUT 2> $LOGFILE_STDERR 

# python3 /home/pi/Repos/rpiHomeBot/main.py &

# sudo python3 /home/pi/Repos/rpiHomeBot/ble_handler.py &

# sudo /home/pi/Repos/ble_scanner/ble_scanner &

