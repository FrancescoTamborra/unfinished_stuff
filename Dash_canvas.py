from dash_table import DataTable
from dash_canvas import DashCanvas
from dash_canvas.utils import parse_jsonstring
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import cairosvg
from cairosvg import svg2png

import json
import dash_html_components as html
import dash_core_components as dcc
import dash
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go


app = dash.Dash(__name__)
#app.config.suppress_callback_exceptions = True

list_columns = ['type', 'width', 'height', 'path']
#columns=[{'name': i, 'id': i} for i in list_columns]

#print('columns = ', columns)

app.layout = html.Div([
    html.Center([
        html.H5('Draw a digit between 0 and 9'),
        DashCanvas(id='canvas',
                   hide_buttons=['line', 'zoom', 'pan', 'pencil', 'rectangle', 'select'],
                   lineWidth=5,
                   lineColor='black',
                   width=150,
                   height=500,
                   goButtonTitle='Predict'),
        DataTable(id='table',
                  style_cell={'textAlign': 'left'},
                  columns=[{'name': i, 'id': i} for i in list_columns]),
    ])
])


@app.callback(
    Output('table', 'data'),
    [Input('canvas', 'json_data')]
)
def update_data(string):
    if string:
        print('string = ', string)
        data = json.loads(string)
        print(type(data))
        print('data obj == ', data['objects'][0])
        print(type(data['objects'][0]))
        print('path ======', data['objects'][0]['path'])
        svg_path = data['objects'][0]['path']
        print('svg_path == ', svg_path)

        # use cairo to save the image ?
        #svg2png(bytestring=svg_path, write_to='output_number.png')
        # nope

        # check this:
        # https://pypi.org/project/svgpathtools/
        # https://pypi.org/project/svg.path/
    else:
        print('prevent')
        raise PreventUpdate
    return data['objects']


if __name__ == '__main__':
    app.run_server(debug=True)
