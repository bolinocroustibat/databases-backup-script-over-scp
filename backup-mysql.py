#!/usr/bin/python

## Import required Python libraries
import os, sys, time
from datetime import datetime
from paramiko import SSHClient # don't forget to "pip install paramiko" on OS
from scp import SCPClient # don't forget to "pip install scp" on OS

## Import settings
from settings import MYSQL_DB_NAMES, MYSQL_USER, MYSQL_USER_PASSWORD, LOGFILE, LOCAL_PATH, REMOTE_PATH, REMOTE_URL, REMOTE_USER

## Open log file and redirects print to log file (https://stackoverflow.com/questions/2513479/redirect-prints-to-log-file)
old_stdout = sys.stdout
log_file = open(LOGFILE,"w")
sys.stdout = log_file

## Function to have readable millisecond time in log file
def logtime():
	return(datetime.utcnow().strftime('%d/%m %H:%M:%S/%f')[:17])

## Getting current datetime and get full path names including datetime "2017-01-26--07-13-34".
DATETIME = time.strftime('%Y-%m-%d--%H-%M-%S')

## Create local backup folder
TODAY_LOCAL_PATH = LOCAL_PATH + DATETIME
try:
	os.makedirs(TODAY_LOCAL_PATH)
	print(logtime() + ": Local backup folder " + TODAY_LOCAL_PATH + " created.\n")
except:
	print(logtime() + ": ### ERROR ### while creating local backup folder\n")

## Local backup
for db in MYSQL_DB_NAMES:
	try:
		dumpcmd = "mysqldump -u " + MYSQL_USER + " -p" + MYSQL_USER_PASSWORD + " " + db + " > " + TODAY_LOCAL_PATH + "/" + db + ".sql"
		os.system(dumpcmd)
		print(logtime() + ": Backup file " + db + ".sql has been saved locally.\n")
	except Exception as e:
		print(logtime() + ": ### ERROR ### while trying to dump the database " + db + " locally\n")
		print(e + "\n")

## Remote backup
if REMOTE_PATH and REMOTE_PATH != '':
	TODAY_REMOTE_PATH = REMOTE_PATH + DATETIME
	## Connecting to backup server
	ssh = SSHClient()
	ssh.load_system_host_keys()
	ssh.connect(REMOTE_URL, username=REMOTE_USER)
	## Create remote backup folder
	try:
		ssh.exec_command('mkdir -p ' + TODAY_REMOTE_PATH)
		ssh.close
		print(logtime() + ": Remote backup folder " + TODAY_REMOTE_PATH + " created on " + REMOTE_URL + "\n")
	except:
		print(logtime() + ": ### ERROR ### while creating remote backup folder" + TODAY_REMOTE_PATH + " on " + REMOTE_URL + "\n")
	scp = SCPClient(ssh.get_transport()) # Initiate distant file transfer (SCPClient takes a paramiko transport as its only argument)
	## Copy on remote
	for db in MYSQL_DB_NAMES:
		try:
			scp.put(TODAY_LOCAL_PATH + "/" + db + ".sql", TODAY_REMOTE_PATH + "/" + db + ".sql")
			print(logtime() + ": Backup file " + db + ".sql has been copied on remote " + REMOTE_URL + ".\n")
		except Exception as e:
			print(logtime() + ": ### ERROR ### while tring to copy " + db + ".sql on the remote\n")
			print(e + "\n")
	scp.close()

print(logtime() + ": Backup script completed.\n")

## Close log file
sys.stdout = old_stdout
log_file.close()
