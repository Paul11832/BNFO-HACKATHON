from dash import html
from navbar import create_navbar

nav = create_navbar()

header = html.H3('Welcome to page 3!', style={'text-align': 'center', 'padding': '16px'})


def create_page_3():
    layout = html.Div([
        nav,
        header,
    ])
    return layout
