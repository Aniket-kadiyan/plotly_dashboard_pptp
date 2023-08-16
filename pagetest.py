from dash import Dash, html, dcc
import dash
import dash_bootstrap_components as dbc
from waitress import serve


app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.DARKLY], title="Dashboard", meta_tags=[
           {'name': 'viewport', 'content': 'width=device-width , initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5'}])
application = app.server
print("\n\n")
serve(application)
navbar = dbc.NavbarSimple(
    dbc.Nav(
        [
            dbc.NavLink(page["name"].upper(), href=page["relative_path"])
            for page in dash.page_registry.values()
            if page["name"].lower()!="not found 404"
        ],
        pills=True,
        fill=True,
        
        # justified=True,
    ),
    brand="Dashboard",
    color="black",
    dark=True,
    style={'borderTop': '5px solid #d6d6d6',
           'borderBottom': '5px solid #d6d6d6',
           "borderLeft": "5px solid #d6d6d6",
           "borderRight": "5px solid #d6d6d6",
           "borderColor": "white", },
    # links_left=True,

)


app.layout = dbc.Container(
    [navbar, dash.page_container],
    fluid=True, style={
        "background-color": "black"
    },
)


if __name__ == "__main__":
    app.run_server(debug=True)
# app.layout = html.Div([

#     html.Div(
#         [
#             # html.Div(
#             #     dcc.Link(
#             #         f"{page['name']} - {page['path']}", href=page["relative_path"]
#             #     )
#             # )
#             # for page in dash.page_registry.values()
#             dcc.Tabs(id = "link_tabs" ,value=val0, children=tabs),
#         ]
#     ),

# 	dash.page_container(id="pagecontainer")
# ])
# # @app.callback(
# #     Output(),
# #     Input(),
# # )
# # def updatepage(link):
# #     print(link)
# if __name__ == '__main__':
# 	app.run(debug=True, port=8050)
