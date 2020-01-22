import pandas as pd
import dash
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from GUI.prepareTable import prepareTable
from GUI.read_files import read_files, findFilePath
from GUI.guiModel import predictInfection
from GUI.distributionTab import distributionTab
from GUI.visualisationsTab import visualisationsTab
import pathlib
import time
import numpy as np


# ======= Creation of the App & Server =======
app = dash.Dash(name = 'DSS Plant Village')

server = app.server
app.config["suppress_callback_exceptions"] = True

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

data, pdDF,infectedDF,healthyDF,dataset = pd.DataFrame(),None,None,None,None

# =============

# ======= Backend computations =======

def computeBackend(pathTestFolder):

    modelOutput = predictInfection(pathTestFolder)
    dataDF = read_files(pathTestFolder)

    dataDF['isInfectedPercentage'], dataDF['isInfectedFlag'] = modelOutput

    ranges = np.linspace(0,1,11)

    df = dataDF.groupby(pd.cut(dataDF['isInfectedPercentage'], ranges)).count()['isInfectedPercentage']
    pd_df = pd.DataFrame({'Range': df.index, 'Count': df.values})

    del df

    infected, healthy = prepareTable(dataDF, pathTestFolder)

    #infectedDF['isInfectedPercentage'] = str(round(infectedDF['isInfectedPercentage'] * 100,2)) + ' %'

    return dataDF, pd_df,infected,healthy

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
                        id='prescriptiveTab',
                        label='Data Distribution',
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
    return ( html.Div(
        id = 'uploadContainer',
        className='uploadContainer',
        children = [
            html.Br(),
            html.Div(
                id = 'textContainer',
                className = 'textContainer',
                children = [
                    html.Br(),
                    html.Div(
                        id='uploadText',
                        className='uploadText',
                        children=html.H2("Instruction Manual Uploading Image Folder")

                    ),
                    html.H3('Dash cannot upload a folder directly. Instead, this page will provide a way to search for this folder.'),
                    html.H3('In order to make this work, please adhere to the following guidelines:'),
                    html.Div(
                        id='fileUploadText',
                        className='fileUploadText',
                        children=[
                            dcc.Markdown(
                            '''
                                
                            1.  Upload a file from the directory that needs to be read, the program will try to find the folder.
                            2.  The user can either click on the button or drag files to the bordered part of the page to upload files.
                            3.  The folder must be located inside the project folder. This can only be done within the project folder due to security reasons.
                                This folder can be placed anywhere inside of the project folder                       
                            4.  Make sure the file name within the test folder is unique in the project directory, the program may choose another folder otherwise.    
                            5.  Another way of uploading the folder is by deleting the "images" folder inside GUI and renaming the user's folder to this name.
                                Using this method, the program can directly access the new image folder without having to upload or drag any files.
                                However, do this with caution, as the program will crash if there is no folder "images" within the directory assets.                         
                            6.  The standard folder will be shown if no file is uploaded. When the upload fails to find the new directory, an error message will be displayed.
                                The standard folder includes some data on which the model is trained and is mostly just for show.
                            7.  The tab "Data Distribution" will not change and only show the distribution of the original data
                            
                            
                            '''),
                            html.Br()
                        ]
                    )
                ]
            ),
            html.Br(), html.Br(),
            html.Div(
                id = 'uploadButtonContainer',
                className='uploadButtonContainer',
                children=
                    dcc.Upload(
                        id = 'uploadData',
                        className = 'uploadData',
                        multiple=True,
                        children =
                            html.Button(
                                id = 'uploadButton',
                                className = 'uploadButton',
                                children= 'Upload Button',
                                n_clicks = 0
                            )
                        ,
                        style = {
                            'width': '0px',
                            'height': '0px',
                            'animation' : 'none'
                        }
                    ),
            ),
            html.Br(), html.H2("OR"),html.Br(),
            dcc.Upload(
                id='dragData',
                className='dragData',
                children=html.Div(id='dragText',className ='dragText', children = 'Drag & Drop Files Here'),
                multiple = True,
                disable_click = True,
                style = {
                    'width': '99.7%',
                    'height': '86px',
                    'text-align': 'center',
                    'margin-top' : '-35px',
                    'padding-top': '-20px',
                    'top' : '-100px'
                }
            )
        ]
    )
)

# =============

# ======= Infected Tab =======

def infectedTab():
    firstDF = str(round(infectedDF[0]['isInfectedPercentage']*100,2)) + ' %'
    secondDF = str(round(infectedDF[1]['isInfectedPercentage']*100,2)) + ' %'
    thirdDF = str(round(infectedDF[2]['isInfectedPercentage']*100,2)) + ' %'
    return (
        html.Div(
            className='infectedDiv',
            children = [
            dbc.Table(firstDF,
                      id='infectedTable1',
                      className='infectedTable1',
                      ),

            dbc.Table(secondDF,
                      id='infectedTable2',
                      className='infectedTable2',
                      ),
            dbc.Table(thirdDF,
                      id='infectedTable3',
                      className='infectedTable3',
                      ),
        ],
        )
    )


# =============

# ======= Healthy Tab =======

def healthyTab():
    firstDF = str(round(healthyDF[0]['isInfectedPercentage']*100,2)) + ' %'
    secondDF = str(round(healthyDF[1]['isInfectedPercentage']*100,2)) + ' %'
    thirdDF = str(round(healthyDF[2]['isInfectedPercentage']*100,2)) + ' %'
    return (
        html.Div(
            className='healthyDiv',
            children =[
            dbc.Table(firstDF,
                      id='healthyTable1',
                      className='healthyTable1',
                      ),
            dbc.Table(secondDF,
                      id='healthyTable2',
                      className='healthyTable2',
                      ),
            dbc.Table(thirdDF,
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
                children="Deep learning for bacterial spot prediction"
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
def appContainer(pathTestFolder,error):
    global data, pdDF,infectedDF,healthyDF,dataset
    data, pdDF,infectedDF, healthyDF = computeBackend(pathTestFolder)
    dataset = pd.read_pickle("Prescriptive_data_nn.pkl")

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
                        "margin-top" : "175px",
                        "margin-bottom" : "175px"
                    }
                ),
                generate_modal(),
                createLowerBanner(),
                dcc.ConfirmDialog(id ='dialogue',message="File Not Found, Using Default Directory", displayed=error),
                html.Div(id='fakeDiv'),
            ]
        )
    )


def layoutApp():
    pathTestFolder = str(pathlib.Path(__file__).parent.resolve()) + '/assets/images/'
    error = False
    return html.Div(id='layoutContainer', children = appContainer(pathTestFolder,error))

app.layout = layoutApp


# =============

# ======= Callback Modal =======

@app.callback(
    Output("modal", "style"),
    [Input("faqButton", "n_clicks"), Input("closeButton", "n_clicks")],
)
def update_click_output(_,__):
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
        return visualisationsTab(data,pdDF)
    elif switchTab == "infectedTab":
        return infectedTab()
    elif switchTab == "healthyTab":
        return healthyTab()
    elif switchTab == "fileSelectionTab":
        return uploadFileTab()
    elif switchTab == "prescriptiveTab":
        return distributionTab(dataset)
    else:
        return html.P("This Error Should Never Occur")


# =============

# ======= Search File Button =======

@app.callback(Output('layoutContainer', 'children'),
              [Input('uploadData', 'contents'), Input('dragData', 'contents')],
              [State('uploadData', 'filename'), State('dragData','filename')])
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

    return appContainer(pathTestFolder,error)


# =============

# ======= Confirm Dialogue =======

@app.callback(Output('dialogue', 'displayed'),
              [Input('interval-component','n_intervals')])
def openDialogue(_):
    #if fileNotFound:
    #    return True
    return False

@app.callback(Output('fakeDiv', 'children'),
              [Input('dialogue', 'submit_n_clicks')])
def closeDialogue(submit_n_clicks):
    if submit_n_clicks:
        return None

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