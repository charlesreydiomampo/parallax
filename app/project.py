import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import date

app = Dash(__name__)

df = pd.read_csv("bystation.csv")
raw_data_ = pd.read_csv("Raw Data 2016 - 2022.csv")
#parquet
app.layout = html.Div([
    dcc.Dropdown(
        id='station-dropdown',
        options=[{'label': category, 'value': category} for category in df['Station'].unique()],
        value=df['Station'].unique()[0],  # Set default value
        multi=False,  # Set to True if you want to allow multiple selections
    ),
    html.Br(),
    dcc.DatePickerRange(
        id='my-date-picker-range',
        month_format='MMM Do, YY',
        end_date_placeholder_text='MMM Do, YY',
        start_date=date(2018, 6, 21)
    ),
    html.Br(),
    html.Br(),
    dcc.Graph(id='selected-station-output')
])

# Define callback to update output based on dropdown selection
@app.callback(
    Output('selected-station-output', 'figure'),
    [Input('station-dropdown', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')]
)
def update_output(selected_station, start_date, end_date):
    df = raw_data_
    ###
    #if end_date is not None:
    #   start_date_object = date.fromisoformat(start_date)
    #    df = raw_data_[raw_data_["date_"] <= start_date_object]
    ###
    heatmap_data = df[df["Station"] == selected_station]
    fig = px.imshow(heatmap_data.pivot_table(index = "Time", columns = "weekday", values = "Value",
                                     aggfunc = "sum"))
    fig.update_xaxes(side="bottom", title = "Day of the Week")
    fig.update_layout(title={'text':f'Heatmap for {selected_station}'}, title_x=0.5)
    return fig


if __name__ == '__main__':
    app.run(debug=True)
