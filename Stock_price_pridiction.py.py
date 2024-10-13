# Importing required libraries and modules
import datetime  # Importing datetime module (not used in this code)
import yfinance as yf  # Importing yfinance library to fetch stock data
import dash  # Importing Dash library to create web dashboard
from dash import dcc  # Importing dcc module from Dash for creating dashboard components
from dash import html  # Importing html module from Dash for creating HTML components
from dash.dependencies import Input, Output, State  # Importing Input, Output, and State from Dash for creating callbacks

# Creating a Dash application
app = dash.Dash()
app.title = "Stock Visualization Dashboard"  # Setting the title of the dashboard

# Defining the layout of the dashboard
app.layout = html.Div(children=[
    # Creating a heading for the dashboard
    html.H1("Stock Visualization Dashboard", style={'textAlign': 'center'}),
    html.Hr(),  # Creating a horizontal rule
    
    # Creating a section for entering the stock name
    html.Div([
        html.H4("Please enter the stock name: "),  # Creating a heading for the input field
        dcc.Input(id='input', value='AAPL', type='text', style={'width': '50%'}),  # Creating an input field for entering the stock name
        html.Button('Submit', id='submit-button', n_clicks=0)  # Creating a submit button
    ], style={'textAlign': 'center'}),
    
    # Creating a section for displaying the output graph
    html.Div(id='output-graph', style={'padding': '20px'}),
    
    # Creating a section for selecting the time period
    html.Div([
        html.H4("Select Time Period: "),  # Creating a heading for the dropdown menu
        dcc.Dropdown(  # Creating a dropdown menu for selecting the time period
            id='time-period',
            options=[
                {'label': '1 Day', 'value': '1d'},
                {'label': '5 Days', 'value': '5d'},
                {'label': '1 Month', 'value': '1mo'},
                {'label': '3 Months', 'value': '3mo'},
                {'label': '6 Months', 'value': '6mo'},
                {'label': '1 Year', 'value': '1y'},
                {'label': '2 Years', 'value': '2y'},
                {'label': '5 Years', 'value': '5y'},
                {'label': '10 Years', 'value': '10y'},
                {'label': 'YTD', 'value': 'ytd'},
                {'label': 'Max', 'value': 'max'}
            ],
            value='1y'  # Setting the default value to 1 year
        )
    ], style={'textAlign': 'center', 'padding': '20px'})
])

# Defining a callback function to update the graph
@app.callback(
    Output(component_id='output-graph', component_property='children'),  # Output component is the graph
    [Input(component_id='submit-button', component_property='n_clicks')],  # Input component is the submit button
    [State(component_id='input', component_property='value'),  # State component is the input field
     State(component_id='time-period', component_property='value')]  # State component is the dropdown menu
)
def update_graph(n_clicks, input_data, time_period):
    try:
        # Fetching stock data from Yahoo Finance using yfinance library
        df = yf.download(input_data, period=time_period)
        
        # Creating a graph using Dash's dcc.Graph component
        graph = dcc.Graph(id="example", figure={
            'data': [{'x': df.index, 'y': df['Close'], 'type': 'line', 'name': input_data}],
            'layout': {'title': input_data}
        })
        
        print("graph update successfully")
    except Exception as e:
        # Handling exceptions by displaying an error message
        graph = html.Div("Error Retrieving stock data.")
        print(f'Error: {e}')
    
    return graph

if __name__ == '__main__':
    app.run_server()  # Running the Dash application
