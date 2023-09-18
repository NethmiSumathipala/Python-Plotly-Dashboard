# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 17:01:23 2023

@author: 1
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash import Input, Output

# Load the dataset
data = pd.read_excel(r'C:\Users\1\Desktop\HND\dash board assignment\Sample superstore.xlsx')
data['Order Date'] = pd.to_datetime(data['Order Date'])

df = data.groupby(["Order Date", "Category"]).sum().reset_index()

app = dash.Dash(title="Assignment")

app.layout = html.Div([html.H1(f'Sales Visualization', style={'color':'#8470FF','fontSize':50,'textAlign':'center'}),
                       dcc.Tabs( children=[
                           dcc.Tab(label='Introduction', style={'backgroundColor': '#00FA9A','fontSize':20},children=[html.Br(),
                           html.Br(),
                           html.Br(),
                           html.Br(),html.Br(),
                           html.Br(),html.Br(),
                           html.Br(),
                               dcc.Markdown('This dashboard provides a comprehensive overview of sales and profit data from our Superstore. Gain valuable insights into our business operations, customer segments, and product categories to make data-driven decisions.',
                                            style={'color':'#8B4726','fontSize':20,'textAlign':'center','fontWeight': 'bold'}),
                               
                               html.Br(),
                               html.Br(), html.Br(),
                                html.Br(),
                               html.Br(),
                               html.Br(), html.Br(),
                                html.Br(), html.Br(),
                                 html.Br(), html.Br(),
                                  html.Br(), html.Br(),
                                   html.Br(),]),
                           dcc.Tab(label='Line Chart', style={'backgroundColor': '#00FA9A','fontSize':20},children=[
                               html.Br(),
                               html.Label('Select a Category',
                                          style={'color' : '#41ABE4' , 'fontSize' : 18,'fontWeight': 'bold'}),
                               dcc.Dropdown(
                                   id='Category',
                                   value='Furniture',  
                                   options=[{'label': x, 'value': x} for x in df.Category.unique()],
                                   style={'font-weight': 'normal'},
                               ),

                               html.Br(),
                               html.Br(),
                               dcc.DatePickerRange(
                                   id='line-chart-date-picker',
                                   display_format='DD/MM/YYYY',
                                   min_date_allowed=min(df['Order Date']),
                                   max_date_allowed=max(df['Order Date']),
                                   initial_visible_month=max(df['Order Date']),
                                   start_date=min(df['Order Date']),
                                   end_date=max(df['Order Date']),
                               ),

                               html.H2(f'Category-wise Profit Trends Over Time',
                                       style={'textAlign': 'Center', 'fontSize': 23, 'color': '#FF1493','fontWeight': 'bold'}),
                               dcc.Graph(id="line1"),]),
                           
                           
                           dcc.Tab(label='Scatter Plot', style={'backgroundColor': '#00FA9A','fontSize':20}, children=[
                               html.Br(),
                               html.Br(),
                              html.Label('Pick one of the below:',
                                         style={'color' : '#41ABE4' , 'fontSize' : 18,'fontWeight': 'bold'}),
                               dcc.RadioItems(
                                   id='Scatter-plot-radio',
                                   options= [
                                       {'label':'Sales','value':'Sales'},
                                       {'label': 'Quantity' , 'value': 'Quantity'},
                                       {'label': 'Discount' ,'value': 'Discount'},
                                       {'label' : 'Profit' , 'value' : 'Profit'}],
                                   value='Quantity'
                                   
                               ),
                               
                               dcc.Graph(id='scatter-plot'),
                           ]),
                           
                           dcc.Tab(label='Interactive Chart' ,  style={'backgroundColor': '#00FA9A','fontSize':20},children=[
                               
                               html.H3(f'Profit Margin',
                                       style={'textAlign': 'Center', 'fontSize': 22, 'color': '	#00C957'}),
                               dcc.Graph(
                                  id='scatter-plot-interactive',
                                   figure=px.scatter(df, x='Sales', y='Profit',color_discrete_sequence=['#00FF00']),
                                   config={'displayModeBar': False},  
                                   className='chart'
                               ),
                               html.H3(f'Sales Over Time',
                                       style={'textAlign': 'Center', 'fontSize': 22, 'color': '	#00C957','fontWeight': 'bold'}),
                               # Line chart
                               dcc.Graph(
                                   id='line-chart-interactive',
                                   config={'displayModeBar': False},
                                   className='chart'
                               ),
                           ]),
                           
                           dcc.Tab(label='Custom Chart', style={'backgroundColor': '#00FA9A','fontSize':20}, children=[
                               html.Br(),
                               html.Br(),
                               html.Label('Select one of the below segments:',
                                          style={'color' : '#41ABE4' , 'fontSize' : 18,'fontWeight': 'bold'}),
                               dcc.Dropdown(
                                   id='segment-dropdown',
                                   options=[{'label': segment, 'value': segment} for segment in data['Segment'].unique()],
                                   value=data['Segment'].unique()[0],  
                                   style={'width': '50%'},
                               ),
                               
                               dcc.Graph(
                                   id='pie-chart',
                                   config={'displayModeBar': False},  
                               ),
                               
                               dcc.Graph(
                                   id='bar-chart',
                                   config={'displayModeBar': False},
                               ),
                               ])],
                            ),
                       html.Div("Nethmi Sarandi - COHNDDS231F-008", className="name-tag",
                                style={'color' : '#636363' , 'fontSize' : 18,'fontWeight': 'bold'}), ])

# Line chart
@app.callback(
    Output(component_id='line1', component_property='figure'),
    Input('line-chart-date-picker', 'start_date'),
    Input('line-chart-date-picker', 'end_date'),
    Input('Category', 'value')
)
def update_line_chart(start_date, end_date, selected_category):
    filtered_df = df[(df['Order Date'] >= start_date) & 
                     (df['Order Date'] <= end_date) & 
                     (df['Category'] == selected_category)]

    # Update the line chart
    fig = px.line(filtered_df, x='Order Date', y='Profit', title=f'Profit Trends for {selected_category}',
                  color_discrete_sequence=['#FF6A6A'])
    
    return fig

# Scatter plot
@app.callback(
    Output('scatter-plot', 'figure'),
    Input('Scatter-plot-radio', 'value'))
def update_scatter_plot(category_values):
    # Calculate correlation
    correlation = df[['Sales', category_values]].corr().iloc[0, 1]

    # Update the scatter plot
    fig = px.scatter(df, x='Sales', y=category_values, title=f'Correlation: {correlation:.2f}',color_discrete_sequence=['#C71585'])

    return fig

# Interactive chart
@app.callback(
    Output('line-chart-interactive', 'figure'),
    Input('scatter-plot-interactive', 'clickData')
)
def update_interactive_line_chart(click_data):
    # Create a default line chart
    fig = px.line(df, x='Order Date', y='Sales',color_discrete_sequence=['#2D7F06'])
    
    if click_data is not None and 'points' in click_data:
        selected_point = click_data['points'][0]
        selected_sales = selected_point['x']
        filtered_df = df[df['Sales'] == selected_sales]
        
        # Update the y-axis range of the line chart
        y_min = filtered_df['Sales'].min()
        y_max = filtered_df['Sales'].max()
        fig.update_yaxes(range=[y_min, y_max])
    
    return fig


#Custom chart
@app.callback(
    [Output('pie-chart', 'figure'),
     Output('bar-chart', 'figure')],
    Input('segment-dropdown', 'value')
)
def update_charts(selected_segment):
    filtered_pie_data = data[data['Segment'] == selected_segment].groupby("Region")["Sales"].sum().reset_index()
    filtered_bar_data = data[data['Segment'] == selected_segment].groupby("Category")["Sales"].sum().reset_index()
    
    fig_pie = px.pie(filtered_pie_data, values='Sales', names='Region', title=f'Sales by Region for {selected_segment}')
    fig_bar = px.bar(filtered_bar_data, x='Category', y='Sales', title=f'Sales by Category for {selected_segment}',
                     color_discrete_sequence=[	'#48D1CC'])
    
    return fig_pie, fig_bar

if __name__ == '__main__':
    app.run_server(port=9221)
