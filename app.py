import altair as alt
from dash import Dash, dcc, html, Input, Output
import pandas as pd

alt.data_transformers.disable_max_rows()

# cars = data.cars()

data = pd.read_csv(
    "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-01-21/spotify_songs.csv"
)


def plot_altair(xrange):
    chart = (
        (
            alt.Chart(data[data["track_popularity"].between(xrange[0], xrange[1])])
            .mark_bar()
            .encode(
                y=alt.Y("playlist_genre", title="Genre", sort="-x"),
                x="count()",
            )
        )
        .properties(width=800, height=400)
        .configure_axis(labelFontSize=20, titleFontSize=20)
    )
    return chart.to_html()


app = Dash(
    __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
)
server = app.server

app.layout = html.Div(
    [
        html.Iframe(
            id="scatter",
            srcDoc=plot_altair(xrange=[50, 100]),
            style={"border-width": "0", "width": "100%", "height": "600px"},
        ),
        html.Div("Popularity range:"),
        dcc.RangeSlider(id="xslider", value=[50, 100], min=0, max=100),
    ]
)


@app.callback(Output("scatter", "srcDoc"), Input("xslider", "value"))
def update_output(xrange):
    return plot_altair(xrange)


if __name__ == "__main__":
    app.run_server(debug=True)
