#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 00:39:07 2019

@author: apple
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table_experiments as dt
import plotly.graph_objs as go
go.Scattermapbox
#import os
import pandas as pd

mapbox_access_token = 'pk.eyJ1IjoidXJzdWxha2Fjem1hcmVrIiwiYSI6ImNpd2ZldGh0OTAw\
MTcyb21ucjExbHpleW8ifQ.-m-YwEngdx5IEET1r4ZFqg'
#os.getenv('MAPBOXKEY')

app = dash.Dash(__name__)
server = app.server

# load data
url = 'https://raw.githubusercontent.com/a627142126/capstone-2018/master/SLCo_station_latlong_v1_yc.csv'
df = pd.read_csv(url)
df['text'] = df['Station Name'] #+ df['Avg. Test Fees']
df = df[['Station Id', 'Avg. Test Fees', 'Station Name', 
         'Address', 'City', 'ZIP', 'Latitude', 'Longitude', 'text']]
df['Avg. Test Fees'] = df['Avg. Test Fees'].str.replace('$', '')
df['Avg. Test Fees'] = pd.to_numeric(df['Avg. Test Fees'])



data = [go.Scattermapbox(
        lon = df['Longitude'],
        lat = df['Latitude'],
        text = df['text'],
        marker=go.scattermapbox.Marker(
            colorscale = 'YlOrRd',
            reversescale = True,
            color = df['Avg. Test Fees'],
            cmin = 10,
            cmax = df['Avg. Test Fees'].max(),
            colorbar=dict(
                title='Avg. Testing Fees ($)'
            )
        )
        )]



layout_table = dict(
    autosize=True,
    height=500,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
)
layout_table['font-size'] = '12'
layout_table['margin-top'] = '20'

layout_map = dict(
    autosize=True,
    height=500,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
    title='Emissions Testing Centers',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(
            lon=-111.9067,
            lat=40.6666
        ),
        zoom=10,
    )
)


def gen_map(df):
    # groupby returns a dictionary mapping the values of the first field
    # 'classification' onto a list of record dictionaries with that
    # classification value.
    return {
        "data": [{
                "type": "scattermapbox",
                "lat": list(df['Latitude']),
                "lon": list(df['Longitude']),
                "hoverinfo": "text",
                "hovertext": [["Name: {} <br>Address: {} <br>Price: {}".format(i,j,k)]
                                for i,j,k in zip(df['text'], df['Address'],df['Avg. Test Fees'])],
                "mode": "markers",
                "name": list(df['text']),
                "marker": {
                    "size": 6,
                    "opacity": 0.7
                }
        }],
        "layout": layout_map
    }

app.layout = html.Div(
    html.Div([
        html.Div(
            [
                html.H1(children='Emission Test Centers',
                        className='nine columns'),
                html.Img(
                    src="https://cusp.nyu.edu/wp-content/uploads/2017/12/PNG-logo-01.png",
                    className='three columns',
                    style={
                        'height': '16%',
                        'width': '16%',
                        'float': 'right',
                        'position': 'relative',
                        'padding-top': 12,
                        'padding-right': 0
                    },
                ),
                html.Div(children='''
                        You can use this website to locate the nearest repair shop that can do emission test.
                        ''',
                        className='nine columns'
                )
            ], className="row"
        ),

        # Selectors
        html.Div(
            [
                html.Div(
                    [
                        html.P('Choose Zipcode:'),
                        dcc.Dropdown(
                            id='zipcode',
                            options= [{'label': str(item),
                                                  'value': str(item)}
                                                 for item in set(df['ZIP'])],
                            multi=True,
                            value=list(set(df['ZIP']))
                        )
                    ],
                    className='six columns',
                    style={'margin-top': '10'}
                ),
                html.Div(
                    [
                        html.P('Choose Price:'),
                        dcc.Dropdown(
                            id='price',
                            options= [{'label': str(item),
                                                  'value': str(item)}
                                                 for item in set(df['Avg. Test Fees'])],
                            multi=True,
                            value=list(set(df['Avg. Test Fees']))
                        )
                    ],
                    className='six columns',
                    style={'margin-top': '10'}
                )
                    ],
                    className='row'
                    #style={'margin-top': '10'}
                ),
          
     

        # Map + table + Histogram
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id='map-graph',
                                  animate=True,
                                  style={'margin-top': '20'})
                    ], className = "six columns"
                ),
                html.Div(
                    [
                        dt.DataTable(
                            rows=df.to_dict('records'),
                            columns=df.columns,
                            row_selectable=True,
                            filterable=True,
                            sortable=True,
                            selected_row_indices=[],
                            id='datatable'),
                    ],
                    style = layout_table,
                    className="six columns"
                ),
                
                html.Div(
                    [
                        html.P('Developed by Capstone Team at CUSP - ', style = {'display': 'inline'}),
                        html.A('cusp@nyu.edu', href = 'cuspo@nyu.edu')
                    ], className = "twelve columns",
                       style = {'fontSize': 18, 'padding-top': 20}
                )
            ], className="row"
        )
    ], className='ten columns offset-by-one'))
                    
                    
                    
@app.callback(
        Output('map-graph', 'figure'),
        [Input('datatable', 'rows'),
         Input('datatable', 'selected_row_indices')])     

def map_selection(rows, selected_row_indices):
    aux = pd.DataFrame(rows)
    temp_df = aux.ix[selected_row_indices, :]
    if len(selected_row_indices) == 0:
        return gen_map(aux)
    return gen_map(temp_df)         
        





@app.callback(
    Output('datatable', 'rows'),
    [Input('zipcode', 'value'),
     Input('price', 'value')])
def update_selected_row_indices(zipcode, price):
    map_aux = df.copy()

    # Type filter
    map_aux = map_aux[map_aux['ZIP'].isin(zipcode)]
    # Boroughs filter
    map_aux = map_aux[map_aux['Avg. Test Fees'].isin(price)]

    rows = map_aux.to_dict('records')
    return rows

       
        
        
        
        


if __name__ == '__main__':
    app.run_server(debug=True)

