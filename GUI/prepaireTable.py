import dash_html_components as html


def get_thumbnail(app,path):
   return html.Img(src=app.get_asset_url('images/'+path),style={'height':'230px', 'width':'230px'})

def prepaireTable(data,app):
    print(data.loc[0, 'leaf'])
    data['leaf'] = data['leaf'].apply(lambda a: get_thumbnail(app,a))


    table_header = [
        html.Thead(html.Tr([html.Th("ID"), html.Th("Leaf")]))
    ]

    rows = []

    for x in range(0,data.shape[0]):
        row = html.Tr([html.Td(data.loc[x,'id']),
                    html.Td(data.loc[x,'leaf'])])
        rows.append(row)

    table_body = [html.Tbody(rows)]

    return table_header+table_body

