import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import pickle
from import_and_calculate import import_data, group_filter_and_calculate
from filter_and_display_graph import display_graph
# from layout_files.layouts import sidebar

# !!!save this off in a different file and try to mimic the example without the
# sidebar, then add the sidebar back in later
# TODO: smooth out daily numbers
# TODO: create a per Capita metric
# TODO: create an "all" option for whole country
# TODO: all for state comparissons -- two states plus whole country
df_import = import_data()
# This function allows for more adjustment in the future
df = group_filter_and_calculate(df_import)
df['date'] = df.index

# see: https://stackoverflow.com/questions/12203901/pandas-crashes-on-repeated-dataframe-reset-index
df = df.reset_index(drop=True)
df.reset_index(inplace=True)
df.drop('index', inplace=True, axis=1)


with open('../data/states.txt', 'rb') as f:
    states = pickle.load(f)

# Create graph to display in main pane

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='select-state',
            options=states,
            value='Connecticut'
        )
    ]),
    dcc.Graph(id='main-graph')
])


@app.callback(
    Output(component_id='main-graph', component_property='figure'),
    Input(component_id='select-state', component_property='value')
)
def display_graph(state: str = 'Connecticut') -> pd.DataFrame:
    """
    Takes the full cleaned COVID data set and filters it by state

    Inputs:
        df (pd.DataFrame): Dataframe containing the cleaned NYT COVID dataset

        state (str): The full name of the state to filter by, e.g. "Ohio"

    Returns:
        df_state (pd.DataFrame): Dataframe containing cleaned NYT COVID data for
        the selected state.

    """

    state_filter_exp = (df.state == state)
    df_state = df.copy().loc[state_filter_exp]
    df_state = df_state.groupby(['date', 'state']).sum()
    df_state.reset_index(inplace=True)

    fig = px.bar(df_state, x='date', y='daily_cases')
    return fig


if __name__ == "__main__":
    app.run_server(port=8080, debug=True)
