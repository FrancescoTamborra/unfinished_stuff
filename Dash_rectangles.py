import dash
import dash_canvas
import dash_table

import pandas as pd
import dash_html_components as html

from dash.dependencies import Input, Output, State
from dash_canvas.utils import parse_jsonstring_rectangle




filename = 'https://ucarecdn.com/d8677a69-d772-4bad-9f5c-bfb7afd8d7f7/-/resize/700/'

app = dash.Dash(__name__)

app.config.suppress_callback_exceptions = True

list_columns = ['width', 'height', 'left', 'top', 'animal']
list_animals = ['penguin', 'iguana', 'turtle', 'pelican']

columns = [{'name': i, "id": i} for i in list_columns]
columns[-1]['presentation'] = 'dropdown'

animals = [{'label': i, 'value': i} for i in list_animals]


app.layout = html.Div([
    html.Div([
              html.H3('Label images with bounding boxes'),
              dash_canvas.DashCanvas(
                                     id='canvas',
                                     width=500,
                                     tool='rectangle',
                                     lineWidth=2,
                                     lineColor='rgba(0, 255, 0, 0.5)',
                                     filename=filename,
                                     hide_buttons=['pencil', 'line'],
                                     goButtonTitle='Label'
                                     ),
             ]),
    html.Div([
              dash_table.DataTable(
                                   id='table',
                                   columns=columns,
                                   editable=True,
                                   dropdown={
                                             'animal': {
                                                      'options': animals
                                                     }
                                            }

                                  ),
             ])
])


@app.callback(Output('table', 'data'), [Input('canvas', 'json_data')])
def show_string(json_data):
    box_coordinates = parse_jsonstring_rectangle(json_data)
    df = pd.DataFrame(box_coordinates, columns=list_columns[:-1])
    df['animal'] = 'penguin'
    return df.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)
