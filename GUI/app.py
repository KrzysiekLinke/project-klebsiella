import base64

import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import dash_daq as daq
import torch


# ======= Creation of the App & Server =======
from GUI.read_files import read_files

app = dash.Dash(
    __name__
)

server = app.server


app.config["suppress_callback_exceptions"] = True

# =============

# ======= Reading imagies from disc =======

data = read_files()

# =============

# ======= Banner =======

def createBanner():
    return html.Div(
        id="dssBanner",
        className="dssBanner",
        children=[
            html.Div(
                id="bannerText",
                children=[
                    html.H5("Plant Village DSS"),
                    html.H6("Predicting Infection on Leaves"),
                ],
            ),
            html.Div(
                id="dssLogo",
                children=[
                    html.Button(
                        id="Help_button", children="HELP", n_clicks=0
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
                        id="mainTab",
                        label="Visualisations",
                        value="tab1",
                        className="tabsStyle",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="infectedTab",
                        label="Images of Infected Leaves",
                        value="tab2",
                        className="tabsStyle",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="healthyTab",
                        label="Images of Healthy Leaves",
                        value="tab3",
                        className="tabsStyle",  # when not hovering over tab
                        selected_className="custom-tab--selected",  # when hovering over tab
                    ),
                ],
            )
        ],
    )


# =============



# ======= Grid Visualisations Tab =======

def countDiv():
    return html.Div(

        id = 'countDiv',
        className = 'countDiv',
        children = [
            html.Div(
                id = 'countBanner',
                className = 'countBanner',
                children = "Number of Infected Leaves Per Plant Type"
            ),

            html.Div(
                id = 'countList',
                className = 'countList',
                children=[
                    html.Div(
                        id = 'countDiv',
                        className = 'countDiv',
                        children=[
                            html.P("# Bacterial Spots"),
                            daq.LEDDisplay(
                                id="countDisplay",
                                value = 17,
                                color = '#FFFFFF',
                                backgroundColor="#000000",
                                size=50
                            )
                        ]

                    )
                ]
            )
        ]
    )

def probChart():
    return html.Div(

        dcc.Graph(
            id='probGraph',
            figure={
                'data': [
                    {'x': ['0-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90-100'],
                     'y': [5,5,5,5,5,5,5,5,5,5],
                     'type': 'bar', 'name': 'probGraph'},

                ],
                'layout': {
                    'title': 'Probability Plot Model Result'
                }
            }
        )
    )

def barChart():
    return html.Div(

        dcc.Graph(
            id='barChart',
            figure={
                'data': [
                    {'x': ['Healthy', 'Infected'],
                     'y': [5,5],
                     'type': 'bar', 'name': 'probGraph'},

                ],
                'layout': {
                    'title': 'Bar Plot # Infected Leaves'
                }
            }
        )
    )

def pieChart():
    return html.Div(
        dcc.Graph(
            id='pieChart',
            figure={
                'data': [
                    {'labels': ['Healthy', 'Infected'],
                     'values': [0.5, 0.5],
                     'type': 'pie', 'name': 'probGraph'},

                ],
                'layout': {
                    'title': 'PieChart Distribution Infected Leaves'
                }
            }
        )


        )

# =============

# ======= Input Test Files Tab =======

def visualisationsTab():
    return (
        html.Div(
            id = 'visualisationPage',
            className = 'visualisationPage',
            children = [
            countDiv(),
            probChart(),
            barChart(),
            pieChart()
        ])
    )


# =============

# ======= Infected Tab =======

def infected_tab():
    return (
        html.Div([
            html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(open(data.loc[2,'path'], 'rb').read())))
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
    [Input("Help_button", "n_clicks"), Input("markdown_close", "n_clicks")],
)
def update_click_output(button_click, close_click):
    ctx = dash.callback_context

    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "Help_button":
            return {"display": "block"}

    return {"display": "none"}


# =============

# ======= Render Tabs =======

@app.callback(Output("app-content", "children"),
              [Input("tabsStyle", "value")]
              )
def render_tab_content(tab_switch):
    if tab_switch == "tab1":
        return visualisationsTab()
    elif tab_switch == "tab2":
        return infected_tab()
    #elif tab_switch == "tab3":
    #    return healthyTab()
    return html.P("SOS SEND HELP")



# =============

# ======= Running Server =======

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)

# =============