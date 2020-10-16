import pandas as pd
import plotly.express as px

import dash 
import dash_core_components as dcc
import dash_html_components as html 
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

#--------------------------------------------------------------------------------------------------------------------------------------------------
# Import and clean data

df = pd.read_csv("bee_data.csv")

df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)


#--------------------------------------------------------------------------------------------------------------------------------------------------
# App Layout

app.layout = html.Div(style={'backgroundColor': "#F7F7F7"},children = [
    html.H1("Map of Bee Colonies", style={'text-align': 'center'}),

    html.H2("Year", style={'text-align': 'left'}),
    dcc.Dropdown(id="slct_year",
                options=[
                    {"label": "2015", "value": 2015},
                    {"label": "2016", "value": 2016},
                    {"label": "2017", "value": 2017},
                    {"label": "2018", "value": 2018}],
                multi=False,
                value=2015,
                style={'width': "40%"}
                ),
    html.H2("Affected by", style={'text-align': 'left'}),
    dcc.Dropdown(id="afft_by",
                options=[
                    {"label": "Disease", "value": "Disease"},
                    {"label": "Varroa_mites", "value": "Varroa_mites"},
                    {"label": "Pesticides", "value": "Pesticides"},
                    {"label": "Pests_excl_Varroa", "value": "Pests_excl_Varroa"},
                    {"label": "Unknown", "value": "Unknown"},
                    {"label": "Other", "value": "Other"}],
                multi=False,
                value="Varroa_mites",
                style={'width': "40%"}
                ),
    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_map', figure={})
])

#--------------------------------------------------------------------------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
    Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value'),
    Input(component_id='afft_by', component_property='value')]
)
def update_graph(option_year, option_cause):
    print(option_year)
    print(type(option_year))
    print(option_cause)
    print(type(option_cause))

    container = f""

    dff = df.copy()
    dff = dff[dff['Year'] == option_year]
    dff = dff[dff['Affected by'] == option_cause]

    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope='usa',
        color='Pct of Colonies Impacted',
        hover_data=['State', 'Pct of Colonies Impacted'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
        template='plotly_dark'
    )

    return container, fig

if __name__ == '__main__':
    app.run_server(debug=True)




