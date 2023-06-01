import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
from dash import html
from jupyter_dash import JupyterDash

df = pd.read_excel('Global-Coal-Plant-Tracker-January-2023.xlsx', sheet_name='Units')

fig = px.scatter_mapbox(df, lat='Latitude', lon='Longitude', hover_data=['Emission factor (kg of CO2 per TJ)'],
                        color='Emission factor (kg of CO2 per TJ)', zoom=3,
                        color_continuous_scale='Bluered')
fig.update_layout(mapbox_style="carto-positron")
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

fig2 = px.scatter_mapbox(df, lat='Latitude', lon='Longitude', hover_data=['Annual CO2 (million tonnes / annum)'],
                         color='Annual CO2 (million tonnes / annum)', zoom=3,
                         color_continuous_scale='Picnic')
fig2.update_layout(mapbox_style="carto-positron")
fig2.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

country_totals = df.groupby('Country')['Annual CO2 (million tonnes / annum)'].sum().reset_index()

top_countries = country_totals.sort_values('Annual CO2 (million tonnes / annum)', ascending=False).head(15)

colors = ['rgb(166,206,227)', 'rgb(31,120,180)', 'rgb(178,223,138)', 'rgb(51,160,44)', 'rgb(71,6,6)',
          'rgb(227,26,28)', 'rgb(253,191,111)', 'rgb(255,127,0)', 'rgb(202,178,214)', 'rgb(106,61,154)',
          'rgb(255,255,153)', 'rgb(177,89,40)', 'rgb(253,180,98)', 'rgb(179,222,105)', 'rgb(252,205,229)']

data = [
    go.Bar(
        x=top_countries['Country'],
        y=top_countries['Annual CO2 (million tonnes / annum)'],
        marker=dict(color=colors),
        hovertemplate='<b>%{x}</b><br><extra></extra>',
        textposition='none'
    )
]

layout = go.Layout(
    title='Top 15 Countries - Annual CO2 Emissions from Coal Plants',
    xaxis=dict(title='Country'),
    yaxis=dict(title='Annual CO2 (million tonnes / annum)'),
    showlegend=False
)

fig3 = go.Figure(data=data, layout=layout)

app = Dash(__name__)
server = app.server

app.layout = html.Div(
    children=[
        html.H1("Coal Plant Emission factor (kg of C02 per TJ)"),
        dcc.Graph(figure=fig),
        html.H2("Annual CO2 (million tonnes / annum)"),
        dcc.Graph(figure=fig2),
        html.H3(),
        dcc.Graph(figure=fig3)
    ]
)

app.run_server(mode='inline')
