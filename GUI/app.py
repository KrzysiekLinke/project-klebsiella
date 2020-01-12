import base64
from io import BytesIO
import pandas as pd

import dash
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from GUI.prepaireTable import prepaireTable
from GUI.read_files import read_files

# ======= Creation of the App & Server =======

app = dash.Dash(
    __name__
)

server = app.server
app.config["suppress_callback_exceptions"] = True


# =============

# ======= Backend computations =======

data = read_files()

infectedTab = prepaireTable(data,app)


# =============

# ======= Banner =======

def createBanner():
    return html.Div(
        id="dssBanner",
        className="dssBanner",
        children=[
            html.Div(
                id="dssLogo",
                className='dssLogo',
                children=
                    html.Img(
                        src=app.get_asset_url('VULogo.png'),
                        style={'height':'100px','width':'100px'})
            ),
            html.Div(
                id="bannerText",
                className='bannerText',
                children=[
                    html.H1("Plant Village DSS"),
                    html.H2("Predicting Infection on Leaves"),
                ],
            ),
            html.Div(
                id="dssFAQ",
                className='dssFAQ',
                children=
                    html.Button(
                        id="faqButton",
                        className='faqButton',
                        children="F. A. Q.",
                        n_clicks=0
                    ),
            ),
            html.Hr()
        ],
    )


# =============

# ======= Instruction Pop-Up =======

def generate_modal():
    return html.Div(
        id="modal",
        className="modal",
        children=[
            html.Div(
                className="modalButtonContainer",
                children=
                    html.Button(
                        id="closeButton",
                        className="closeButton",
                        children = "Close",
                        n_clicks=0
                )
            ),
            html.Div(
                id = "modalText",
                className = "modalText",
                children =
                    dcc.Markdown(

                        '''
                        ## Instruction Manual for Plant Village DSS
                        The DSS is a system that helps the platform identifying leaves with bacterial spots. There are 4 tabs on the page as shown below. For each a small instruction manual will be provided here.
                        #### File Selection
                        This tab is the default tab for this DSS and the location where a test folder should be uploaded.
                        Clicking on the provided hyperlink will result in the pop-up for file selection from the user's computer.
                        Uploading a correct test folder will result in the creation of the visualisations and activations of the modle within this DSS.
                        The three remaining tabs will change according to the provided upload. 
                        #### Visualisations
                        As the name suggests, this tab shows all visualisations related to the uploaded file.
                        If none are uploaded, this tab will show the visualisations related to the original dataset.
                        Also all data related to the prediction of the model (count of the number of predicted leaves for instance) is shown in this tab.
                        #### Images of Infected/Healthy Leaves
                        The images shown in these tabs are the result of the prediction from the model.
                        These images show which leaves are classified as infected and which as healthy.
                        The tabs are divided into the 3 different types of possible leaves within the dataset as well. 
                        Moreover, the ID number of each leaf is shown above/below each picture. 
        
        
                        Operators may stop measurement by clicking on `Stop` button, and edit specification parameters by clicking specification tab.
                        '''

                    )
            )
        ]
    )


# =============

# ======= Creation of Tabs =======

def createTabs():
    return html.Div(
        id="tabsDiv",
        className="tabsDiv",
        children=[
            dcc.Tabs(
                id="tabList",
                value="mainTab",
                className="tabList",
                children=[
                    dcc.Tab(
                        id="mainTab",
                        label="Prediction Results",
                        value="mainTab",
                        className="tabStyle",
                        selected_className="selectedTab",
                    ),
                    dcc.Tab(
                        id="infectedTab",
                        label="Images of Infected Leaves",
                        value="infectedTab",
                        className="tabStyle",
                        selected_className="selectedTab",
                    ),
                    dcc.Tab(
                        id="healthyTab",
                        label="Images of Healthy Leaves",
                        value="healthyTab",
                        className="tabStyle",  # when not hovering over tab
                        selected_className="selectedTab",  # when hovering over tab
                    ),
                ],
            ),
            html.Hr()
        ],
    )


# =============

# ======= Input Test Files Tab =======

def visualisationsTab():
    return (
        html.Div(
            id = 'mainPage',
            className = 'mainPage',
            children = [
            countDiv(),
            probChart(),
            barChart(),
            pieChart()
        ])
    )

# =============

# ======= LED-Display Div =======

def countDiv():
    return html.Div(
        id = 'countDiv',
        className = 'countDiv',
        children = [
            html.Div(
                id = 'countList',
                className = 'countList',
                children=[
                    html.Div(
                        id = 'innerCountDiv',
                        className = 'innerCountDiv',
                        children=[
                            html.Div(
                                id = 'firstTextCountDiv',
                                className = 'firstTextCountDiv',
                                children = ['Number of Infected Leaves', html.Br() ,'Per Plant Type']
                            ),
                            html.Div(
                                id='secondTextCountDiv',
                                className='secondTextCountDiv',
                                children='Count'
                            ),
                            daq.LEDDisplay(
                                id="countDisplay",
                                className='countDisplay',
                                value = 17,
                                color = '#FFFFFF',
                                backgroundColor="#0069A9",
                                size=50,
                                label = 'Number',
                            ),
                            daq.LEDDisplay(
                                id="countDisplayPercentage",
                                className='countDisplayPercentage',
                                value=0.31,
                                color='#FFFFFF',
                                backgroundColor="#0069A9",
                                size=50,
                                label = 'Percentage'
                            )
                        ]
                    )
                ]
            )
        ]
    )

# =============

# ======= Probability Graph Div =======

def probChart():
    return html.Div(
        id = 'probDiv',
        className = 'probDiv',
        children =
        dcc.Graph(
            id='probGraph',
            className = 'probGraph',
            figure={
                'data': [
                    {'x': ['0-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90-100'],
                     'y': [5,5,5,5,5,5,5,5,5,5],
                     'type': 'bar', 'name': 'probGraph'},

                ],
                'layout': {
                    'title': 'Probability Plot Model Result',
                    'xaxis': {
                        'title': 'Probability Ranges'
                    },
                    'yaxis': {
                        'title': 'Number of Leaves'
                    },
                    "titlefont": {
                        "size": 30
                    },
                    'paper_bgcolor': '#E4FED7',
                    'plot_bgcolor': '#E4FED7',
                    'font': {
                        'color': '#373936'
                    }
                }
            }
        )
    )

# =============

# ======= Bar Chart Div =======

def barChart():
    return html.Div(
        id = 'barDiv',
        className ='barDiv',
        children=
        dcc.Graph(
            id='barChart',
            className='barChart',
            figure={
                'data': [
                    {'x': ['Healthy', 'Infected'],
                     'y': [5,5],
                     'type': 'bar', 'name': 'probGraph'},

                ],
                'layout': {
                    'title': 'Bar Plot # Infected Leaves',
                    'xaxis': {
                        'title': 'Predicted Values Images'
                    },
                    'yaxis': {
                        'title': 'Count for each Predicted Value'
                    },
                    'height': '80vh',
                    "titlefont": {
                        "size": 30
                    },
                    'paper_bgcolor': '#E4FED7',
                    'plot_bgcolor': '#E4FED7',
                    'font': {
                        'color': '#373936'
                    }
                }
            }
        )
    )

# =============

# ======= PieChart Div =======

def pieChart():
    return html.Div(
        id='pieDiv',
        className='pieDiv',
        children=
        dcc.Graph(
            id='pieChart',
            className='pieChart',
            figure={
                'data': [
                    {'labels': ['Healthy', 'Infected'],
                     'values': [0.5, 0.5],
                     'type': 'pie', 'name': 'probGraph'},

                ],
                'layout': {
                    'title': 'PieChart Distribution Infected Leaves',
                    "titlefont": {
                        "size": 30
                    },
                    'paper_bgcolor': '#E4FED7',
                    'font': {
                        'color': '#373936'
                    }
                }
            }
        )
    )

# =============
# =============

# ======= Infected Tab =======

def infected_tab():
    return (
        html.Div([
            dbc.Table(infectedTab,
                id='infectedTable',
                className='infectedTable',
                )
            ],
        style = {'align':'centre','marginRight':'auto','marginLeft':'auto','marginTop':'20px'})
    )

# =============

# ======= Healthy Tab =======

def healthy_tab():
    return (
        html.Div([
            dbc.Table(infectedTab,
                id='healthyTable',
                className='healthyTable',
                )
            ],
        style = {'align':'centre','marginRight':'auto','marginLeft':'auto','marginTop':'20px'})
    )

# =============



# ======= App Overview =======

app.layout = html.Div(
    id="appContainer",
    children=[
        createBanner(),
        html.Div(
            id="divContainer",
            children=[
                createTabs(),
                html.Div(id="tabContent"),
            ],
        ),
        generate_modal(),
    ],
)


# =============

# ======= Callback Modal =======


@app.callback(
    Output("modal", "style"),
    [Input("faqButton", "n_clicks"), Input("closeButton", "n_clicks")],
)
def update_click_output(button_click, close_click):
    ctx = dash.callback_context

    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "faqButton":
            return {"display": "block"}

    return {"display": "none"}


# =============

# ======= Render Tabs =======

@app.callback(Output("tabContent", "children"),
              [Input("tabList", "value")]
              )
def render_tab_content(switchTab):
    if switchTab == "mainTab":
        return visualisationsTab()
    elif switchTab == "infectedTab":
        return infected_tab()
    #elif switchTab == "healthyTab":
    #    return healthyTab()
    return html.P("SOS SEND HELP")


# =============

# ======= Running Server =======

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)

# =============