from fasthtml.common import Div, H2, P, Strong, H3, Ul, Li

about = Div(cls='content-container')(
    H2('About FRIGID'),
    P('FRIGID (Fetching Reliable Instances of General ICE Detainments) is a community-driven platform designed to track and visualize ICE (Immigration and Customs Enforcement) activity across New Jersey. Our mission is to provide transparent, accessible information about ICE operations to help keep communities informed.'),
    Div(cls='alert alert-info')(
        Strong('Note:'),
        'This platform relies on community-reported data and should be used as an informational resource rather than definitive legal guidance.'
    ),
    H3('Our Mission'),
    P('We believe that accessible information is a cornerstone of community safety. FRIGID aims to:'),
    Ul(
        Li('Collect and visualize reports of ICE activity in New Jersey'),
        Li('Provide educational resources about immigration rights'),
        Li('Create transparency around enforcement patterns'),
        Li('Empower communities with knowledge to make informed decisions')
    ),
    H3('How It Works'),
    P('We at FRIGID collect data from various sources including social media reports, news organizations, and first-hand accounts. This data is verified to the best of our ability, aggregated, and displayed on an interactive map to show patterns of ICE activity.'),
    Div(cls='row')(
        Div(cls='col-md-4')(
            Div(cls='card')(
                Div('Data Collection', cls='card-header'),
                Div(cls='card-body')(
                    P('We gather information from social media platforms and local news, filtering for reports of ICE activity in New Jersey.')
                )
            )
        ),
        Div(cls='col-md-4')(
            Div(cls='card')(
                Div('Verification', cls='card-header'),
                Div(cls='card-body')(
                    P('Reports are cross-referenced when possible with multiple sources to ensure accuracy.')
                )
            )
        ),
        Div(cls='col-md-4')(
            Div(cls='card')(
                Div('Visualization', cls='card-header'),
                Div(cls='card-body')(
                    P('Data is plotted on interactive maps showing trends and hotspots of activity.')
                )
            )
        )
    ),
    H3('Data Privacy'),
    P('We take privacy seriously. All private personal information is removed from reports before they are added to our database. We focus on location data and the frequency of enforcement actions.'),
    H3('Legal Disclaimers'),
    Div(cls='alert alert-warning')(
        Strong('Important Legal Information:'),
        Ul(
            Li('FRIGID provides informational resources only, not legal advice'),
            Li('We make no warranties about the accuracy or completeness of our data'),
            Li('Use of this information is at your own risk'),
            Li('We are not liable for any actions taken based on this information'),
            Li('For legal advice, consult a qualified immigration attorney')
        )
    ),
    P('FRIGID complies with all applicable U.S. federal laws and New Jersey state laws. This platform is protected under Section 230 of the Communications Decency Act for third-party content.')
)