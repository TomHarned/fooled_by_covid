import datetime
import subprocess
import shlex
import requests
from constants import (
    NYT_BACKUP_FILE,
    NYT_DATA_ALL,
    NYT_DATA_FILE,
    LOG
)


# If the file has been updated today, then update it
def check_updated(log_file_name: str = LOG) -> bool:
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
    with open(log_file_name) as f:
        for line in f:
            pass
    last_line = line.strip('\n')

    if last_line == today:
        updated_today = True
        print("\nData is already up to date\n")
    else:
        updated_today = False

    return updated_today


def replace_live_file(data_url: str = NYT_DATA_ALL,
                      live_file: str = NYT_DATA_FILE,
                      backup_file: str = NYT_BACKUP_FILE,
                      log_file: str = LOG) -> None:
    """
    Replace the current live file with the current version on the NYT
    github site for covid data.

    Inputs:
        data_url (str): url to the nyt github with the covid data

        live_file (str): relative path and name of the file used by the
                         dashboard

        backup_file (str): relative path and name of the prevoius file used by
                           the dashboard.

        log_file (str): relative path and name of the file containing ordered
                        datestamps of each update

        Output:
            None, overwrites the backup file with the current live file and
            updaes the current file with the live version on the nyt github.
    """

    # back_up prior day's file
    file_cmd = f"mv {live_file} {backup_file}"

    try:
        subprocess.run(shlex.split(file_cmd), check=True)
    except FileNotFoundError:
        print("Live file does not exist...no backup created")

    # Replace the "live" file with new
    req = requests.get(data_url)
    with open(live_file, 'wb') as f:
        f.write(req.content)

    # Log the latest update
    with open(log_file, 'a') as logfile:
        logfile.write(str(datetime.date.today()) + '\n')

    now = datetime.datetime.now().strftime('%D %H:%M')

    print(f"\nData updated as of {now}\n")
