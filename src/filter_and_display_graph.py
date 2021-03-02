import pandas as pd
import plotly.express as px
from import_and_calculate import group_filter_and_calculate

def display_graph(df: pd.DataFrame,
                             state: str = 'All') -> pd.DataFrame:
    """
    Takes the full cleaned COVID data set and filters it by state

    Inputs:
        df (pd.DataFrame): Dataframe containing the cleaned NYT COVID dataset

        state (str): The full name of the state to filter by, e.g. "Ohio"

    Returns:
        df_state (pd.DataFrame): Dataframe containing cleaned NYT COVID data for
        the selected state.

    """

    if state == 'All':
        df_state = df.groupby('date').sum()
    else:
        state_filter_exp = df.state == state
        df_state = df.copy().loc[state_filter_exp]
        df_state = df_state.groupby(['date', 'state']).sum()

    fig = px.bar(df_state, x='date', y='daily_cases')

    return fig

# TODO: Graph that compares any two states
# TODO: Graph that compares any state to the whole Country
