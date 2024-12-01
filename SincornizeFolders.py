import os
import shutil
import time
import hashlib
import argparse
from datetime import datetime

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def log_operation(message, log_file):
 
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] {message}"
    print(formatted_message)
    with open(log_file, "a") as log:
        log.write(formatted_message + "\n")

def synchronize_folders(source, replica, log_file):
    
    if not os.path.exists(replica):
        os.makedirs(replica)
        log_operation(f"Created directory: {replica}", log_file)

    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        replica_path = os.path.join(replica, item)

        if os.path.isdir(source_path):
    
            synchronize_folders(source_path, replica_path, log_file)
        else:
            
            if not os.path.exists(replica_path) or calculate_md5(source_path) != calculate_md5(replica_path):
                shutil.copy2(source_path, replica_path)
                log_operation(f"Copied file: {source_path} to {replica_path}", log_file)

    for item in os.listdir(replica):
        replica_path = os.path.join(replica, item)
        source_path = os.path.join(source, item)

        if not os.path.exists(source_path):
            if os.path.isdir(replica_path):
                shutil.rmtree(replica_path)
                log_operation(f"Removed directory: {replica_path}", log_file)
            else:
                os.remove(replica_path)
                log_operation(f"Removed file: {replica_path}", log_file)

def main():
    parser = argparse.ArgumentParser(description="Synchronize two folders periodically.")
    parser.add_argument("source", help="Path to the source folder")
    parser.add_argument("replica", help="Path to the replica folder")
    parser.add_argument("log_file", help="Path to the log file")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds")

    args = parser.parse_args()

    source = args.source
    replica = args.replica
    log_file = args.log_file
    interval = args.interval

    if not os.path.exists(source):
        print(f"Error: Source folder does not exist: {source}")
        return


    log_operation("Starting folder synchronization...", log_file)
    try:
        while True:
            log_operation("Performing synchronization...", log_file)
            synchronize_folders(source, replica, log_file)
            log_operation("Synchronization complete.", log_file)
            time.sleep(interval)
    except KeyboardInterrupt:
        log_operation("Synchronization stopped by user.", log_file)

if __name__ == "__main__":
    main()
