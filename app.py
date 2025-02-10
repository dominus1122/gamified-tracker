# app.py
from dash import Dash, dcc, html
import pandas as pd

# Sample data
data = {
    'Name': ['John', 'Sarah', 'Mike'],
    'Points': [50, 70, 40]
}
df = pd.DataFrame(data)

# Initialize the app
app = Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("Leaderboard"),  # Title
    dcc.Graph(
        figure={
            'data': [{'x': df['Name'], 'y': df['Points'], 'type': 'bar'}],
            'layout': {'title': 'Team Performance'}
        }
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)