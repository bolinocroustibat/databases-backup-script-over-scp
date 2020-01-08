## PostgreSQL database details to which backup to be done. Used only by backup-postgresql.py script.
POSTGRES_DB_NAMES = ['db1_name','db2_name'] # names of the PostgreSQL databases names to backup.
POSTGRES_SYSTEM_USER = 'postgres' # System user who will access PostgreSQL. Make sure he has enough privileges to take all databases backup.

## MySQL database details to which backup to be done. Used only by backup-mysql.py script.
MYSQL_DB_NAMES = ['db1_name','db2_name'] # names of the MySQL databases to backup.
MYSQL_USER = '' # MySQL user. Make sure he has enough privileges to take all databases backup.
MYSQL_USER_PASSWORD = '' # MySQL user password

## Local setting
LOCAL_PATH = '/root/databases-backup-script-over-scp/dumps/' # full local path where dumps will be saved, with trailing slash.
LOGFILE = '/root/databases-backup-script-over-scp/log-last-script.log' # full path to log file.

### Remote settings
REMOTE_URL = '' # leave blank if you don't want to save remotely.
REMOTE_USER = '' # you need to be authorized on remote with your user SSH keys.
REMOTE_PATH = '/home/backup-sql/' # full remote path where dumps will be saved.
