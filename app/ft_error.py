from fasthtml.common import Div, H4, P, A

error = lambda e: Div(cls='error-container')(
    Div(cls='alert alert-danger')(
        H4('Error', cls='alert-heading'),
        P(f'{e}')
    ),
    A('Back to Home', href='/', cls='btn btn-primary btn-back')
)