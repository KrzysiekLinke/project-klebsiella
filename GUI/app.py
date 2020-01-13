
import pandas as pd
import dash
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from GUI.prepareTable import prepareTable
from GUI.read_files import read_files
from GUI.guiModel import predictInfection
import pathlib


# ======= Creation of the App & Server =======

app = dash.Dash(
    __name__
)

server = app.server
app.config["suppress_callback_exceptions"] = True

# =============

# ======= Backend computations =======

pathTestFolder = str(pathlib.Path(__file__).parent.resolve()) + '/assets/images/'

modelOutput = predictInfection(pathTestFolder)

data = read_files()

data['isInfectedPercentage'],data['isInfectedFlag'] = modelOutput

ranges = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]

df = data.groupby(pd.cut(data['isInfectedPercentage'], ranges)).count()['isInfectedPercentage']
pdDF = pd.DataFrame({'Range' : df.index, 'Count' : df.values})

del df

infectedDF, healthyDF = prepareTable(data,app)

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
                    html.A(href = 'http://www.vu.nl',
                        children = html.Img(
                                    src=app.get_asset_url('VULogo.png'),
                                    style={'height':'100px','width':'100px'}
                                )
                        ),
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
                        children="Manual",
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
                        Uploading a correct test folder will result in the creation of the visualisations and activations of the model within this DSS.
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
                        id='fileSelectionTab',
                        label='File Upload',
                        value='fileSelectionTab',
                        className='tabStyle',
                        selected_className='selectedTab'
                    ),
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
                    )
                ],
            ),
            html.Hr()
        ],
    )


# =============

# ======= Upload File Tab =======

def uploadFileTab():
    return (
        html.Div(
            id = 'uploadContainerDiv',
            className= 'uploadContainerDiv',
            children = [
                dcc.Upload(
                    html.Button(
                        id = 'uploadButton',
                        className='uploadButton',
                        children = 'Upload File'
                    )
                )
            ]
        )
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
                                value = data[['isInfectedFlag']].sum(),
                                color = '#FFFFFF',
                                backgroundColor="#0069A9",
                                size=50,
                                label = 'Number',
                            ),
                            daq.LEDDisplay(
                                id="countDisplayPercentage",
                                className='countDisplayPercentage',
                                value=round(data[['isInfectedFlag']].sum()/len(data),2),
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
                     'y': pdDF['Count'],
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
                    {'x': ['Healthy'],
                     'y': [int(len(data) - data[['isInfectedFlag']].sum())],
                     'type': 'bar', 'name': 'Healthy'},
                    {'x': ['Infected'],
                     'y': [int(data[['isInfectedFlag']].sum())],
                     'type': 'bar', 'name': 'Infected'
                    }

                ],
                'layout': {
                    'title': 'Bar Plot Counting The Number Of Infected Leaves',
                    'xaxis': {
                        'title': 'Predicted Values Images'
                    },
                    'yaxis': {
                        'title': 'Count for each Predicted Value',
                    },
                    'height': '80vh',
                    "titlefont": {
                        "size": 30
                    },
                    'paper_bgcolor': '#E4FED7',
                    'plot_bgcolor': '#E4FED7',
                    'color' : ['blue','orange'],
                    'font': {
                        'color': '#373936'
                    },
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
                     'values': [int(len(data) - data[['isInfectedFlag']].sum()),int(data[['isInfectedFlag']].sum())],#[0.512,0.488],
                     #[round((len(data) - data[['isInfectedFlag']].sum())/len(data),1), round(data[['isInfectedFlag']].sum()/len(data),1)],
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

# ======= Infected Tab =======

def infectedTab():
    return (
        html.Div([
            dbc.Table(infectedDF,
                id='infectedTable',
                className='infectedTable',
                )
            ],
        style = {'align':'centre','marginRight':'auto','marginLeft':'auto','marginTop':'20px'})
    )

# =============

# ======= Healthy Tab =======

def healthyTab():
    return (
        html.Div([
            dbc.Table(healthyDF,
                id='healthyTable',
                className='healthyTable',
                )
            ],
        style = {'align':'centre','marginRight':'50','marginLeft':'50','marginTop':'20px'})
    )

# =============

# ======= Bottom Banner =======

def createLowerBanner():
    return html.Div(
        id="dssLowerBanner",
        className="dssLowerBanner",
        children=[
            html.Div(
                id="assignment",
                className="assignment",
                children= "Deep learning for bacterial spot prediction"
            ),
            html.Div(
                id="group",
                className='group',
                children=[
                    html.Div(
                        id = "groupNumber",
                        className= "GroupNumber",
                        children = 'Group 2'
                    ),
                    html.Div(
                        id = "groupMembers",
                        className= "groupMembers",
                        children =[
                            'Marije Gemmink (2628341)', html.Br(),
                            'Joep van Genderingen (2627749)', html.Br(),
                            'Krzysztof Linke (2674002)', html.Br(),
                            'Daan Schönberger (2566280)', html.Br(),
                            'Tim Vorstenbosch (2588989)'
                        ]
                    ),
                ]
            ),
            html.Div(
                id = "powerButtonDiv",
                className = "powerButtonDiv",
                children=
                    daq.PowerButton(
                        id='powerButton',
                        className = 'powerButton',
                        on=True,
                    ),
            ),
            html.Hr()
        ],
    )


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
        createLowerBanner(),
        #dcc.Interval(id='interval', interval=1000, n_intervals=0),
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
        return infectedTab()
    elif switchTab == "healthyTab":
        return healthyTab()
    elif switchTab == "fileSelectionTab":
        return uploadFileTab()
    else:
        return html.P("SOS SEND HELP")

# =============

# ======= Power Button =======

@app.callback(
    Output("divContainer", "children"),
    [Input("powerButton", "on")]
)
def power_off(powerOn):

    if not powerOn:
        return  html.Div(id = "shutdown", children= "Server Shutdown Active. Please activate the button again to restart the system.")
    else:
        return [createTabs(), html.Div(id="tabContent")]

# =============

# ======= Run Server =======
if __name__ == "__main__":
    app.run_server(debug=True, port=8050)

# =============