import subprocess, sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "dash", "dash_daq", "dash-bootstrap-components", "keras", "tensorflow"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "scipy", "--upgrade"])

import pandas as pd
import dash
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from prepareTable import prepareTable
from read_files import read_files, findFilePath
from guiModel import predictInfection
from distributionTab import distributionTab
from visualisationsTab import visualisationsTab
import pathlib
import time
import numpy as np
import glob

# ======= Creation of the App & Server =======
app = dash.Dash(name='DSS Spotting Bacteria')

server = app.server
app.config["suppress_callback_exceptions"] = True

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

data, pdDF, infectedDF, healthyDF, dataset, lossList = pd.DataFrame(), None, None, None, None, None

# =============

# ======= Backend computations =======

def computeBackend(pathTestFolder):
    image_path = glob.glob(pathTestFolder + "/*")

    dataDF, error2 = read_files(pathTestFolder)

    if error2:
        pathTestFolder = str(pathlib.Path(__file__).parent.resolve()) + '/assets/images/'
        dataDF, _ = read_files(pathTestFolder)

    modelOutput = predictInfection(pathTestFolder)

    dataDF['isInfectedPercentage'], dataDF['isInfectedFlag'] = modelOutput
    dataDF['id'] = dataDF['id'].astype(int) + 1

    ranges = np.linspace(-0.000000000000000001, 1, 11)

    df = dataDF.groupby(pd.cut(dataDF['isInfectedPercentage'], ranges)).count()['isInfectedPercentage']
    pd_df = pd.DataFrame({'Range': df.index, 'Count': df.values})

    readDF = dataDF.copy(deep=True)
    readDF['id'] = '#' + dataDF['id'].astype(str)
    readDF.to_csv(str(pathlib.Path(__file__).parent.resolve()) + '/assets/imagesTextFile.csv', sep=';',index=False)

    del df, readDF

    infected, healthy = prepareTable(dataDF, pathTestFolder)

    return dataDF, pd_df, infected, healthy, error2, error2


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
                html.A(href='http://www.vu.nl',
                       children=html.Img(
                           src=app.get_asset_url('VULogo.png'),
                           style={'height': '100px', 'width': '100px'}
                       )
                       ),
            ),
            html.Div(
                id="bannerText",
                className='bannerText',
                children=[
                    html.H1("DSS Leaf Infection"),
                    html.H2("Predicting Bacterial Spots on Leaves"),
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
                    children="Close",
                    n_clicks=0
                )
            ),
            html.Div(
                id="modalText",
                className="modalText",
                children=
                dcc.Markdown(

                    '''
                    ## Instruction Manual for Plant village DSS

                    The DSS is a system that helps the platform identifying leaves with bacterial spots. 
                    There are 5 tabs on the page as shown below. For each a small instruction manual will be provided here.

                    ### File Selection
                    This tab is the default tab for this DSS and the location where the test folder should be uploaded. 
                    Clicking on the provided button or dragging files to the bordered area will result in the search for the corresponding parent directory. 
                    The tab pages related to the prediction will change accordingly when a new file is uploaded. 
                    A standard folder will be selected when there is no new upload. This standard directory is based on the original training data.

                    ### Prescriptive Data
                    The distribution of the provided data is visualised on this tab page. 
                    The LED-displays show the number of leaves with bacterial spots and the probability that a random leaf within the folder is infected with bacterial spots. 
                    The distribution of the classes per type of leaf are shown in both the bar chart and three pie charts. 
                    Moreover, some model statistics are also shown to give the user an idea of how well the model performs.

                    ### Prediction Results
                    As the name suggests, this tab shows all visualisations related to the uploaded file, or in other words the predictive data. 
                    The distribution of the images with and without bacterial spots will be given on this page.  
                    The LED-displays have the exact same meaning as previously described, as well as the bar plot and pie chart. 
                    A probability graph is also given, which shows the number of images that fall into one of the given probability ranges. 
                    Therefore, if the model is 70% sure that the leaf is infected, it will count 1 image towards the range 70-80%. 
                    This is useful to show, since it reflects the model’s performance if the graph shows extreme values in the ranges 0-10% and 90-100%. 
                    If this is the case, the model is fairly sure of its estimations and hence it will perform well generally. 

                    ### Images of Leaves with Bacterial Spots/without Bacterial Spots:
                    The images shown on their respective tab are the images that have been predicted to have bacterial spots or not.
                    These images are depicted in three tables. The tables do not only show the pictures, but also the ID number for each picture (first picture in the folder: ID = 1, second: ID = 2, etc.). 
                    Moreover, the probability of the leaf having bacterial spots or not is also shown in the table. 
                    The order of the table is based on the ID number of each image, reading left to right, top to bottom. 
                    An extra text file is provided, in which also the image names are displayed in addition to the previous columns.
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
                value="fileSelectionTab",
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
                        id='prescriptiveTab',
                        label='Prescriptive Data',
                        value='prescriptiveTab',
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
                        label="Images of Leaves with Bacterial Spots",
                        value="infectedTab",
                        className="tabStyle",
                        selected_className="selectedTab",
                    ),
                    dcc.Tab(
                        id="healthyTab",
                        label="Images of Leaves without Bacterial Spots",
                        value="healthyTab",
                        className="tabStyle",
                        selected_className="selectedTab",
                    )
                ],
            ),
            html.Hr()
        ],
    )


# =============

# ======= Upload File Tab =======

def uploadFileTab():
    return (html.Div(
        id='uploadContainer',
        className='uploadContainer',
        children=[
            html.Br(),
            html.Div(
                id='textContainer',
                className='textContainer',
                children=[
                    html.Br(),
                    html.Div(
                        id='uploadText',
                        className='uploadText',
                        children=html.H2("Instruction Manual Uploading Image Folder")

                    ),
                    html.H3(
                        'Dash cannot upload a folder directly. Instead, this page will provide a way to search for this folder.'),
                    html.H3('In order to make this work, please adhere to the following guidelines:'),
                    html.Div(
                        id='fileUploadText',
                        className='fileUploadText',
                        children=[
                            dcc.Markdown(
                                '''
    
                                -   Upload a file from the directory that needs to be read. The program will try to find the folder.
    
                                -   The user can either click on the button or drag files to the bordered part of the page to upload files.
    
                                -   The folder must be located inside the project folder. This can only be done within the project folder due to security reasons. 
                                    This folder can be placed anywhere inside of the project folder.
    
                                -   Make sure the file name within the test folder is unique in the project directory, the program may find another folder otherwise. 
    
                                -   Another way of uploading the folder is by deleting the “images” folder inside the GUI directory and renaming the user’s folder to this name. 
                                    Using this method, the program can directly access the new image folder without having to upload or drag any files. 
                                    However, do this with caution, as the program will crash if there is no folder “images” within the directory assets.
    
                                -   The standard folder will be shown if no file is uploaded. When the upload fails to find the new directory, an error message will be displayed. 
                                    The standard folder includes some data on which the model is trained and is mostly just for show.
    
                                '''),
                            html.Br()
                        ]
                    )
                ]
            ),
            html.Br(), html.Br(),
            dcc.Upload(
                id='uploadData',
                className='uploadData',
                multiple=True,
                children=
                html.Button(
                    id='uploadButton',
                    className='uploadButton',
                    children='Upload Button',
                    n_clicks=0
                )
                ,
                style={
                    'width': '20%',
                    'height': '0px',
                    'animation': 'none',
                    'display': 'block',
                    'position': 'absolute',
                    'left': '40%',
                    'right': '40%'
                }
            ),
            html.Br(), html.H2("OR"), html.Br(),
            dcc.Upload(
                id='dragData',
                className='dragData',
                children=html.Div(id='dragText', className='dragText', children='Drag & Drop Files Here'),
                multiple=True,
                disable_click=True,
                style={
                    'width': '99.7%',
                    'height': '86px',
                    'text-align': 'center',
                    'margin-top': '-35px',
                    'padding-top': '-20px',
                    'top': '-100px'
                }
            ),
        ]
    )
    )


# =============

# ======= Infected Tab =======

def infectedTab():
    return (
        html.Div(
            className='infectedDiv',
            children=[
                dbc.Table(infectedDF[0],
                          id='infectedTable1',
                          className='infectedTable1',
                          ),

                dbc.Table(infectedDF[1],
                          id='infectedTable2',
                          className='infectedTable2',
                          ),
                dbc.Table(infectedDF[2],
                          id='infectedTable3',
                          className='infectedTable3',
                          ),
            ],
        )
    )


# =============

# ======= Healthy Tab =======

def healthyTab():
    return (
        html.Div(
            className='healthyDiv',
            children=[
                dbc.Table(healthyDF[0],
                          id='healthyTable1',
                          className='healthyTable1',
                          ),
                dbc.Table(healthyDF[1],
                          id='healthyTable2',
                          className='healthyTable2',
                          ),
                dbc.Table(healthyDF[2],
                          id='healthyTable3',
                          className='healthyTable2',
                          ),
            ],
        )
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
                children="Deep Learning for predicting bacterial spots on leaves"
            ),
            html.Div(
                id="group",
                className='group',
                children=[
                    html.Div(
                        id="groupNumber",
                        className="GroupNumber",
                        children='Group 2'
                    ),
                    html.Div(
                        id="groupMembers",
                        className="groupMembers",
                        children=[
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
                id="powerButtonDiv",
                className="powerButtonDiv",
                children=
                daq.PowerButton(
                    id='powerButton',
                    className='powerButton',
                    on=True,
                ),
            ),
        ],
    )


# ======= App Overview =======
def appContainer(pathTestFolder, error):
    global data, pdDF, infectedDF, healthyDF, dataset, lossList
    data, pdDF, infectedDF, healthyDF, error2, error3 = computeBackend(pathTestFolder)
    dataset = pd.read_pickle("Prescriptive_data_nn.pkl")
    lossList = pd.read_pickle("TL_chart")


    return (
        html.Div(
            id="appContainer",
            children=[
                createBanner(),
                dcc.Loading(
                    id='loading',
                    className='loading',
                    type='cube',
                    fullscreen=False,
                    children=[
                        html.Div(
                            id="divContainer",
                            children=[
                                createTabs(),
                                html.Div(id="tabContent"),
                            ]
                        )],
                    style={
                        "background-color": "#E4FED7",
                        "margin-top": "175px",
                        "margin-bottom": "175px"
                    }
                ),
                generate_modal(),
                createLowerBanner(),
                dcc.ConfirmDialog(id='dialogue', message="File Not Found, Using Default Directory", displayed=error),
                dcc.ConfirmDialog(id='dialogue2',
                                  message="Folder has no images, please insert images into this directory for it to be analysed",
                                  displayed=error3),
                html.Div(id='fakeDiv'),
            ]
        )
    )


def layoutApp():
    pathTestFolder = str(pathlib.Path(__file__).parent.resolve()) + '/assets/images/'
    error = False
    return html.Div(id='layoutContainer', children=appContainer(pathTestFolder, error))


app.layout = layoutApp


# =============

# ======= Callback Modal =======

@app.callback(
    Output("modal", "style"),
    [Input("faqButton", "n_clicks"), Input("closeButton", "n_clicks")],
)
def update_click_output(_, __):
    buttonPress = dash.callback_context

    if buttonPress.triggered:
        actionID = buttonPress.triggered[0]["prop_id"].split(".")[0]
        if actionID == "faqButton":
            return {"display": "block"}

    return {"display": "none"}


# =============

# ======= Render Tabs =======

@app.callback(Output("tabContent", "children"),
              [Input("tabList", "value")]
              )
def render_tab_content(switchTab):
    time.sleep(1.3)
    if switchTab == "mainTab":
        return visualisationsTab(data, pdDF)
    elif switchTab == "infectedTab":
        return infectedTab()
    elif switchTab == "healthyTab":
        return healthyTab()
    elif switchTab == "fileSelectionTab":
        return uploadFileTab()
    elif switchTab == "prescriptiveTab":
        return distributionTab(dataset, lossList)
    else:
        return html.P("This Error Should Never Occur")


# =============

# ======= Search File Button =======

@app.callback(Output('layoutContainer', 'children'),
              [Input('uploadData', 'contents'), Input('dragData', 'contents')],
              [State('uploadData', 'filename'), State('dragData', 'filename')])
def uploadFile(list_of_contents, list_of_contents2, list_of_names, list_of_names2):
    pathTestFolder = str(pathlib.Path(__file__).parent.resolve()) + '/assets/images/'
    error = True
    if list_of_contents is not None or list_of_contents2 is not None:

        if list_of_contents2 is not None:
            nameFirstFile = list_of_names2[0]
        else:
            nameFirstFile = list_of_names[0]

        completeFilePath = findFilePath(nameFirstFile)
        if completeFilePath is not None and completeFilePath is not []:
            pathTestFolder = str(completeFilePath.parent) + '/'
            error = False

    return appContainer(pathTestFolder, error)


# =============

# ======= Power Button =======

@app.callback(
    Output("divContainer", "children"),
    [Input("powerButton", "on")]
)
def power_off(powerOn):
    if not powerOn:
        return html.Div(id="shutdown",
                        children="Server Shutdown Active. Please activate the button again to restart the system.")
    else:
        return [createTabs(), html.Div(id="tabContent")]


# =============

# ======= Run Server =======
if __name__ == "__main__":
    app.run_server(debug=False, port=8050)

# =============
