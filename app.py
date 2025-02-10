from dash import Dash, dcc, html, Input, Output, State, dash_table
import pandas as pd

# Initialize the app
app = Dash(__name__)

# Sample data (initially empty)
data = {
    'Ship Number': [],
    'Drawing Number': [],
    'Drawing Name': [],
    'Scheduled Start': [],
    'Scheduled Finish': [],
    'External Deadline': [],
    'Target Delivery': [],
    'Actual Delivery': [],
    'Status': [],
    'PIC': [],
    'Support Staff': [],
    'Progress': [],
    'Remarks': [],
    'Qtd Mhr': [],
    'Actual Mhr': [],
    'DER': []
}
df = pd.DataFrame(data)

# Layout of the app
app.layout = html.Div([
    html.H1("Job Input Form"),
    
    # Input Form
    html.Div([
        html.Label("Ship Number"),
        dcc.Input(id='ship-number', type='text', placeholder='Enter Ship Number'),
        
        html.Label("Drawing Number"),
        dcc.Input(id='drawing-number', type='text', placeholder='Enter Drawing Number'),
        
        html.Label("Drawing Name"),
        dcc.Input(id='drawing-name', type='text', placeholder='Enter Drawing Name'),
        
        html.Label("Scheduled Start"),
        dcc.Input(id='scheduled-start', type='date', placeholder='Select Scheduled Start'),
        
        html.Label("Scheduled Finish"),
        dcc.Input(id='scheduled-finish', type='date', placeholder='Select Scheduled Finish'),
        
        html.Label("External Deadline"),
        dcc.Input(id='external-deadline', type='date', placeholder='Select External Deadline'),
        
        html.Label("Target Delivery"),
        dcc.Input(id='target-delivery', type='date', placeholder='Select Target Delivery'),
        
        html.Label("Actual Delivery"),
        dcc.Input(id='actual-delivery', type='date', placeholder='Select Actual Delivery'),
        
        html.Label("PIC (Person In Charge)"),
        dcc.Input(id='pic', type='text', placeholder='Enter PIC Name'),
        
        html.Label("Support Staff"),
        dcc.Input(id='support-staff', type='text', placeholder='Enter Support Staff Name'),
        
        html.Label("Progress (%)"),
        dcc.Input(id='progress', type='number', placeholder='Enter Progress (e.g., 50)'),
        
        html.Label("Remarks"),
        dcc.Input(id='remarks', type='text', placeholder='Enter Remarks'),
        
        html.Label("Qtd Mhr"),
        dcc.Input(id='qtd-mhr', type='number', placeholder='Enter Qtd Mhr'),
        
        html.Label("Actual Mhr"),
        dcc.Input(id='actual-mhr', type='number', placeholder='Enter Actual Mhr'),
        
        html.Button('Submit', id='submit-button', n_clicks=0),
    ], style={'display': 'grid', 'gap': '10px'}),
    
    # Display Table
    html.H2("Job List"),
    dash_table.DataTable(
        id='job-table',
        columns=[{"name": col, "id": col} for col in df.columns],
        data=df.to_dict('records'),
        editable=True,
        row_deletable=True,
        style_table={'overflowX': 'auto'}
    )
])

# Callback to handle form submission
@app.callback(
    Output('job-table', 'data'),
    [Input('submit-button', 'n_clicks')],
    [
        State('ship-number', 'value'),
        State('drawing-number', 'value'),
        State('drawing-name', 'value'),
        State('scheduled-start', 'value'),
        State('scheduled-finish', 'value'),
        State('external-deadline', 'value'),
        State('target-delivery', 'value'),
        State('actual-delivery', 'value'),
        State('pic', 'value'),
        State('support-staff', 'value'),
        State('progress', 'value'),
        State('remarks', 'value'),
        State('qtd-mhr', 'value'),
        State('actual-mhr', 'value')
    ]
)
def update_table(n_clicks, ship_number, drawing_number, drawing_name, scheduled_start, scheduled_finish,
                 external_deadline, target_delivery, actual_delivery, pic, support_staff, progress, remarks,
                 qtd_mhr, actual_mhr):
    if n_clicks > 0:
        # Calculate Status based on the formula
        status = "ONGOING"
        if actual_delivery:
            if actual_delivery == external_deadline:
                status = "ON-TIME"
            elif actual_delivery > external_deadline:
                status = "DELAYED"
            elif actual_delivery < external_deadline:
                status = "ADVANCE"
        
        # Calculate DER (Qtd Mhr / Actual Mhr)
        der = None
        if qtd_mhr and actual_mhr:
            der = round((actual_mhr / qtd_mhr) * 100, 2)
        
        # Add new row to the table
        new_row = {
            'Ship Number': ship_number,
            'Drawing Number': drawing_number,
            'Drawing Name': drawing_name,
            'Scheduled Start': scheduled_start,
            'Scheduled Finish': scheduled_finish,
            'External Deadline': external_deadline,
            'Target Delivery': target_delivery,
            'Actual Delivery': actual_delivery,
            'Status': status,
            'PIC': pic,
            'Support Staff': support_staff,
            'Progress': progress,
            'Remarks': remarks,
            'Qtd Mhr': qtd_mhr,
            'Actual Mhr': actual_mhr,
            'DER': der
        }
        
        # Append the new row to the existing data
        global df
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        return df.to_dict('records')
    
    return df.to_dict('records')

# Run the app
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=10000, debug=True)