import dash
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

def distributionTab(dataset):
    return (
        html.Div(
            id = 'distributionPage',
            className = 'distributionPage',
            children = [
                countDiv(dataset),
                barChart(dataset),
                pieChart(dataset)
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
                                children = ['Number of Bacterial Spots']
                            ),
                            html.Div(
                                id='secondTextCountDivDist',
                                className='secondTextCountDivDist',
                                children='Count'
                            ),
                            daq.LEDDisplay(
                                id="countDisplayDist",
                                className='countDisplayDist',
                                value = dataset["Label"].sum(),
                                color = '#FFFFFF',
                                backgroundColor="#0069A9",
                                size=50,
                                label = 'Number',
                            ),
                            daq.LEDDisplay(
                                id="countDisplayPercentageDist",
                                className='countDisplayPercentageDist',
                                value= round(dataset["Label"].sum()/len(dataset),2),
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
                     'type': 'bar', 'name': "Healhy"},
                    {'x': [plantTypeList[0], plantTypeList[1], plantTypeList[2]],
                     'y': [df1["Label"].sum(), df2["Label"].sum(), df3["Label"].sum()],
                     'type': 'bar', 'name': 'Infected'},
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
                     'type': 'pie', 'name': 'probGraph'},
                ],
                'layout': {
                    'title': 'PieChart Pepperbell',
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
                        'title': 'PieChart Potato',
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
                        'title': 'PieChart Tomato',
                        "titlefont": {
                            "size": 30
                        },
                        'paper_bgcolor': '#E4FED7',
                        'font': {
                            'color': '#373936'
                        },
                        'legend' : go.layout.Legend(
                        x=1,
                        y=1,
                        )
                    }
                }
            ),



        ]
    )

