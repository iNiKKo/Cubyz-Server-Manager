#!/bin/bash

# Define the source folder & Save File
SOURCE_FOLDER="/home/minipc/.cubyz/saves/SMP"
BACKUP_FOLDER="/home/minipc/Desktop/cubyz_backups/"

# Check if the folder exists
if [ ! -d "$SOURCE_FOLDER" ]; then
    echo "Error: The folder '$SOURCE_FOLDER' does not exist."
    exit 1
fi

# Get the current date and time in UK Central Time with the format DD_MM_YYYY_HH_MM_SS
CURRENT_DATETIME=$(TZ="Europe/London" date "+%d_%m_%Y_%H_%M_%S")


FOLDER_NAME=$(basename "$SOURCE_FOLDER")

# Create the backup folder if it doesn't exist
mkdir -p "$BACKUP_FOLDER"

# Copy the saved folder to the backup location with the date and time appended
cp -r "$SOURCE_FOLDER" "$BACKUP_FOLDER/${FOLDER_NAME}_${CURRENT_DATETIME}"

# Notify user
echo "Backup completed! Your backup is located at: $BACKUP_FOLDER/${FOLDER_NAME}_${CURRENT_DATETIME}"
