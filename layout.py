from dash import html, dcc, dash_table

layout = html.Div([
    html.Div(className='card', children=[
        html.H1("📊 30-Day Readmission Risk Tool"),
        html.H4("⬆️ Upload Patient CSV File"),
        dcc.Upload(
            id='upload-data',
            children=html.Div(['Drag & Drop or ', html.A('Select a File')]),
            style={
                'width': '100%', 'height': '60px', 'lineHeight': '60px',
                'borderWidth': '2px', 'borderStyle': 'dashed',
                'borderRadius': '15px', 'textAlign': 'center',
                'margin': '10px auto', 'backgroundColor': '#e0f7fa'
            }
        )
    ]),

    html.Div(className='card', children=[
        html.H4("📋 Expected Format"),
        dash_table.DataTable(id='input-format-table')
    ]),

    html.Div(className='card', children=[
        html.H4("📈 Prediction Result"),
        html.Div(id='prediction-output')
    ])
])
