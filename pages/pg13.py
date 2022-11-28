import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html, register_page, ctx, no_update
from dash_extensions.enrich import Output, Input, State, callback

dash.register_page(__name__,
                   path='/brecha-salarial-genero',  # represents the url text
                   name='Brecha salarial condicionada',  # name of page, commonly used as name of link
                   title='Brecha salarial condicionada'  # epresents the title of browser's tab
)


# page 1 data
df = pd.read_csv("datasets/brecha_salarial_genero.csv")
df['indicador'] = df['indicador'].astype(str)
df['pais'] = df['pais'].astype(str)
df['comparacion_por'] = df['comparacion_por'].astype(str)
df['ano'] = df['ano'].astype(int)

mark_values = {2000:'2000',2001:'2001',2002:'2002',
                2003:'2003',2004:'2004',2005:'2005',
                2006:'2006',2007:'2007',2008:'2008',
                2009:'2009',2010:'2010',2011:'2011',
                2012:'2012',2015:'2015',2016:'2016',
                2013:'2013',2014:'2014',2015:'2015',
                2016:'2016',2017:'2017',2018:'2018',
                2019:'2019',2020:'2020',2021:'2021'}

# Para ordenar dropdown:
list_comparacion_por = list(df['comparacion_por'].unique())
list_comparacion_por_orden = list(df['comparacion_por_orden'].unique())
list_comparacion_por_ordenada = [x for _,x in sorted(zip(list_comparacion_por_orden,list_comparacion_por))]

layout = html.Div([
        dbc.Row([
        dbc.Col([
            dcc.Dropdown(options=[{'label': x, 'value': x} for x in df.pais.unique()], multi=True, id='page13-pais_elect')
        ], width=6),
        dbc.Col([
            dcc.Dropdown(options=[{'label': x, 'value': x} for x in list_comparacion_por_ordenada], multi=False, persistence=True, persistence_type='memory', value='Total', id='page13-comparacion_por_elect')
        ], width=6),
    ]),
        dbc.Row([
        dbc.Col([
            dcc.Graph(id='page13-line', config={'displayModeBar':False})
        ], width=12),
    ]),
        dbc.Row([
        dbc.Col([
        dcc.RangeSlider(id='page13-the_year',
                min=2000,
                max=2021,
                value=[2000,2021],
                marks=mark_values,
                step=1)
        ], width=12),
    ]),
])


@callback(
    Output('page13-pais_elect', "value"),
    Output("store", "data"),
    Input('page13-pais_elect', "value"),
    State("store", "data"),
)
def sync_dropdowns(dd_pais, store_pais):
    if dd_pais is None:
        return store_pais, no_update
    return dd_pais, dd_pais

@callback(
    Output('page13-line', 'figure'),
    Input('page13-pais_elect', 'value'),
    Input('page13-comparacion_por_elect', 'value'),
    [Input('page13-the_year','value')]
)


def update_graphs(pais_v, comparacion_por_v, years_chosen):
    dff = df.copy()
    print(years_chosen)
    dff=dff[(dff['ano']>=years_chosen[0])&(dff['ano']<=years_chosen[1])]
    if type(pais_v) == str:
        pais_v = [pais_v]
    dff = dff[dff['pais'].isin(pais_v)]
    dff = dff.query(f"comparacion_por == '{comparacion_por_v}'")
    indicador = dff['indicador'].iat[0]
    detalle_indicador_v = dff['detalle_indicador'].iat[0]
    disclaimer = dff['disclaimer'].iat[0]
    fig_line = px.line(dff, x='ano', y='valor', color='pais2', error_y='valor_errorestandar',
    line_dash= 'desagregacion', symbol= 'desagregacion',
    labels=dict(ano="Año", valor="", pais2="País", indicador="Indicador", desagregacion="Desagregación")).update_xaxes(type='category').update_layout(margin=dict(l=10, r=10, t=10, b=10))
    fig_line.update_traces(line=dict(width=2), 
        marker={'size': 10})
    fig_line.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=True,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            gridcolor = 'rgb(230, 230, 230)',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showline=True,
            showgrid=True,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            gridcolor = 'rgb(230, 230, 230)',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        autosize=True,
        margin=dict(
            autoexpand=True,
            l=25,
            r=25,
            t=65,
            b=120,
        ),
        legend=dict(orientation = "h", yanchor="bottom",y=-0.35,xanchor="left", x=0, font=dict(size= 12)),
        showlegend=True,
        plot_bgcolor='white',
        legend_title='',
    )

    annotations = []

    # Title
    annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.10,
                                  xanchor='left', yanchor='bottom',
                                  text=indicador,
                                  font=dict(family='Arial',
                                            size=22,
                                            color='rgb(37,37,37)'),
                                  showarrow=False))
    annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.03,
                                  xanchor='left', yanchor='bottom',
                                  text=detalle_indicador_v,
                                  font=dict(family='Arial',
                                            size=15,
                                            color='rgb(37,37,37)'),
                                  showarrow=False))
    #Source
    annotations.append(dict(xref='paper', yref='paper', x=0.001, y=-0.40,
                                  xanchor='left', yanchor='bottom',
                                  text=disclaimer,
                                  font=dict(family='Arial',
                                            size=10,
                                            color='rgb(82, 82, 82)'),
                                  showarrow=False))

    fig_line.update_layout(annotations=annotations)
    return fig_line