import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table

# ======= Creation of the App & Server =======

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

server = app.server


# app.config["suppress_callback_exceptions"] = True

# =============

# ======= Banner =======

def createBanner():
    return html.Div(
        id="banner",
        className="bannerClass",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H5("Plant Village DSS"),
                    html.H6("Predicting Infection on Leaves"),
                ],
            ),
            html.Div(
                id="banner-logo",
                children=[
                    html.Button(
                        id="learn-more-button", children="LEARN MORE", n_clicks=0
                    ),
                    html.Img(id="logo", src=app.get_asset_url("dash-logo-new.png")),
                ],
            ),
        ],
    )


# =============

# ======= Instruction Pop-Up =======

def generate_modal():
    return html.Div(
        id="markdown",
        className="modal",
        children=(
            html.Div(
                id="markdown-container",
                className="markdown-container",
                children=[
                    html.Div(
                        className="close-container",
                        children=html.Button(
                            "Close",
                            id="markdown_close",
                            n_clicks=0,
                            className="closeButton",
                        ),
                    ),
                    html.Div(
                        className="markdown-text",
                        children=dcc.Markdown(
                            children=(
                                """
                        ###### Instruction Manual for Plant Village DSS
                        The DSS is a system that helps the platform identifying leaves with bacterial spots. There are 4 tabs on the page as shown below. For each a small instruction manual will be provided here.
                        ###### File Selection
                        This tab is the default tab for this DSS and the location where a test folder should be uploaded.
                        Clicking on the provided hyperlink will result in the pop-up for file selection from the user's computer.
                        Uploading a correct test folder will result in the creation of the visualisations and activations of the modle within this DSS.
                        The three remaining tabs will change according to the provided upload. 
                        ###### Visualisations
                        As the name suggests, this tab shows all visualisations related to the uploaded file.
                        If none are uploaded, this tab will show the visualisations related to the original dataset.
                        Also all data related to the prediction of the model (count of the number of predicted leaves for instance) is shown in this tab.
                        ###### Images of Infected/Healthy Leaves
                        The images shown in these tabs are the result of the prediction from the model.
                        These images show which leaves are classified as infected and which as healthy.
                        The tabs are divided into the 3 different types of possible leaves within the dataset as well. 
                        Moreover, the ID number of each leaf is shown above/below each picture. 


                        Operators may stop measurement by clicking on `Stop` button, and edit specification parameters by clicking specification tab.
                    """
                            )
                        ),
                    ),
                ],
            )
        ),
    )


# =============

# ======= Tabs =======

def createTabs():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="tabsStyle",
                value="tab1",
                className="tabsStyles",
                children=[
                    dcc.Tab(
                        id="fileTab",
                        label="File Selection",
                        value="tab1",
                        className="tabsStyle",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="mainTab",
                        label="Visualisations",
                        value="tab2",
                        className="tabsStyle",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="infectedTab",
                        label="Images of Infected Leaves",
                        value="tab3",
                        className="tabsStyle",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="healthyTab",
                        label="Images of Healthy Leaves",
                        value="tab4",
                        className="tabsStyle",  # when not hovering over tab
                        selected_className="custom-tab--selected",  # when hovering over tab
                    ),
                ],
            )
        ],
    )


# =============

# ======= Input Test Files Tab =======

def fileTab():
    return (
        html.Div([
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                # Allow multiple files to be uploaded
                multiple=True
            ),
            html.Div(id='output-data-upload')
        ])
    )


# =============

# ======= Input Test Files Tab =======

def visualisationsTab():
    return (
        html.Div([
            html.P("YEEEEET BOIIIIII")
        ])
    )


# =============


# ======= App Overview =======

app.layout = html.Div(
    id="big-app-container",
    children=[
        createBanner(),
        html.Div(
            id="app-container",
            children=[
                createTabs(),
                # Main app
                html.Div(id="app-content"),
            ],
        ),
        generate_modal(),
    ],
)


# =============

# ======= Callback Modal =======


@app.callback(
    Output("markdown", "style"),
    [Input("learn-more-button", "n_clicks"), Input("markdown_close", "n_clicks")],
)
def update_click_output(button_click, close_click):
    ctx = dash.callback_context

    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "learn-more-button":
            return {"display": "block"}

    return {"display": "none"}


# =============

# ======= Render Tabs =======

@app.callback(Output("app-content", "children"),
              [Input("tabsStyle", "value")]
              )
def render_tab_content(tab_switch):
    if tab_switch == "tab1":
        return fileTab()
    elif tab_switch == "tab2":
        return visualisationsTab()
    return html.P("SOS SEND HELP")


# =============

# ======= Running Server =======

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)