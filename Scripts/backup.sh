#!/bin/bash

# Define the source folder (only the SMP folder in this case)
SOURCE_FOLDER="/home/minipc/.cubyz/saves/SMP"
BACKUP_FOLDER="/home/minipc/Desktop/cubyz_backups/"

# Check if the SMP folder exists
if [ ! -d "$SOURCE_FOLDER" ]; then
  echo "Error: The folder '$SOURCE_FOLDER' does not exist."
  exit 1
fi

# Get the current date and time in the format YYYY-MM-DD_HH-MM-SS
CURRENT_DATETIME=$(date "+%Y-%m-%d_%H-%M-%S")

# Get the name of the source folder (just the last part of the path)
FOLDER_NAME=$(basename "$SOURCE_FOLDER")

# Create the backup folder if it doesn't exist
mkdir -p "$BACKUP_FOLDER"

# Copy the SMP folder to the backup location with the date and time appended
cp -r "$SOURCE_FOLDER" "$BACKUP_FOLDER/${FOLDER_NAME}_${CURRENT_DATETIME}"

# Notify user
echo "Backup completed! Your backup is located at: $BACKUP_FOLDER/${FOLDER_NAME}_${CURRENT_DATETIME}"
