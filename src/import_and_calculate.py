import pandas as pd
import numpy as np
import update_data
import datetime
import fbc_utils

def import_data() -> pd.DataFrame:
    """
    Checks the NYT Github site for updates and constructs a dataframe from
    their COVID data, while calculating some basic daily and rolling metrics
    """
    updated = update_data.check_updated()
    if not updated:
        update_data.replace_live_file()

    df = fbc_utils.read_data()
    df_nums = fbc_utils.calc_daily_metrics(df)
    return df_nums

def group_filter_and_calculate(df, groupby_vars=None,
                               filter_expr=None) -> pd.DataFrame:
    """
    Takes the clean df of NY Times data and groups and filters by the supplied
    variables, returning a dataframe.

    """

    if not groupby_vars:
        groupby_vars = ['date', 'state']

    if not filter_expr:
        filter_expr = (df.date == df.date)

    df_grouped = (df
                  .loc[filter_expr, :]
                  .groupby(groupby_vars)
                  .sum()
                  .reset_index()
                  .set_index('date'))

    data_cols = ['daily_cases', 'daily_deaths']
    rolling_cols = ['daily_cases_7d_roll', 'daily_deaths_7d_roll']

    df_grouped[rolling_cols] = (df_grouped[data_cols]
                                .rolling(7, center=True)
                                .mean())

    return df_grouped
