from dash import Dash, dcc, html, page_container
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title="Robust Estimators Lab",
)
server = app.server


def nav_link(label: str, href: str):
    return dcc.Link(label, href=href, className="top-nav-link")


app.layout = html.Div(
    [
        html.Header(
            [
                html.Div(
                    [
                        html.H1("Robust Estimators Lab", className="app-title"),
                        html.Div(
                            "Interactive teaching and evidence interface for robust estimator mixtures",
                            className="app-subtitle",
                        ),
                    ]
                ),
                html.Nav(
                    [
                        nav_link("01 — Build the problem", "/"),
                        nav_link("02 — GA search", "/ga-search"),
                        nav_link("03 — Thesis results", "/thesis-results"),
                        nav_link("04 — Validation pipeline", "/validation"),
                    ],
                    className="top-nav",
                ),
            ],
            className="app-header",
        ),
        html.Main(page_container, className="page-container"),
    ],
    className="app-shell",
)

if __name__ == "__main__":
    app.run(debug=True)
