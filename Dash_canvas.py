from dash_table import DataTable
from dash_canvas import DashCanvas
from dash_canvas.utils import parse_jsonstring
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

#import cairosvg
#from cairosvg import svg2png

#from svg.path import parse_path
#from svgpathtools import wsvg
from svgpathtools import parse_path, wsvg
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM

import json
import tempfile
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
        print('data obj == ', data['objects'][0])
        print(type(data['objects'][0]))
        svg_path = data['objects'][0]['path']
        print('svg_path == ', svg_path)

        inner_list = []
        for block in svg_path:
            inner_str = " ".join(map(str, block))
            inner_list.append(inner_str)

        path_str = " ".join(inner_list)
        print('path string = ', path_str)

        path = parse_path(path_str)
        print('parsed = ', path)
        print("path is continuous? ", path.iscontinuous())
        print("path is closed? ", path.isclosed())

        # Save svg tempfile
        t = tempfile.NamedTemporaryFile()
        print(t.name)
        wsvg(path, filename=t.name)
        wsvg(path, filename='persistent.svg')
        t.file.seek(0)
        # do stuff

        drawing = svg2rlg(t.name)
        renderPM.drawToFile(drawing, "digit.png", fmt="PNG")
        #
        t.close()

    else:
        print('prevent')
        raise PreventUpdate
    return data['objects']


if __name__ == '__main__':
    app.run_server(debug=True)
