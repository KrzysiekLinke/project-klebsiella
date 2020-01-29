import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq

# ======= Input Test Files Tab =======

def visualisationsTab(data,pdDF):
    return (
        html.Div(
            id='mainPage',
            className='mainPage',
            children=[
                countDiv(data),
                probChart(pdDF),
                barChart(data),
                pieChart(data)
            ])
    )


# =============

# ======= LED-Display Div =======

def countDiv(data):
    return html.Div(
        id='countDiv',
        className='countDiv',
        children=[
            html.Div(
                id='countList',
                className='countList',
                children=[
                    html.Div(
                        id='innerCountDiv',
                        className='innerCountDiv',
                        children=[
                            html.Div(
                                id='firstTextCountDiv',
                                className='firstTextCountDiv',
                                children=['Number of Leaves with Bacterial Spots']
                            ),
                            daq.LEDDisplay(
                                id="countDisplay",
                                className='countDisplay',
                                value=data[['isInfectedFlag']].sum(),
                                color='#FFFFFF',
                                backgroundColor="#0069A9",
                                size=50,
                                label={
                                    "label": "Number",
                                    "style":{
                                        "font-size":"16px",
                                        "color": "#373936",
                                        "font-weight": "bold"
                                    }
                                },
                            ),
                            daq.LEDDisplay(
                                id="countDisplayPercentage",
                                className='countDisplayPercentage',
                                value=round(data[['isInfectedFlag']].sum() / len(data), 2),
                                color='#FFFFFF',
                                backgroundColor="#0069A9",
                                size=50,
                                label={
                                    "label": "Probability",
                                    "style":{
                                        "font-size":"16px",
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


# =============

# ======= Probability Graph Div =======

def probChart(pdDF):
    return html.Div(
        id='probDiv',
        className='probDiv',
        children=
        dcc.Graph(
            id='probGraph',
            className='probGraph',
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

def barChart(data):
    return html.Div(
        id='barDiv',
        className='barDiv',
        children=
        dcc.Graph(
            id='barChart',
            className='barChart',
            figure={
                'data': [
                    {'x': ['Non-Bacterial Spots'],
                     'y': [int(len(data) - data[['isInfectedFlag']].sum())],
                     'type': 'bar', 'name': 'Non-Bacterial'},
                    {'x': ['Bacterial Spots'],
                     'y': [int(data[['isInfectedFlag']].sum())],
                     'type': 'bar', 'name': 'Bacterial'
                     }

                ],
                'layout': {
                    'title': 'The Number Of Leaves with Bacterial Spots',
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
                    'color': ['blue', 'orange'],
                    'font': {
                        'color': '#373936'
                    },
                }

            }
        )
    )


# =============

# ======= PieChart Div =======

def pieChart(data):
    return html.Div(
        id='pieDiv',
        className='pieDiv',
        children=
        dcc.Graph(
            id='pieChart',
            className='pieChart',
            figure={
                'data': [
                    {'labels': ['Non-Bacterial', 'Bacterial'],
                     'values': [int(len(data) - data[['isInfectedFlag']].sum()), int(data[['isInfectedFlag']].sum())],
                     'type': 'pie', 'name': 'probGraph'},

                ],
                'layout': {
                    'title': 'Distribution of Bacterial Spots on Leaves',
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