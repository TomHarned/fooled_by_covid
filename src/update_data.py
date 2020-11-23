import subprocess
import datetime
import requests
import shlex
import pandas as pd
import importlib
import constants

importlib.reload(constants)

# TODO: only grab data if you haven't update in a day

# If the file has been updated today, then update it


def check_updated(log_file_name: str = constants.LOG) -> bool:
    """
    Checks the logfile to see if the data
       was updated today

       Input:
        log_file_name (str): name of log that tracks updates

        Output:
            updated_today (bool): True/False indcating wether data
            was updated today
    """

    today = str(datetime.date.today())

    # Get the last line of the log file
    # this is not very efficient, but the file is super small, so...
    with open(constants.LOG) as f:
        for line in f:
            pass
    last_line = line.strip('\n')

    if last_line == today:
        updated_today = True
        print("\nData is already up to date\n")
    else:
        updated_today = False

    return updated_today


        url = constants.NYT_DATA_ALL
        r = requests.get(url)

        # back_up prior day's file
        file_cmd = f"mv {constants.NYT_DATA_FILE} {constants.NYT_BACKUP_FILE}"
        subprocess.run(shlex.split(file_cmd))

        # Replace the "live" file with new
        with open(constants.NYT_DATA_FILE, 'wb') as f:
            f.write(r.content)

    else:
        print("Data is already current, no updates made")





df = pd.read_csv(constants.NYT_DATA_FILE,
                 dtype=constants.DATA_TYPES,
                 parse_dates=constants.PARSE_DATES)


# Log the latest update
with open(constants.LOG, 'a') as logfile:
    logfile.write(str(datetime.date.today()) + '\n')



subprocess.run(shlex.split(cmd))

