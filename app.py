import dash
from dash import html, dcc, Input, Output, State, html
import dash_bootstrap_components as dbc
from dash import page_registry, page_container

from dash_extensions.enrich import (
    DashProxy,
    MultiplexerTransform,
    html,
    dcc,
)

external_stylesheets = [dbc.themes.JOURNAL]

app = DashProxy(
    __name__,
    transforms=[MultiplexerTransform()],
    use_pages=True,
    prevent_initial_callbacks=True,
    suppress_callback_exceptions=True,
    external_stylesheets=external_stylesheets,
)

server = app.server

GENLAC_LOGO = "/assets/genlac.png"

dropdown = dbc.Row([
    dbc.Col(
        dbc.DropdownMenu(
        children=[
            dbc.DropdownMenuItem("Employment and skills", header=True),
            dbc.DropdownMenuItem("Labor force participation rate", href="/"),
            dbc.DropdownMenuItem("Employment rate", href="/tasa-de-empleo"),
            dbc.DropdownMenuItem("Unemployment rate", href="/tasa-de-desempleo"),
            dbc.DropdownMenuItem("Labor informality rate", href="/tasa-de-informalidad-laboral"),
            dbc.DropdownMenuItem("Weekly hours worked", href="/horas-de-trabajo"),
            dbc.DropdownMenuItem("Employers", href="/empleador"),
            dbc.DropdownMenuItem("Wage earners", href="/asalariados"),
            dbc.DropdownMenuItem("Self-employed", href="/cuentapropista"),
            dbc.DropdownMenuItem("Unpaid workers", href="/no-remunerado"),
            dbc.DropdownMenuItem(divider=True),
            dbc.DropdownMenuItem("Income", header=True),
            dbc.DropdownMenuItem("Average hourly wage", href="/salario-horario"),
            dbc.DropdownMenuItem("Monthly labor income", href="/ingreso-laboral"),
            dbc.DropdownMenuItem("Gender wage gap (conditional)", href="/brecha-salarial-genero"),
            dbc.DropdownMenuItem(divider=True),
            dbc.DropdownMenuItem("Skills of the adult population", header=True),
            dbc.DropdownMenuItem("Years of education", href="/anios-educacion"),
            dbc.DropdownMenuItem("Percentage of high-skilled adults", href="/adultos-con-alta-calificacion"),
        ],
        size="lg",
        nav=True,
        in_navbar=True,
        label="Indicators",
        className="ms-0",
        toggle_style={"color": "#460074"},
        align_end=False,
        style={'width':'100%'}

        )
    )
],
className="g-0 ms-auto flex-nowrap mt-5 mt-md-0",
align="center",
)


navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                        dbc.Collapse(
                            dropdown, 
                            className="ml-auto",
                            id="navbar-collapse",
                            is_open=False,
                            navbar=True,
                        ),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="/",
                style={"textDecoration": "none"},
            ),
        ],
    fluid=True),
    #outline=True, 
    color="light",
    dark=True,
)
# Definimos el layout:
app.layout = html.Div(
    [
        dcc.Store(id="store", data='Argentina'),
        dbc.Container([
    dbc.Row(
        [
            navbar # Navbar
        ]
    ),
    html.Br(),        
    dbc.Row(
        [
            dash.page_container # Contenido de cada pagina
        ]
    )
], fluid=True)
    ]
)


if __name__ == "__main__":
    app.run_server()