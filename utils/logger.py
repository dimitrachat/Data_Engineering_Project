import os
import time
import datetime
from datetime import datetime
import traceback


# Global Vars
data_path = None

def set_logging_path(path)->None:

    """
    Set the logging path of this job in order for our cudtom logging to work 
    :path -> str: Your logging path
    """
    global data_path
    data_path = path


def log(txt)->None:
    """
    A custom function to log our input to a file located inside the data folder. 
    Every Month will have a new log file:
    txt-> str: Customizing Logging
    """
    if data_path is None:
        raise ValueError("Logging path not set. Please call set_logging_path() before using log().")
    now = datetime.now()
    timestampt = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestampt}: {txt}")

    log_dir = os.path.join(data_path, 'data')
    log_filename = f"{now.strftime('%Y-%m')}-logs.txt"
    log_path = os.path.join(data_path, log_filename)
    log_path = os.path.join(log_dir,log_filename)

    # Ensure to create the log directory if it doesn't exist
    os.makedirs(log_dir, exist_ok = True)
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(f"{timestampt}:{txt}\n")
        