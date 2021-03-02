#!/usr/bin/env ipython
import dash
import dash_core_components as dcc
import dash_html_components as html

sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "Simple sidebar example"
        )
    ]
)
