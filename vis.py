import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
import threading
import time

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='live-graph', animate=True),
    dcc.Interval(
        id='graph-update',
        interval=1000,  # in milliseconds
        n_intervals=0
    ),
])

# Global variables to simulate incoming data
x_data = []
y_data = []
t = 0

# Function to generate new data
def generate_data():
    global t
    while True:
        t += 0.1
        new_x = t
        new_y = np.sin(new_x) + 0.5 * np.sin(3 * new_x)
        x_data.append(new_x)
        y_data.append(new_y)
        time.sleep(1)

# Start a thread to simulate data generation
data_thread = threading.Thread(target=generate_data)
data_thread.start()

@app.callback(Output('live-graph', 'figure'),
              Input('graph-update', 'n_intervals'))
def update_graph_live(n):
    data = go.Scatter(
        x=list(x_data),
        y=list(y_data),
        mode='lines+markers'
    )

    return {'data': [data],
            'layout': go.Layout(xaxis=dict(range=[min(x_data), max(x_data)]),
                                yaxis=dict(range=[min(y_data), max(y_data)]))}

if __name__ == '__main__':
    app.run_server(debug=True)
