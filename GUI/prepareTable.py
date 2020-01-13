import dash_html_components as html


def get_thumbnail(app,path):
   return html.Img(src=app.get_asset_url('images/'+path),style={'height':'230px', 'width':'230px'})

def prepareTable(df,app):
    df['leaf'] = df['leaf'].apply(lambda a: get_thumbnail(app,a))

    infectedTable = df[df['isInfectedFlag']==1].reset_index()
    healthyTable = df[df['isInfectedFlag']==0].reset_index()

    return makeTable(infectedTable,True), makeTable(healthyTable,False)

def makeTable(inputDF, infected):
    table_header = [
        html.Thead(html.Tr([html.Th("ID"), html.Th("Leaf"), html.Th("Probability of being Infected/Healthy")]))
    ]
    rows = []

    if not infected:
        inputDF['isInfectedPercentage'] = 1-inputDF['isInfectedPercentage']

    for x in range(0, int(inputDF.shape[0])):
        row = html.Tr([html.Td(inputDF.loc[x, 'id']),
                       html.Td(inputDF.loc[x, 'leaf']),
                       html.Td(inputDF.loc[x,'isInfectedPercentage'])])
        rows.append(row)

    table_body = [html.Tbody(rows)]

    return table_header + table_body
