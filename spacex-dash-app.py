# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

min_payload = df['Payload Mass (kg)'].min()
max_payload = df['Payload Mass (kg)'].max()
site_options = [{'label': 'All Sites', 'value': 'ALL'}] + [
    {'label': site, 'value': site}
    for site in df['Launch Site'].unique()
]
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TASK 1: dropdown
    dcc.Dropdown(
        id='site-dropdown',
        options=site_options,
        value='ALL',
        placeholder="Select a Launch Site",
        searchable=True
    ),
    html.Br(),

    # TASK 2: pie chart
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    # TASK 3: payload slider
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload, max=max_payload, step=100,
        marks={int(min_payload): str(int(min_payload)),
               int(max_payload): str(int(max_payload))},
        value=[min_payload, max_payload]
    ),
    html.Br(),

    # TASK 4: scatter chart
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # show total successful launches by site
        fig = px.pie(
            df,
            names='Launch Site',
            values='class',
            title='Total Successful Launches by Site'
        )
    else:
        # filter for the selected site
        filtered = df[df['Launch Site'] == selected_site]
        # count success vs failures
        outcome = filtered['class'].value_counts().reset_index()
        outcome.columns = ['Outcome', 'Count']
        outcome['Outcome'] = outcome['Outcome'].map({1: 'Success', 0: 'Failure'})
        fig = px.pie(
            outcome,
            names='Outcome',
            values='Count',
            title=f'Success vs. Failure for site {selected_site}'
        )
    return fig

@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # show total successful launches by site
        fig = px.pie(
            df,
            names='Launch Site',
            values='class',
            title='Total Successful Launches by Site'
        )
    else:
        # filter for the selected site
        filtered = df[df['Launch Site'] == selected_site]
        # count success vs failures
        outcome = filtered['class'].value_counts().reset_index()
        outcome.columns = ['Outcome', 'Count']
        outcome['Outcome'] = outcome['Outcome'].map({1: 'Success', 0: 'Failure'})
        fig = px.pie(
            outcome,
            names='Outcome',
            values='Count',
            title=f'Success vs. Failure for site {selected_site}'
        )
    return fig

@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [
        Input('site-dropdown', 'value'),
        Input('payload-slider', 'value')
    ]
)
def update_scatter(selected_site, payload_range):
    low, high = payload_range
    mask = (df['Payload Mass (kg)'] >= low) & (df['Payload Mass (kg)'] <= high)

    if selected_site == 'ALL':
        filtered = df[mask]
    else:
        filtered = df[(df['Launch Site'] == selected_site) & mask]

    fig = px.scatter(
        filtered,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Payload vs. Outcome',
        labels={'class': 'Launch Outcome (1=Success, 0=Fail)'}
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)


# Run the app
if __name__ == '__main__':
    app.run()

import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# 1. Load data
df = pd.read_csv("spacex_launch_dash.csv")

# 2. Payload bounds
min_payload = df['Payload Mass (kg)'].min()
max_payload = df['Payload Mass (kg)'].max()

# 3. Dropdown options
site_options = [{'label': 'All Sites', 'value': 'ALL'}] + [
    {'label': site, 'value': site}
    for site in df['Launch Site'].unique()
]

# 4. Initialize app
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TASK 1
    dcc.Dropdown(
        id='site-dropdown',
        options=site_options,
        value='ALL',
        placeholder="Select a Launch Site",
        searchable=True
    ),
    html.Br(),

    # TASK 2
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    # TASK 3
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload, max=max_payload, step=100,
        marks={int(min_payload): str(int(min_payload)),
               int(max_payload): str(int(max_payload))},
        value=[min_payload, max_payload]
    ),
    html.Br(),

    # TASK 4
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# PIE CHART CALLBACK
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(
            df,
            names='Launch Site',
            values='class',
            title='Total Successful Launches by Site'
        )
    else:
        filtered = df[df['Launch Site'] == selected_site]
        outcome = filtered['class'].value_counts().reset_index()
        outcome.columns = ['Outcome', 'Count']
        outcome['Outcome'] = outcome['Outcome'].map({1: 'Success', 0: 'Failure'})
        fig = px.pie(
            outcome,
            names='Outcome',
            values='Count',
            title=f'Success vs. Failure for site {selected_site}'
        )
    return fig

# SCATTER CHART CALLBACK
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [
        Input('site-dropdown', 'value'),
        Input('payload-slider', 'value')
    ]
)
def update_scatter(selected_site, payload_range):
    low, high = payload_range
    mask = (df['Payload Mass (kg)'] >= low) & (df['Payload Mass (kg)'] <= high)

    if selected_site == 'ALL':
        filtered = df[mask]
    else:
        filtered = df[(df['Launch Site'] == selected_site) & mask]

    fig = px.scatter(
        filtered,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Payload vs. Outcome',
        labels={'class': 'Launch Outcome (1=Success, 0=Fail)'}
    )
    return fig

# RUN SERVER
if __name__ == '__main__':
    app.run_server(debug=True)

import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# 1. Load data
df = pd.read_csv("spacex_launch_dash.csv")

# 2. Payload bounds
min_payload = df['Payload Mass (kg)'].min()
max_payload = df['Payload Mass (kg)'].max()

# 3. Dropdown options
site_options = [{'label': 'All Sites', 'value': 'ALL'}] + [
    {'label': site, 'value': site}
    for site in df['Launch Site'].unique()
]

# 4. Initialize app
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TASK 1
    dcc.Dropdown(
        id='site-dropdown',
        options=site_options,
        value='ALL',
        placeholder="Select a Launch Site",
        searchable=True
    ),
    html.Br(),

    # TASK 2
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    # TASK 3
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload, max=max_payload, step=100,
        marks={int(min_payload): str(int(min_payload)),
               int(max_payload): str(int(max_payload))},
        value=[min_payload, max_payload]
    ),
    html.Br(),

    # TASK 4
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# PIE CHART CALLBACK
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(
            df,
            names='Launch Site',
            values='class',
            title='Total Successful Launches by Site'
        )
    else:
        filtered = df[df['Launch Site'] == selected_site]
        outcome = filtered['class'].value_counts().reset_index()
        outcome.columns = ['Outcome', 'Count']
        outcome['Outcome'] = outcome['Outcome'].map({1: 'Success', 0: 'Failure'})
        fig = px.pie(
            outcome,
            names='Outcome',
            values='Count',
            title=f'Success vs. Failure for site {selected_site}'
        )
    return fig

# SCATTER CHART CALLBACK
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [
        Input('site-dropdown', 'value'),
        Input('payload-slider', 'value')
    ]
)
def update_scatter(selected_site, payload_range):
    low, high = payload_range
    mask = (df['Payload Mass (kg)'] >= low) & (df['Payload Mass (kg)'] <= high)

    if selected_site == 'ALL':
        filtered = df[mask]
    else:
        filtered = df[(df['Launch Site'] == selected_site) & mask]

    fig = px.scatter(
        filtered,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Payload vs. Outcome',
        labels={'class': 'Launch Outcome (1=Success, 0=Fail)'}
    )
    return fig

# RUN SERVER
if __name__ == '__main__':
    app.run_server(debug=True)

