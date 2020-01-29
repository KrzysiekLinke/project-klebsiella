import dash_html_components as html
import os
import base64


def get_thumbnail(directory, path):
    encoded_image = base64.b64encode(open(directory+path, 'rb').read())
    return html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),style={'height':'80px', 'width':'80px'})

def prepareTable(df,directory):

    df['leaf'] = df['leaf'].apply(lambda a: get_thumbnail(directory,a))

    infectedTable = df[df['isInfectedFlag']==1].reset_index()
    healthyTable = df[df['isInfectedFlag']==0].reset_index()

    return makeTable(infectedTable,True), makeTable(healthyTable,False)

def makeTable(inputDF, infected):

    if infected:
        table_header = [
            html.Thead(html.Tr([html.Th("ID"), html.Th("Leaf"), html.Th("Probability of having Bacterial Spots")]))
        ]

    else:
        table_header = [
            html.Thead(html.Tr([html.Th("ID"), html.Th("Leaf"), html.Th("Probability of NOT having Bacterial Spots")]))
        ]

    rows1, rows2,rows3 = [],[],[]

    if not infected:
        inputDF['isInfectedPercentage'] = 1-inputDF['isInfectedPercentage']

    for x in range(0, inputDF.shape[0], 3):

        row = html.Tr([html.Td(inputDF.loc[x, 'id']),
                       html.Td(inputDF.loc[x, 'leaf']),
                       html.Td(inputDF.loc[x,'isInfectedPercentage'])])
        rows1.append(row)

    for x in range(1, inputDF.shape[0], 3):

        row = html.Tr([html.Td(inputDF.loc[x, 'id']),
                       html.Td(inputDF.loc[x, 'leaf']),
                       html.Td(inputDF.loc[x,'isInfectedPercentage'])])
        rows2.append(row)

    for x in range(2, inputDF.shape[0], 3):
        row = html.Tr([html.Td(inputDF.loc[x, 'id']),
                       html.Td(inputDF.loc[x, 'leaf']),
                       html.Td(inputDF.loc[x,'isInfectedPercentage'])])
        rows3.append(row)


    table1 = table_header + [html.Tbody(rows1)]
    table2 = table_header + [html.Tbody(rows2)]
    table3 = table_header + [html.Tbody(rows3)]

    return [table1,table2,table3]
