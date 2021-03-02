import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import json
from import_and_calculate import import_data, group_filter_and_calculate
from filter_and_display_graph import display_graph
# from layout_files.layouts import sidebar

# !!!save this off in a different file and try to mimic the example without the
# sidebar, then add the sidebar back in later
df = import_data()
# This function allows for more adjustment in the future
df = group_filter_and_calculate(df)
df['date'] = df.index

with open('../data/states.json', 'r') as f:
    states = json.load(f)

# Create graph to display in main pane

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width
# SIDEBAR_STYLE = {
#     "position": "fixed",
#     "top": 0,
#     "left": 0,
#     "bottom": 0,
#     "width": "16rem",
#     "padding": "2rem 1rem",
#     "background-color": "#f8f9fa",
# }
#
# # the styles for the main content position it to the right of the sidebar and
# # add some padding.
# CONTENT_STYLE = {
#     "margin-left": "18rem",
#     "margin-right": "2rem",
#     "padding": "2rem 1rem",
# }
#
# sidebar = html.Div(
#     [
#         html.H2("Sidebar", className="display-4"),
#         html.Hr(),
#         html.P(
#             "A simple sidebar layout with navigation links", className="lead"
#         ),
#         dcc.Dropdown(
#             id='state-input',
#             options=[
#                 states
#             ],
#             value='All'
#         ),
#      # style=SIDEBAR_STYLE
#     ])

# content = html.Div(id="page-content", style=CONTENT_STYLE)

# app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='select-state'
            options=
        )
    ])
])
@app.callback(
    Output(component_id='output-graph', component_property='children'),
    Input(component_id='state-selection', component_property='value')
)
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


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        page_one =html.Div(children=[
            html.H1(children='Hello Dash'),

                html.Div(children='''
                    Dash: A web application framework for Python.
                '''),
                dcc.Graph(
                    id='output-graph',
                    figure=fig
                )
            ])
        return page_one
    elif pathname == "/page-1":
        return page_one
    # html.P("This is the content of page 1. Yay!")
    elif pathname == "/page-2":
        return html.P("Oh cool, this is page 2!")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

if __name__ == "__main__":
    app.run_server(port=8080, debug=True)
