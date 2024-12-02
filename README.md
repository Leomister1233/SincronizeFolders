# SincronizeFolders

Folder Synchronization Script
This script synchronizes two folders, ensuring that the contents of the source folder are mirrored in the replica folder. It will copy new or updated files from the source to the replica and delete files from the replica that no longer exist in the source. The synchronization process runs at a defined interval, allowing periodic updates.

Features:
Synchronizes files and directories between a source and a replica folder.
Copies files if they are new or modified based on MD5 checksum comparison.
Deletes files from the replica if they no longer exist in the source folder.
Logs all operations with timestamps to a specified log file.
Runs periodically at a user-defined interval.
