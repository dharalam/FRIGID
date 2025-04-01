from fasthtml.common import Div, H1, Form, P, Label, Input, Textarea, Strong, Ul, Li, Hr, H5, Button, H3 

def create_report(messages:list[tuple[str]]=[]):
    report = Div(cls='container mt-4')(
        H1('Submit ICE Activity Report', cls='text-center mb-4'),
        *(Div(f'{ message }', cls=f"alert alert-{ category if category != 'error' else 'danger' } flash-message") for category, message in messages),
        Div(cls='form-container')(
            P('Use this form to report ICE (Immigration and Customs Enforcement) activity in your area. This information helps our community stay informed and safe.', cls='lead'),
            Form(method='POST', action='/report')(
                Div(cls='mb-3')(
                    Label('Location', fr='location', cls='form-label required-field'),
                    Input(type='text', id='location', name='location', required='', placeholder='City, town, or specific address where activity was observed', cls='form-control'),
                    Div('Be as specific as possible with the location.', cls='form-text')
                ),
                Div(cls='row')(
                    Div(cls='col-md-6 mb-3')(
                        Label('Date', fr='date', cls='form-label required-field'),
                        Input(type='date', id='date', name='date', required='', cls='form-control')
                    ),
                    Div(cls='col-md-6 mb-3')(
                        Label('Approximate Time', fr='time', cls='form-label required-field'),
                        Input(type='time', id='time', name='time', required='', cls='form-control')
                    )
                ),
                Div(cls='mb-3')(
                    Label('Description', fr='description', cls='form-label required-field'),
                    Textarea(id='description', name='description', rows='4', required='', placeholder='Describe what you observed. Include details about vehicles, number of agents, activities observed, etc.', cls='form-control')
                ),
                Div(cls='alert alert-warning small')(
                    Strong('Warning:'),
                    'Please avoid including:',
                    Ul(
                        Li('Names or identifying details of individuals'),
                        Li('Speculative information (stick to observed facts)')
                    )
                ),
                H5('Contact Information (Optional)'),
                P('Your contact information will be kept confidential and only used if we need to verify details about your report.', cls='text-m'),
                Div(cls='mb-3')(
                    Label('Your Name', fr='contact_name', cls='form-label'),
                    Input(type='text', id='contact_name', name='contact_name', cls='form-control')
                ),
                Div(cls='row')(
                    Div(cls='col-md-6 mb-3')(
                        Label('Email', fr='contact_email', cls='form-label'),
                        Input(type='email', id='contact_email', name='contact_email', cls='form-control')
                    ),
                    Div(cls='col-md-6 mb-3')(
                        Label('Phone', fr='contact_phone', cls='form-label'),
                        Input(type='tel', id='contact_phone', name='contact_phone', cls='form-control')
                    )
                ),
                Div(cls='mb-3')(
                    Label('Additional Information', fr='additional_info', cls='form-label'),
                    Textarea(id='additional_info', name='additional_info', rows='3', placeholder='Any other details that might be helpful', cls='form-control')
                ),
                Div(cls='mb-3 form-check')(
                    Input(type='checkbox', id='terms_consent', name='terms_consent', required='', cls='form-check-input'),
                    Label(fr='terms_consent', cls='form-check-label')(
                        'I agree to the Terms of Service and understand that:',
                        Ul(cls='small')(
                            Li('This is not an emergency service'),
                            Li('Reports are public-facing unless marked sensitive'),
                            Li('False reports may be removed')
                        )
                    )
                ),
                Div(cls='legal-disclaimer small text-m')(
                    P('By submitting, you acknowledge that FRIGID:', cls="text-m"),
                    Ul(
                        Li('Cannot verify all reports in real-time'),
                        Li('Is not affiliated with any government agency'),
                        Li('May use anonymized data for statistical purposes'),
                        Li('Reserves the right to withhold publication of reports')
                    )
                ),
                Div(cls='d-grid gap-2')(
                    Button('Submit Report', type='submit', id='form-submit', cls='btn btn-primary')
                )
            ),
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
            P('FRIGID complies with all applicable U.S. federal laws and New Jersey state laws. This platform is protected under Section 230 of the Communications Decency Act for third-party content.'),
            Div(cls='privacy-notice')(
                H5('Privacy Notice'),
                P('Your privacy is important to us. Reports are sent to a secure Proton Mail account to ensure encryption and security. We do not store personal information on our servers unless you explicitly provide it. All contact information is optional and will only be used to follow up on reports if necessary.'),
                P('If you prefer to remain completely anonymous, you can submit the form without providing any contact information.')
            )
        )
    )
    return report