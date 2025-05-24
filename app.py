import dash
from dash import dcc, html, Input, Output, State, dash_table, ctx
import pandas as pd
import base64
import io
from model_utils import load_model

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("30-Day Readmission Risk Prediction Tool", style={
        'textAlign': 'center', 'color': '#003566', 'marginTop': '30px',
        'marginBottom': '20px', 'fontFamily': 'Segoe UI'
    }),

    html.Div([
        html.H4(" Required CSV Format:", style={'textAlign': 'center', 'color': '#001d3d'}),
        dash_table.DataTable(
            data=pd.DataFrame({
                "Column": [
                     "Age", "LOS_days", "Prev_Admissions",
                    "Comorbidity_Score", "Follow_Up", "Discharge_Type", "Gender"
                ],
                "Description": [

                    "Patient age (integer)",
                    "Length of stay (days)",
                    "Number of previous admissions",
                    "Charlson Comorbidity Index score",
                    "Yes / No – Follow-up appointment scheduled?",
                    "Home / Rehab / Nursing Facility",
                    "Male / Female"
                ]
            }).to_dict('records'),
            columns=[{"name": i, "id": i} for i in ["Column", "Description"]],
            style_table={'margin': 'auto', 'width': '90%', 'marginTop': '10px'},
            style_cell={'textAlign': 'center', 'padding': '10px', 'fontFamily': 'Segoe UI'},
            style_header={'backgroundColor': '#0077b6', 'color': 'white', 'fontWeight': 'bold'}
        )
    ], style={"marginBottom": "30px"}),

    html.Div([
        html.H5(" How to Calculate the Comorbidity Score (CCI):", style={'color': '#001d3d'}),
        html.P("The CCI score is based on the presence of chronic conditions. Each condition has a weight as shown below."),
        html.P("Sum the scores manually for each patient and enter the total in your CSV under the column 'Comorbidity_Score'."),
        html.Ul([
            html.Li("1 point: Myocardial infarction"),
            html.Li("1 point: Congestive heart failure"),
            html.Li("1 point: Peripheral vascular disease"),
            html.Li("1 point: Cerebrovascular disease"),
            html.Li("1 point: Dementia"),
            html.Li("1 point: Chronic pulmonary disease"),
            html.Li("1 point: Connective tissue disease–rheumatic disease"),
            html.Li("1 point: Peptic ulcer disease"),
            html.Li("1 point: Mild liver disease"),
            html.Li("1 point: Diabetes without complications"),
            html.Li("2 points: Diabetes with complications"),
            html.Li("2 points: Paraplegia and Hemiplegia"),
            html.Li("2 points: Renal disease"),
            html.Li("2 points: Cancer"),
            html.Li("3 points: Moderate or severe liver disease"),
            html.Li("6 points: Metastatic carcinoma"),
            html.Li("6 points: AIDS/HIV"),
        ], style={'lineHeight': '1.8'}),
        html.P("If you're unsure, consult your clinical documentation or quality team.")
    ], style={
        'backgroundColor': '#f8f9fa',
        'padding': '25px',
        'margin': 'auto',
        'width': '85%',
        'borderRadius': '10px',
        'boxShadow': '0 2px 6px rgba(0,0,0,0.1)',
        'fontFamily': 'Segoe UI',
        'marginBottom': '50px'
    }),

    html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div(['\ud83d\udccc Drag and Drop or Select CSV File']),
            style={
                'width': '70%', 'margin': 'auto', 'padding': '40px',
                'borderWidth': '2px', 'borderStyle': 'dashed',
                'borderRadius': '15px', 'textAlign': 'center',
                'backgroundColor': '#ffffff', 'borderColor': '#0077b6'
            },
            multiple=False
        ),
        html.Button("\u2b07\ufe0f Download Results", id="btn-download", n_clicks=0,
                    style={'marginTop': '20px', 'backgroundColor': '#0077b6', 'color': 'white',
                           'padding': '10px 20px', 'border': 'none', 'borderRadius': '5px'}),
        dcc.Download(id="download-results"),
        html.Div(id='output-table', style={'marginTop': '40px'})
    ])
])

def parse_contents(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    return pd.read_csv(io.StringIO(decoded.decode('utf-8')))

@app.callback(
    Output('output-table', 'children'),
    Input('upload-data', 'contents')
)
def update_output(contents):
    if contents is None:
        return html.Div()

    df = parse_contents(contents)

    if "Comorbidity_Score" not in df.columns:
        return html.Div("\u274c Error: Missing required column 'Comorbidity_Score'.")

    model, cols = load_model()

    try:
        X_input = pd.get_dummies(df, drop_first=False)
        X_input = X_input.reindex(columns=cols, fill_value=0)
        predictions = model.predict(X_input)

        df['Prediction'] = predictions
        df['Prediction'] = df['Prediction'].map({0: "\ud83d\udfe2 No", 1: "\ud83d\udd34 Yes - High Risk"})

        return dash_table.DataTable(
            data=df[[ "Age", "LOS_days", "Prev_Admissions", "Comorbidity_Score", "Gender", "Follow_Up", "Discharge_Type", "Prediction"]].to_dict('records'),
            columns=[{'name': i, 'id': i} for i in [ "Age", "LOS_days", "Prev_Admissions", "Comorbidity_Score", "Gender", "Follow_Up", "Discharge_Type", "Prediction"]],
            style_table={'overflowX': 'auto', 'margin': 'auto', 'width': '95%'},
            style_cell={'textAlign': 'center', 'padding': '10px'},
            style_header={'backgroundColor': '#1f77b4', 'color': 'white'}
        )

    except Exception as e:
        return html.Div(f"\u26a0\ufe0f Unexpected error: {str(e)}")

@app.callback(
    Output("download-results", "data"),
    Input("btn-download", "n_clicks"),
    State("upload-data", "contents"),
    prevent_initial_call=True
)
def download_csv(n_clicks, contents):
    if not contents:
        return

    df = parse_contents(contents)

    if "Comorbidity_Score" not in df.columns:
        return

    model, cols = load_model()
    X_input = pd.get_dummies(df, drop_first=False)
    X_input = X_input.reindex(columns=cols, fill_value=0)
    predictions = model.predict(X_input)
    df['Prediction'] = predictions
    df['Prediction'] = df['Prediction'].map({0: "No", 1: "High Risk"})

    return dcc.send_data_frame(df.to_csv, filename="readmission_predictions.csv", index=False)

if __name__ == '__main__':
    app.run(debug=True)
