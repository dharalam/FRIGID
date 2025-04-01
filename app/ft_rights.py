from fasthtml.common import Div, H2, H3, Strong, P, Ul, Li, Ol, A

rights = Div(cls='content-container')(
    H2('Know Your Rights'),
    Div(cls='alert alert-warning')(
        Strong('Disclaimer:'),
        'The information provided here is for educational purposes only and does not constitute legal advice. Please consult with an immigration attorney for guidance specific to your situation.'
    ),
    P("Understanding your rights during encounters with Immigration and Customs Enforcement (ICE) officers is crucial. Everyone in the United States, regardless of immigration status, has certain constitutional rights. Here's what you should know:"),
    Div(cls='card mb-4')(
        Div('Your Rights at Home', cls='card-header'),
        Div(cls='card-body')(
            Ul(
                Li(
                    Strong("You don't have to open your door."),
                    'ICE officers cannot enter your home without a valid search warrant signed by a judge or your consent.'
                ),
                Li(
                    Strong('Ask to see a warrant.'),
                    'If officers claim to have a warrant, ask them to slide it under the door or hold it up to a window so you can inspect it before opening the door.'
                ),
                Li(
                    Strong('Check if the warrant is signed by a judge.'),
                    'Only a judicial warrant (signed by a judge) gives ICE the legal authority to enter your home without permission.'
                ),
                Li(
                    Strong('Remain silent.'),
                    'You have the right to remain silent and do not have to answer questions about your immigration status, birthplace, or how you entered the U.S.'
                )
            )
        )
    ),
    Div(cls='card mb-4')(
        Div('Your Rights in Public Places', cls='card-header'),
        Div(cls='card-body')(
            Ul(
                Li(
                    Strong('You have the right to remain silent.'),
                    'You can tell the officer you want to remain silent.'
                ),
                Li(
                    Strong('You can refuse a search.'),
                    "If you're stopped in public, officers cannot search you or your belongings without your consent or probable cause."
                ),
                Li(
                    Strong("You can ask if you're free to go."),
                    'If the officer says yes, calmly walk away.'
                ),
                Li(
                    Strong('You have the right to speak to a lawyer.'),
                    'If detained, say that you wish to speak to an attorney.'
                )
            )
        )
    ),
    Div(cls='card mb-4')(
        Div('Your Rights if Detained', cls='card-header'),
        Div(cls='card-body')(
            Ul(
                Li(
                    Strong('You have the right to speak to an attorney.'),
                    'You can ask for a list of free or low-cost legal services.'
                ),
                Li(
                    Strong('You have the right to contact your consulate.'),
                    'Foreign nationals detained in the U.S. have the right to call their consulate or have law enforcement inform the consulate of their arrest.'
                ),
                Li(
                    Strong('You have the right to refuse to sign anything.'),
                    "Don't sign any documents without speaking to an attorney, especially if you don't understand what they say."
                ),
                Li(
                    Strong('You have the right to a hearing.'),
                    'If you believe you have the right to stay in the U.S., you can request a hearing before an immigration judge.'
                )
            )
        )
    ),
    H3('What to Do During an ICE Encounter'),
    Ol(
        Li(
            Strong('Stay calm and do not run.'),
            'This can be used against you and may lead to arrest.'
        ),
        Li(
            Strong('Document the encounter.'),
            "If possible, note officers' names, badge numbers, and what occurred."
        ),
        Li(
            Strong('Report the incident.'),
            'Contact local immigrant rights organizations to report ICE activity.'
        )
    ),
    H3('Prepare in Advance'),
    P('Being prepared can help protect you and your loved ones:'),
    Ul(
        Li(
            Strong('Create a safety plan.'),
            'Decide who will take care of your children, pets, or property if you are detained.'
        ),
        Li(
            Strong('Memorize important phone numbers.'),
            'Know the numbers of family members, friends, and immigration attorneys.'
        ),
        Li(
            Strong('Keep important documents in a safe place.'),
            'Store copies of birth certificates, immigration documents, and other important papers where a trusted person can access them.'
        ),
        Li(
            Strong('Carry the phone number of an immigration attorney.'),
            'Have this information readily available if you need legal assistance.'
        )
    ),
    H3('Resources for Legal Assistance'),
    Div(cls='row')(
        Div(cls='col-md-6')(
            Div(cls='card')(
                Div('Legal Aid Organizations in New Jersey', cls='card-header'),
                Div(cls='card-body')(
                    Ul(
                        Li('American Friends Service Committee: (973) 643-1924'),
                        Li('Legal Services of New Jersey: (888) 576-5529'),
                        Li('Catholic Charities Immigration Legal Services: (973) 733-3516'),
                        Li('American Civil Liberties Union of NJ: (973) 642-2084')
                    )
                )
            )
        ),
        Div(cls='col-md-6')(
            Div(cls='card')(
                Div('Know Your Rights Materials', cls='card-header'),
                Div(cls='card-body')(
                    Ul(
                        Li(
                            A('Know Your Rights (ACLU)', href='https://www.aclu.org/know-your-rights/immigrants-rights')
                        ),
                        Li(
                            A('Know Your Rights (NIJC)', href='https://immigrantjustice.org/know-your-rights/ice-encounter')
                        )
                    )
                )
            )
        )
    )
)