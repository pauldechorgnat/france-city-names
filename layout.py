import os
from dash import html, dcc

# import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib
from multi_text_input import MultiTextInput

matplotlib.use("agg")
# plt.style.use("dark_background")


def layout():
    return html.Div(
        [
            html.H1("Carte des terminaisons"),
            MultiTextInput(
                id="terminaison-input",
                value="",
                values=[],
                placeholder="Appuyez sur Enter pour valider",
            ),
            # dcc.Graph(id="map")
            html.Center(html.Img(id="map", src="assets/images/france__dark.jpeg")),
            html.Button("Download", id="download"),
            dcc.Download(id="download-image"),
        ]
    )


def create_matplotlib_graph(df_geo, france, terminaisons=[], background="dark"):
    name = "france_" + "_".join(sorted(terminaisons))
    name += f"_{background}"
    name = f"assets/images/{name}.png"
    if background == "dark":
        plt.style.use("dark_background")

    if not os.path.exists(name):
        print("Creating new graph")
        df_geo["terminaison"] = None

        for t in terminaisons:
            df_geo.loc[
                df_geo["libgeo_simple"].apply(lambda x: x[-len(t) :] == t),
                "terminaison",
            ] = t

        fig, ax = plt.subplots(1, 1, figsize=(10, 10))

        france.plot(ax=ax, legend=False, color="#F0F0F0")
        if (len(terminaisons) != 0) and (df_geo["terminaison"].notna().sum() > 0):
            df_geo.plot("terminaison", ax=ax, legend=True)

        ax.axis("off")

        plt.savefig(name)
    else:
        print("Using already computed map")
    return name

    plt.savefig("assets/images/")


# def get_map(df, terminaisons=[]):
#     terminaisons = sorted(terminaisons, key=len, reverse=True)

#     df["terminaison"] = None

#     for t in terminaisons:
#         df.loc[
#             df["libgeo_simple"].apply(lambda x: x[-len(t) :] == t), "terminaison"
#         ] = t

#     fig = px.scatter(
#         data_frame=df,
#         x="xcl2154",
#         y="ycl2154",
#         color="terminaison",
#         height=1000,
#         width=1000,
#     )
#     fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")

#     return fig
