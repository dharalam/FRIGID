from fasthtml.common import Div, H2, H3, Strong, P, H4, H5, Table, Thead, Tr, Th, Tbody, Td, Script

def render_data(total_reports, unique_places, top_places, reddit_data, reddit_cols, ero_data, ero_cols):
    data = Div(cls='data-container')(
        H2('Analysis'),
        Div(cls='data-stats')(
            H3('Summary'),
            Div(cls='row')(
                Div(cls='col-md-4')(
                    P(
                        Strong('Total Reports:'),
                        f'{ total_reports }'
                    )
                ),
                Div(cls='col-md-4')(
                    P(
                        Strong('Unique Places:'),
                        f'{ unique_places }'
                    )
                )
            ),
            H4('Most Reported Places'),
            Div(cls='row')(
                *(Div(cls='col-md-4 mb-2')(
                    Div(cls='card')(
                        Div(cls='card-body')(
                            H5(f'{ place }', cls='card-title'),
                            P(f'{ count } reports', cls='card-text')
                        )
                    )
                ) for place, count in top_places)
            )
        ),
        H3('Reddit Data'),
        Div(cls='table-container')(
            Table(cls='table')(
                Thead(
                    Tr(
                        *(Th(f'{ col }') for col in reddit_cols)
                    )
                ),
                Tbody(
                    *(Tr(
                        *(Td(f'{ row[col] }') for col in reddit_cols)
                    ) for row in reddit_data)
                )
            )
        ),
        H3('ERO Twitter Data'),
        Div(cls='table-container')(
            Table(cls='table')(
                Thead(
                    Tr(
                        *(Th(f'{ col }') for col in ero_cols),
                    )
                ),
                Tbody(
                    *(Tr(
                        *(Td(f'{ row[col] }') for col in ero_cols)
                    ) for row in ero_data),
                )
            )
        )
    )
    return data

data_script = Script("// Add any data-specific JavaScript here\r\n    document.addEventListener('DOMContentLoaded', function() {\r\n        console.log('Data page loaded');\r\n    });")