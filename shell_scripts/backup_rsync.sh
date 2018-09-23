!/bin/bash
# Script to synchronise all files to backup.
# Reinstall Ubuntu Server LTS 16.04 with user=aephir, and you should be able to restore system with:
# sudo rsync -av --delete-during /mnt/drive1/rsync/ /
# modified from https://raspberrypi.stackexchange.com/questions/5427/can-a-raspberry-pi-be-used-to-create-a-backup-of-itself Milliways answer on Feb. 26 '15
# to restore a backup, use:
# sudo rsync -avH /mnt/drive1/rsync/ /
BACKUP_MOUNTED=$(mount | awk '/drive1/ {print $6}' | grep "rw")
if [ $BACKUP_MOUNTED ]; then
    echo $BACKUP_MOUNTED
    echo "Commencing Backup"
    rsync -aHv --delete-during --delete-excluded --exclude-from=/home/aephir/scripts/rsync-exclude.txt / /mnt/drive1/rsync
else
    echo "Backup drive not available or not writable"
fi
