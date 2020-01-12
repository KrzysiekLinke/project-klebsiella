import dash_html_components as html


def get_thumbnail(app,path):
   return html.Img(src=app.get_asset_url('images/'+path),style={'height':'230px', 'width':'230px'})

def prepaireTable(df,app):
    df['leaf'] = df['leaf'].apply(lambda a: get_thumbnail(app,a))

    infectedTable = df[df['isInfectedFlag']==1].reset_index()
    healthyTable = df[df['isInfectedFlag']==0].reset_index()

    return makeTable(infectedTable), makeTable(healthyTable)

def makeTable(inputDF):
    table_header = [
        html.Thead(html.Tr([html.Th("ID"), html.Th("Leaf")]))
    ]
    rows = []

    for x in range(0, inputDF.shape[0]):
        row = html.Tr([html.Td(inputDF.loc[x, 'id']),
                       html.Td(inputDF.loc[x, 'leaf'])])
        rows.append(row)

    table_body = [html.Tbody(rows)]

    return table_header + table_body


