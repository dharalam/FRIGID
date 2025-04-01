from fasthtml.common import Div, Strong, Script, Html, Head, FT, Title, Meta, Link, Body, Nav, A, Li, Ul, Header, H1

def render_template(title:str, active_page:str, block:FT = None, addl:FT =  None):
    base = Html(
        Head(
            Title(f'{title} - FRIGID'),
            Meta(charset='utf-8'),
            Meta(name='viewport', content='width=device-width, initial-scale=1.0'),
            Link(rel='stylesheet', href='https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css'),
            Link(rel='stylesheet', href="./app/static/style.css"),
        ),
        Body(
            Nav(cls='navbar')(
                Div(cls='container')(
                    A('FRIGID', href='/', cls='navbar-brand'),
                    Ul(cls='navbar-nav')(
                        Li(cls='nav-item')(
                            A('Map', href='/', cls=f"nav-link {'active' if active_page == 'map' else ''}")
                        ),
                        Li(cls='nav-item')(
                            A('About', href='/about', cls=f"nav-link {'active' if active_page == 'about' else ''}")
                        ),
                        Li(cls='nav-item')(
                            A('Data', href='/data', cls=f"nav-link {'active' if active_page == 'data' else ''}")
                        ),
                        Li(cls='nav-item')(
                            A('Know Your Rights', href='/rights', cls=f"nav-link {'active' if active_page == 'rights' else ''}")
                        ),
                        Li(cls='nav-item')(
                            A('Submit a Report', href='/report', cls=f"nav-link {'active' if active_page == 'report' else ''}")
                        )
                    )
                )
            ),
            Header(cls='header')(
                Div(cls='container')(
                    H1(
                        Strong('F'),
                        'etching ',
                        Strong('R'),
                        'eliable ',
                        Strong('I'),
                        'nstances of ',
                        Strong('G'),
                        'enuine ',
                        Strong('I'),
                        'CE ',
                        Strong('D'),
                        'etainments'
                    )
                )
            ),
            block,
            Script(src='https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/js/bootstrap.bundle.min.js'),
            addl
        )
    )
    return base