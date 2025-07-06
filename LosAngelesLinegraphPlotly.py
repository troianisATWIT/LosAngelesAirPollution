from dash import Dash, dcc, html, Input, Output
import plotly.express as px

app = Dash(__name__)


app.layout = html.Div([
    html.H4('Air Pollution over the past 24 hours in Los Angeles'),
    dcc.Graph(id="line-charts-x-graph"),
    dcc.Checklist(
        id="line-charts-x-checklist",
        options=["Carbon Monoxide", "PM 2.5", "Ground Level Ozone",],
        value=["Los Angeles"],
        inline=True
    ),
])


@app.callback(
    Output("line-charts-x-graph", "figure"),
    Input("line-charts-x-checklist", "value"))
def update_line_chart(country):
    df = px.data.gapminder() # replace with your own data source
    mask = df.country.isin(country)
    fig = px.line(df[mask],
        x="date", y="pollutant", color='country')
    return fig


if __name__ == "__main__":
    app.run(debug=True)
