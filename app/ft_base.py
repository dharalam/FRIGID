from fasthtml.common import Div, Strong, Script, Html, Head, FT, Title, Meta, Link, Body, Nav, A, Li, Ul, Header, H1, Button, I

def render_template(title:str, active_page:str, block:FT = None, addl:FT =  None):
    base = Html(
        Head(
            Title(f'{title} - FRIGID'),
            Meta(charset='utf-8'),
            Meta(name='viewport', content='width=device-width, initial-scale=1.0'),
            # Add theme-color meta for mobile browsers
            Meta(name='theme-color', content='#9d1535'),
            Link(rel='stylesheet', href='https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css'),
            # Add Font Awesome for theme icons
            Link(rel='stylesheet', href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'),
            Link(rel='stylesheet', href="./app/static/style.css"),
            # Add dark mode script in the head for immediate theme detection
            Script("""
                // Check for saved theme preference or respect OS preference
                const getTheme = () => {
                    const savedTheme = localStorage.getItem('theme');
                    if (savedTheme) {
                        return savedTheme;
                    }
                    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
                };
                
                // Apply theme immediately to prevent flash of wrong theme
                document.documentElement.setAttribute('data-theme', getTheme());
            """)
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
                        'eneral ',
                        Strong('I'),
                        'CE ',
                        Strong('D'),
                        'etainments'
                    )
                )
            ),
            block,
            # Add the theme toggle button
            Button(
                I(cls='fas fa-moon'),
                cls='theme-toggle',
                id='theme-toggle',
                type='button',
                title='Toggle Dark/Light Mode'
            ),
            Script(src='https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/js/bootstrap.bundle.min.js'),
            # Add theme toggle functionality script
            Script("""
                document.addEventListener('DOMContentLoaded', () => {
                    const toggleBtn = document.getElementById('theme-toggle');
                    const toggleIcon = toggleBtn.querySelector('i');
                    
                    // Update toggle button icon based on current theme
                    const updateToggleIcon = () => {
                        const currentTheme = document.documentElement.getAttribute('data-theme');
                        if (currentTheme === 'dark') {
                            toggleIcon.className = 'fas fa-sun';
                            toggleBtn.title = 'Switch to Light Mode';
                        } else {
                            toggleIcon.className = 'fas fa-moon';
                            toggleBtn.title = 'Switch to Dark Mode';
                        }
                    };
                    
                    // Initial icon update
                    updateToggleIcon();
                    
                    // Toggle theme
                    toggleBtn.addEventListener('click', () => {
                        const currentTheme = document.documentElement.getAttribute('data-theme');
                        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
                        
                        document.documentElement.setAttribute('data-theme', newTheme);
                        localStorage.setItem('theme', newTheme);
                        updateToggleIcon();
                    });
                });
            """),
            addl
        )
    )
    return base