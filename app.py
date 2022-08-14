#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output


# In[ ]:


cm = pd.read_csv('expanded_country_matrix.csv')


# In[ ]:


commodity = pd.read_excel('commodity.xlsx')


# In[ ]:


cm2 = pd.merge(cm, commodity, how='left', on = 'commodity')
df = cm2.iloc[:, 1:]


# In[ ]:


df['formatted_date'] = df.year * 1000 + df.week_of_the_year * 10 + 0
df['date'] = pd.to_datetime(df['formatted_date'], format='%Y%W%w')


# In[ ]:


app = Dash(__name__)


# In[ ]:


server = app.server


# In[ ]:


app.layout = html.Div(
    [
        html.Div(
        [
        html.P('Choose a category'),
        dcc.Dropdown(['Animal Products', 'Plant Products', 'Processed Food Products'], 
                      value = 'Animal Products', id = 'category')
        ], style = {'width': '30%', 'display': 'inline-block'}),
        
        html.Div(
        [
        html.P('Choose a country'),
        dcc.Dropdown(df['country'].unique(), 
                      value = 'Poland', id = 'country')
        ], style = {'width': '30%', 'display': 'inline-block'}),
        
        html.Div(
        [
        html.P('Choose a disease'),
        dcc.Dropdown(df['disease'].unique(), 
                      value = 'African swine fever', id = 'disease')
        ], style = {'width': '30%', 'display': 'inline-block'}),
        
        dcc.Graph(id = 'myGraph')
    ])
    
      
             
    


# In[ ]:


@app.callback(
    Output('myGraph', 'figure'),
    Input('category', 'value'),
    Input('country', 'value'),
    Input('disease', 'value'),
    )
def update_graph(cat, country, disease):
    
    if cat == 'Animal Products':
        dff = df[df['Animal Products'] == 1.0]
    elif cat == 'Plant Products':
        dff = df[df['Plant Products'] == 1.0]
    else:
        dff = df[df['Processed Food Products'] == 1.0]
        
    dff = dff[dff['country'] == country]
    dff = dff[dff['disease'] == disease]
    
    fig = px.scatter(dff, 
            x = 'date',
            y = 'metric_tons', 
            hover_data = ['country', 'year', 'week_of_the_year', 'commodity'])
    
    fig.update_layout(margin={'l': 80, 'b': 80, 't': 50, 'r': 0}, hovermode='closest')
    
    fig.update_xaxes(title = 'date')
    
    fig.update_yaxes(title = 'metric tons')
    
    return fig


# In[ ]:


if __name__ == '__main__':
    app.run_server(debug = True)


# In[ ]:




