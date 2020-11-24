import pandas as pd
from constants import NYT_DATA_FILE, DATA_TYPES, PARSE_DATES

def read_data(live_file: str = constants.NYT_DATA_FILE,
              data_types: str = constants.DATA_TYPES,
              date_parse_cols: str = constants.PARSE_DATES) -> pd.DataFrame:
    """
    Reads in the most recent live file
    """

    df = pd.read_csv(live_file,
                     dtype=data_types,
                     parse_dates=date_parse_cols)
    return df
