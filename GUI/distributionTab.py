
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
import plotly.graph_objects as go
import numpy as np

def distributionTab(dataset,lossList):
    return (
        html.Div(
            id = 'distributionPage',
            className = 'distributionPage',
            children = [
                countDiv(dataset),
                barChart(dataset),
                pieChart(dataset),
                html.Hr(),
                modelSummary(lossList)
            ]
        )
    )

def countDiv(dataset):
    return html.Div(
        id = 'countDivDist',
        className = 'countDivDist',
        children = [
            html.Div(
                id = 'countListDist',
                className = 'countListDist',
                children=[
                    html.Div(
                        id = 'innerCountDivDist',
                        className = 'innerCountDivDist',
                        children=[
                            html.Div(
                                id = 'firstTextCountDivDist',
                                className = 'firstTextCountDivDist',
                                children = ['Number of Leaves with Bacterial Spots']
                            ),
                            daq.LEDDisplay(
                                id="countDisplayDist",
                                className='countDisplayDist',
                                value = dataset["Label"].sum(),
                                color = '#FFFFFF',
                                backgroundColor="#0069A9",
                                size=50,
                                label = {
                                    "label": "Number",
                                    "style":{
                                        "font-size":"18px",
                                        "color": "#373936",
                                        "font-weight": "bold",
                                    }
                                },
                            ),
                            daq.LEDDisplay(
                                id="countDisplayPercentageDist",
                                className='countDisplayPercentageDist',
                                value= round(dataset["Label"].sum()/len(dataset),2),
                                color='#FFFFFF',
                                backgroundColor="#0069A9",
                                size=50,
                                label = {
                                    "label": "Probability",
                                    "style":{
                                        "font-size":"18px",
                                        "color": "#373936",
                                        "font-weight": "bold"
                                    }
                                }
                            )
                        ]
                    )
                ]
            )
        ]
    )

def barChart(dataset):
    plantTypeList = dataset["PlantType"].unique()
    df1 = dataset.loc[dataset["PlantType"] == plantTypeList[0]]
    df2 = dataset.loc[dataset["PlantType"] == plantTypeList[1]]
    df3 = dataset.loc[dataset["PlantType"] == plantTypeList[2]]
    return html.Div(
        id = 'barDivDist',
        className ='barDivDist',
        children=
        dcc.Graph(
            id='barChartDist',
            className='barChartDist',
            figure={
                'data': [
                    {'x': [plantTypeList[0], plantTypeList[1], plantTypeList[2]],
                     'y': [len(df1) - df1["Label"].sum(), len(df2) - df2["Label"].sum(), len(df3) - df3["Label"].sum()],
                     'type': 'bar', 'name': "Non-Bacterial"},
                    {'x': [plantTypeList[0], plantTypeList[1], plantTypeList[2]],
                     'y': [df1["Label"].sum(), df2["Label"].sum(), df3["Label"].sum()],
                     'type': 'bar', 'name': 'Bacterial'},
                ],
                'layout': {
                    'title': 'Distribution of the Leaves with Bacterial Spots',
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

def pieChart(dataset):
    plantTypeList = dataset["PlantType"].unique()
    df1 = dataset.loc[dataset["PlantType"] == plantTypeList[0]]
    df2 = dataset.loc[dataset["PlantType"] == plantTypeList[1]]
    df3 = dataset.loc[dataset["PlantType"] == plantTypeList[2]]

    sum1 = df1.groupby(df1["ClassName"])["Label"].count()
    sum2 = df2.groupby(df2["ClassName"])["Label"].count()
    sum3 = df3.groupby(df3["ClassName"])["Label"].count()

    return html.Div(
        id='pieDivDist',
        className='pieDivDist',
        children=[
        dcc.Graph(
            id='pieChartPepperbell',
            className='pieChartPepperbell',
            figure={
                'data': [
                    {'labels': sorted(df1["ClassName"].unique()),
                     'values': sum1,
                     'type': 'pie', 'name': 'pieChartDist'},
                ],
                'layout': {
                    'title': 'Distribution Pepperbell Plant',
                    "titlefont": {
                        "size": 30
                    },
                    'paper_bgcolor': '#E4FED7',
                    'font': {
                        'color': '#373936'
                    }
                }
            }
        ),
            dcc.Graph(
                id='pieChartPotato',
                className='pieChartPotato',
                figure={
                    'data': [
                        {'labels': sorted(df2["ClassName"].unique()),
                         'values': sum2,
                         'type': 'pie', 'name': 'probGraph'},
                    ],
                    'layout': {
                        'title': 'Distribution Potato Plant',
                        "titlefont": {
                            "size": 30
                        },
                        'paper_bgcolor': '#E4FED7',
                        'font': {
                            'color': '#373936'
                        }
                    }
                }
            ),
            dcc.Graph(
                id='pieChartTomato',
                className='pieChartTomato',
                figure={
                    'data': [
                        {'labels': sorted(df3["ClassName"].unique()),
                         'values': sum3,
                         'type': 'pie', 'name': 'probGraph'},
                    ],
                    'layout': {
                        'title': 'Distribution Tomato Plant',
                        "titlefont": {
                            "size": 30
                        },
                        'paper_bgcolor': '#E4FED7',
                        'font': {
                            'color': '#373936'
                        },

                    }
                }
            ),
        ]
    )

def modelSummary(lossList):

    return html.Div(

        id='modelSummaryDiv',
        className='modelSummaryDiv',
        children =[
            html.Div(id="modelSummaryTitle",className="modelSummaryTitle",children="Model Summary"),
            html.Div(
                id = 'modelNumbersDiv',
                className = 'modelNumbersDiv',
                children = [
                    html.Div(
                        id='modelNumbersText',
                        className='modelNumbersText',
                        children=['Model Statistics']
                    ),
                    daq.LEDDisplay(
                        id="countDisplayModelAccuracy",
                        className='countDisplayModelAccuracy',
                        value=0.96,
                        color='#FFFFFF',
                        backgroundColor="#0069A9",
                        size=50,
                        label={
                            "label": "Accuracy",
                            "style":{
                                "font-size":"18px",
                                "color": "#373936",
                                "font-weight": "bold",
                                "margin-bottom": "-20px"
                            }
                        }
                    ),

                    daq.LEDDisplay(
                        id="countDisplayModelPrecision",
                        className='countDisplayModelPrecision',
                        value=0.92,
                        color='#FFFFFF',
                        backgroundColor="#0069A9",
                        size=50,
                        label={
                            "label": "Precision",
                            "style":{
                                "font-size":"18px",
                                "color": "#373936",
                                "font-weight": "bold",
                                "margin-bottom": "-20px"
                            }
                        }
                    ),
                    daq.LEDDisplay(
                        id="countDisplayModelRecall",
                        className='countDisplayModelRecall',
                        value=0.81,
                        color='#FFFFFF',
                        backgroundColor="#0069A9",
                        size=50,
                        label={
                            "label": "Recall",
                            "style": {
                                "font-size": "18px",
                                "color": "#373936",
                                "font-weight": "bold",
                                "margin-bottom": "-20px"
                            }
                        }
                    ),
                ]
            ),
            html.Div(
                id = 'modelPlotsDiv',
                className = 'modelPlotsDiv',
                children=[
                    dcc.Graph(
                        id = 'accuracyPlot',
                        className= 'accuracyPlot',
                        figure = {
                            'data': [
                                {'x': list(range(len(lossList[1]))),
                                 'y': lossList[1],
                                 'name': 'Loss'},
                                {'x': list(range(len(lossList[1]))),
                                 'y': lossList[3],
                                 'name': 'Loss Validation'
                                 }
                            ],
                            'layout': {
                                'title': 'Model Accuracy Graph',
                                "titlefont": {
                                    "size": 30
                                },
                                'paper_bgcolor': '#E4FED7',
                                'font': {
                                    'color': '#373936'
                                },
                                'xaxis': {
                                    'title': 'Number of Iterations'
                                },
                                'yaxis': {
                                    'title': 'Accuracy',
                                    'type' : 'linear',
                                    'autorange': False,
                                    'range': [0.05,1.1],
                                    'fixedrange': True
                                }
                            }
                        }

                    ),
                    dcc.Graph(
                        id='precisionPlot',
                        className='precisionPlot',
                        figure={
                            'data': [
                                {'x': list(range(len(lossList[0]))),
                                 'y': lossList[0],
                                 'name': 'Loss'},
                                {'x': list(range(len(lossList[0]))),
                                 'y': lossList[2],
                                 'name': 'Loss Validation'
                                }

                            ],
                            'layout': {
                                'title': 'Model Precision Graph',
                                "titlefont": {
                                    "size": 30
                                },
                                'paper_bgcolor': '#E4FED7',
                                'font': {
                                    'color': '#373936'
                                },
                                'xaxis': {
                                    'title': 'Number of Iterations'
                                },
                                'yaxis': {
                                    'title' : 'Precision',
                                    'type': 'linear',
                                    'autorange': False,
                                    'range': [-0.1, 3 ],
                                    'fixedrange': True
                                }
                            }
                        }

                    )
                ]


            )
        ]
    )

