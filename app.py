import dash
from dash import dcc
from dash import html
import dash_player as player
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import pathlib

FRAMERATE = 24.0

def load_data(path):
    # Load the dataframe
    video_info_df = pd.read_csv("data.csv",index_col=0)
    return video_info_df

video_info_df = load_data("data.csv")

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "ModzEd"
server = app.server
app.config.suppress_callback_exceptions = True

BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("data").resolve()


# Main App
app.layout = html.Div(
    children=[
        dcc.Interval(id="interval-updating-graphs", interval=1000, n_intervals=0),
        html.Div(id="top-bar", className="row"),
        html.Div(
            className="container",
            children=[
                html.Div(
                    id="left-side-column",
                    className="eight columns",
                    children=[
                        html.Img(
                            id="logo-mobile", src=app.get_asset_url("dash-logo.png")
                        ),
                        html.Div(
                            id="header-section",
                            children=[
                                html.H1("ModzED"),
                                html.H5("Simplifying Online Education"),
                                html.Br(),
                                html.Br(),
                                html.P(
                                    "To get started, for the sample video select the desired operation from the drop down menu"
                                ),
                                html.Ul(
                                    children=[
                                    html.Li("Transcript - View transcript of the uploaded video"),
                                    html.Li("Summary - Reduce a long video into a short, manageable summary."),
                                    html.Li("Important Topics - Learn about the important topics covered in the video"),
                                    html.Li("Lookup Keywords - Search for the desired topic in a video along with its timestamp"),
                                    html.Li("Video Captioning - Get what the video is actually about"),
                                    ],
                                ),
                            ],
                        ),
                        html.Div(
                            className="video-outer-container",
                            children=html.Div(
                                className="video-container",
                                children=player.DashPlayer(
                                    id="video-display",
                                    url="https://www.youtube.com/watch?v=CgFVgp_VCN8",
                                    controls=True,
                                    playing=False,
                                    volume=1,
                                    width="100%",
                                    height="100%",
                                ),
                            ),
                        ),
                        html.Div(
                            className="control-section",
                            children=[
                                html.Div(
                                    className="control-element",
                                    children=[
                                        html.Div(children=["Select Operation:"]),
                                        dcc.Dropdown(
                                            id="dropdown-select-op",
                                            options=[
                                                {
                                                    "label": "Transcript",
                                                    "value": "Transcript",
                                                }, 
                                                {
                                                    "label": "Summary",
                                                    "value": "Summary",
                                                }, 
                                                {
                                                    "label": "Important Topics",
                                                    "value": "Topics",
                                                },   
                                                {
                                                    "label": "Lookup",
                                                    "value": "Lookup",
                                                },   
                                                {
                                                    "label": "Video Captions",
                                                    "value": "Caption",
                                                },                                                
                                            ],
                                            value="Select Any Option",
                                            clearable=False,
                                        ),
                                    ],
                                ),
                                
                            ],
                            
                        ),
                    ],
                    
                    
                ),
                html.Div(
                    id="right-side-column",
                    className="four columns",
                    children=[
                        html.Div(
                            className="img-container",
                            children=html.Img(
                                id="logo-web", src=app.get_asset_url("dash-logo.png")
                            ),
                        ),
                        html.Div(id="div-visual-mode"),
                        
                    ],
                ),
            ],
        ),
    ]
)

@app.callback(
    Output("div-visual-mode", "children"),
    [Input("dropdown-select-op", "value")]
)
def reset_threshold_center(value):
    if value == "Transcript":
        return video_info_df.iloc[0].values
    if value == "Summary":
        return video_info_df.iloc[1].values
    if value == "Topics":
        return video_info_df.iloc[2].values
    if value == "Lookup":
        return video_info_df.iloc[3].values
    if value == "Caption":
        return video_info_df.iloc[4].values


# Running the server
if __name__ == "__main__":
    app.run_server(debug=True, port=8053)
