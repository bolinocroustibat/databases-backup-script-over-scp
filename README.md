This Python script is used for MySQL databases backup using mysqldump utility, Paramiko/SSHClient and Paramiko/SCPClient.

Use it with a cron. Edit your root crontab with "crontab -e" and add those lines, for example:

# Backup every Monday and Thursday at 6:00
0 6 * * 1,4 python3 /root/backup-sql/backup-mysql.py > /root/backup-sql/log-last-cron.log