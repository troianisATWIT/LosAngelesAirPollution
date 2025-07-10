# Past 6 Month Monitored Air Pollution Data (Line Chart) dashboard for Los Angeles County, CA

# Include HTML/CSS

from dash import dash, dcc, html, Input, Output
from flask import Flask
import requests
import plotly.express as px
from dash.dependencies import Input, Output


app = Flask(__name__)

API_KEY = "5c60f307f08a9fe0acd901195430ee0f"

# BASE_URL = f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={start}&end={end}&appid={API_KEY}"

#county_name = 'Los Angeles'
# def get_pollution_data(county):
   # url = BASE_URL + "appid=" + API_KEY + "&q=" + county + "&units=metric"
    # response = requests.get(url)
   # return response.json()

def get_air_pollution(lat, lon):
    pollution_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(pollution_url)

    if response.status_code == 200:
        return response.json()['list'][0]
    else:
        messagebox.showerror("Error", f"Air Pollution API error: {response.status_code}")
        return None
    
def show_air_pollution():
    county = county_entry.get()
    if county:
        coordinates = get_county_coordinates(county)
        if coordinates:
            lat, lon = coordinates

            pollution_data = get_air_pollution(lat, lon)
            if pollution_data:
                update_air_pollution_display(pollution_data)
        else:
            messagebox.showerror("")
    else:
        messagebox.showerror("")


# data = get_pollution_data("Los Angeles")

app = dash.Dash(__name__)


app.layout = html.Div(
    children=[
         html.H1 ('Air Pollution over the past 6 months hours in Los Angeles County, CA'),
         
    dcc.Input(id='county-input', value='Los Angeles County, CA', type='text'),
    html.Select('Retrieve Air Pollution Data', id='submit-button', n_clicks=0),
    html.Div(id='pollution-output'),
    dcc.Graph(id="line-charts-x-graph"),
    dcc.Checklist(
        id="line-charts-x-checklist",
        options=["Carbon Monoxide", "PM 2.5", "Ground Level Ozone",],
        value=["Los Angeles"],
        inline=True
    ),
])





@app.callback(
    Output('pollution-output', 'children'),
    Input('submit-button', 'n_clicks'),
    Input('county-input', 'value')
)

@app.callback(
    Output("line-charts-x-graph", "figure"),
    Input("line-charts-x-checklist", "value"))
def update_line_chart(country):
    df = px.data.gapminder() 
    mask = df.country.isin(country)
    fig = px.line(df[mask],
        x="date", y="pollutant", color='country')
    return fig

# return html.Div([
           # html.P(f"Carbon Monoxide: {county}"),
           # html.P(f"Ground Level Ozone: {county}"),
          #  html.P(f"PM2.5: {county}"),
  #      ])


if __name__ == '__main__':
    app.run(debug=True)

