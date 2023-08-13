from dash import Dash, Output, Input, State, dcc
from layout import layout, create_matplotlib_graph
from utils import remove_accents
import geopandas as gpd
from flask_caching import Cache

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]


app = Dash(
    name="Terminaisons",
    external_stylesheets=external_stylesheets,
)
cache = Cache(
    app.server,
    config={
        "CACHE_TYPE": "filesystem",
        "CACHE_DIR": "cache-directory",
    },
)

app.layout = layout()


TIMEOUT = 60


@cache.memoize(timeout=TIMEOUT)
def load_data():
    df_geo = gpd.read_file("a-com2022.json")
    df_geo["pays"] = "France"
    df_geo["libgeo_simple"] = (
        df_geo["libgeo"].str.lower().apply(remove_accents).apply(str)
    )

    france = df_geo.dissolve("pays").reset_index()

    return df_geo, france


df_geo, france = load_data()


@app.callback(
    Output("map", "src"),
    Input("terminaison-input", "values"),
)
def update_image(values):
    if values is None:
        values = []

    name = create_matplotlib_graph(
        df_geo=df_geo,
        france=france,
        terminaisons=values,
    )
    return name


@app.callback(
    Output("download-image", "data"),
    Input("download", "n_clicks"),
    State("map", "src"),
    prevent_initial_call=True,
)
def download_image(n_clicks, src):
    return dcc.send_file(src)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8050,
        debug=True,
    )
