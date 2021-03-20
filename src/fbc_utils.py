import pandas as pd
from constants import (DATA_TYPES, NYT_DATA_FILE, PARSE_DATES)


def read_data(live_file: str = NYT_DATA_FILE,
              data_types: str = DATA_TYPES,
              date_parse_cols: str = PARSE_DATES) -> pd.DataFrame:
    """
    Reads in the most recent live file
    """

    df = pd.read_csv(live_file,
                     dtype=data_types,
                     parse_dates=date_parse_cols)
    return df

def make_lagged_data(df: pd.DataFrame, lag: int = 1) -> pd.DataFrame:
    """
    Summary:
        Takes a dataframe and does a self to create a lagged metric

    Inputs:
        df (pd.DataFrame): Dataframe of time series
        lag (int): Numer of days to lag data

    Outputs:
        lagged_df (pd.DataFrame): Data frame with a columns of lagged metrics
    """
    def make_lag_name(col: str, lag: int = 1) -> str:
        """
        Creates a new column name based on the lag
        """
        col_suffix = "_".join(['lag', str(lag), 'day'])
        new_col_name = '_'.join([col, col_suffix])
        return new_col_name

    df_lagged = df.copy()
    dt_lag_col = make_lag_name('date', lag)
    df_lagged[dt_lag_col] = df_lagged['date'] - pd.tseries.offsets.Day(lag)

    left_cols = [dt_lag_col, 'state', 'county']
    right_cols = ['date_tmp', 'state', 'county']

    # Create a temporary df for the righthand side of the join,
    # with lagged metrics
    df_tmp = df_lagged.loc[:, ['date',  'state',
                               'county', 'cases',
                               'deaths']]

    cases_lag = make_lag_name('cases', lag)
    deaths_lag = make_lag_name('deaths', lag)

    df_tmp = df_tmp\
        .rename(columns={'date': 'date_tmp',
                         'cases': cases_lag,
                         'deaths': deaths_lag})

    df_lagged = pd.merge(df_lagged, df_tmp, how='left',
                         left_on=left_cols,
                         right_on=right_cols)

    to_drop = ['date_tmp', dt_lag_col]
    df_lagged = df_lagged.drop(to_drop, axis=1)
    return df_lagged


def calc_daily_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Summary:
        The metrics in the NYT data is cumulative by day.
        this function subtracts the prior day's total out
        so that we can get a proper daily metric.

    Inputs:
        df (pd.DataFrame) - dataframe of NYT covid data

    Outputs:
        df_daily_nums (pd.DataFrame) - NYT df with daily metrics

    """
    df_prior_day = make_lagged_data(df, lag=1)

    df_prior_day['daily_cases'] = (df_prior_day['cases'] -
                                   df_prior_day['cases_lag_1_day'])

    df_prior_day['daily_deaths'] = (df_prior_day['deaths'] -
                                    df_prior_day['deaths_lag_1_day'])

    df_daily_nums = df_prior_day.copy()
    df_daily_nums = df_daily_nums.drop(['cases_lag_1_day',
                                        'deaths_lag_1_day'],
                                       axis=1)
    return df_daily_nums


def calc_lagging_metrics(df: pd.DataFrame) -> pd.DateOffset:
    """
    Summary:
        COVID has an approximpate two-week incubation period so case numbers
        don't reflect the situation as it is today, but rather the sitation as
        it was two weeks ago
    """
    raise NotImplementedError

