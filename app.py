# Import necessary libraries
import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Initialize Dash app
app = dash.Dash(__name__)

# Load preprocessed ZHVI data into DataFrame
# Assuming data contains your preprocessed ZHVI data
data = pd.read_csv('preprocessed_data.csv')

# Define layout of the dashboard
app.layout = html.Div([
    html.Label('Select a State:'),
    dcc.Dropdown(
        id='state-dropdown',
        options=[],
        value=None,  # No default value initially
        clearable=False  # Prevents the dropdown from being cleared
    ),
    html.Label('Select a Region:'),
    dcc.Dropdown(id='region-dropdown'),
    dcc.Graph(id='zhvi-graph')
])

# Update state dropdown options when the app starts
@app.callback(
    Output('state-dropdown', 'options'),
    Output('state-dropdown', 'value'),
    [Input('state-dropdown', 'value')]
)
def update_state_dropdown(selected_state):
    # Filter out regions with null StateName and "USA" as RegionName
    states = [{'label': state, 'value': state} for state in data[data['StateName'].notnull()]['StateName'].unique()]
    # Set the default value if not selected
    if selected_state is None:
        selected_state = states[0]['value']
    return states, selected_state

# Define callback to update region dropdown based on selected state
@app.callback(
    Output('region-dropdown', 'options'),
    [Input('state-dropdown', 'value')]
)
def update_region_dropdown(selected_state):
    if selected_state is None:
        return []
    # Filter data based on selected state
    filtered_data = data[data['StateName'] == selected_state]
    # Get unique regions for the selected state
    regions = [{'label': region, 'value': region} for region in filtered_data['RegionName'].unique()]
    return regions

# Define callback to update graph based on selected region
@app.callback(
    Output('zhvi-graph', 'figure'),
    [Input('region-dropdown', 'value')]
)
def update_graph(selected_region):
    if not selected_region:
        return {}
    # Filter data based on selected region
    filtered_data = data[data['RegionName'] == selected_region]

    # Prepare data for plotting
    melt_data = filtered_data.melt(id_vars=['RegionName', 'StateName'], var_name='Date', value_name='ZHVI')
    melt_data['Date'] = pd.to_datetime(melt_data['Date'])

    # Plot the data
    fig = px.line(melt_data, x='Date', y='ZHVI',
                  title=f'ZHVI (Zillow Housing Value Index) Trend for {selected_region}')
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
