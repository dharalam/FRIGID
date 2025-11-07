from fasthtml.common import Div, Span, H3, P, Script, Style

loading_block = Div(cls="container")(
        Div(cls="loading-overlay", id="map-loading")(
            Div(cls="loading-content")(
                Div(cls="spinner-border text-primary", role="status")(
                    Span(cls="visually-hidden")("Loading maps...")
                ),
                H3(cls="mt-3")("Loading ICE Detainment Map..."),
                P("Please wait while we fetch the latest information.")
            )
        ),
        # Map container that will be populated later
        Div(id="map-container", cls="map-content d-none")()
    )

loading_script = Script("""
    (function() {
            console.log('Starting map loading process...');
            const mapContainer = document.getElementById('map-container');
            const loadingOverlay = document.getElementById('map-loading');

            // Consolidated theme setup: expose a single global setup function so
            // other pages and the injected map HTML all share the same behavior.
            if (!window.__frigid_setupThemeControls) {
                window.__frigid_setupThemeControls = function() {
                    // Apply persisted theme from localStorage if available
                    try {
                        const persisted = localStorage.getItem('theme');
                        if (persisted) {
                            document.documentElement.setAttribute('data-theme', persisted);
                            console.log('Applied persisted theme:', persisted);
                        }
                    } catch (e) { console.warn('Could not access localStorage for theme', e); }

                    // Helper to switch which map container is visible based on data-theme
                    window.__frigid_updateMapTheme = function() {
                        const currentTheme = document.documentElement.getAttribute('data-theme');
                        const lightMap = document.getElementById('light-map');
                        const darkMap = document.getElementById('dark-map');
                        if (lightMap && darkMap) {
                            if (currentTheme === 'dark') {
                                lightMap.style.display = 'none';
                                darkMap.style.display = 'block';
                            } else {
                                lightMap.style.display = 'block';
                                darkMap.style.display = 'none';
                            }
                        }
                    };

                    // Observe for theme changes on the root element so we can update maps
                    if (!window.__frigid_themeObserver) {
                        window.__frigid_themeObserver = new MutationObserver(function(mutations) {
                            mutations.forEach(function(mutation) {
                                if (mutation.attributeName === 'data-theme') {
                                    try { window.__frigid_updateMapTheme(); } catch(e){}
                                    try { localStorage.setItem('theme', document.documentElement.getAttribute('data-theme')); } catch(e) {}
                                }
                            });
                        });
                        window.__frigid_themeObserver.observe(document.documentElement, { attributes: true });
                    }

                    // Delegate theme toggle clicks at document level so buttons
                    // added later are handled (works while maps are loading).
                    if (!window.__frigid_toggleDelegated) {
                        console.log('Installing delegated theme toggle handler');
                        document.addEventListener('click', function (ev) {
                            try {
                                const btn = ev.target && (ev.target.closest ? ev.target.closest('#theme-toggle, .theme-toggle, [data-theme-toggle]') : null);
                                if (!btn) return;
                                console.log('Theme toggle clicked:', btn);
                                const cur = document.documentElement.getAttribute('data-theme');
                                const next = (cur === 'dark') ? 'light' : 'dark';
                                document.documentElement.setAttribute('data-theme', next);
                                try { localStorage.setItem('theme', next); } catch(e) {}
                                // Immediately update map wrappers
                                try { window.__frigid_updateMapTheme && window.__frigid_updateMapTheme(); } catch(e){}
                            } catch (e) {
                                console.warn('Theme toggle handler error', e);
                            }
                        }, { capture: false });
                        window.__frigid_toggleDelegated = true;
                    }

                    // Run initial update
                    try { window.__frigid_updateMapTheme(); } catch(e) {}
                };
            }

            // Ensure the consolidated setup is executed now
            try { window.__frigid_setupThemeControls(); } catch(e) { console.warn('setupThemeControls failed', e); }

            // Define the fetch function
            async function fetchMapData() {
                console.log('Fetching map data...');
                try {
                    const response = await fetch('/api/map-data');
                    console.log('Received response:', response.status);

                    if (!response.ok) {
                        throw new Error('Failed to load map data: ' + response.status);
                    }

                    // Be defensive about the response type. Some servers may return
                    // HTML (or malformed JSON). Try to parse JSON, but fall back to
                    // treating the response as raw HTML if parsing fails.
                    let mapData;
                    const contentType = response.headers.get('content-type') || '';
                    if (contentType.includes('application/json')) {
                        try {
                            mapData = await response.json();
                        } catch (e) {
                            // If json() fails, try text then JSON.parse
                            const text = await response.text();
                            try { mapData = JSON.parse(text); }
                            catch (e2) { mapData = { mapHtml: text }; }
                        }
                    } else {
                        // Not JSON according to headers; try to parse as JSON, else
                        // assume the entire response is the HTML we need.
                        const text = await response.text();
                        try { mapData = JSON.parse(text); }
                        catch (e) { mapData = { mapHtml: text }; }
                    }

                    const mapHtml = (mapData && mapData.mapHtml) ? mapData.mapHtml : String(mapData);
                    console.log('Map data received, rendering...');

                    // Use a <template> to safely parse the returned HTML string and
                    // avoid some innerHTML tokenization quirks.
                    const tpl = document.createElement('template');
                    tpl.innerHTML = mapHtml.trim();

                    // Clear and append
                    mapContainer.innerHTML = '';
                    mapContainer.appendChild(tpl.content.cloneNode(true));

                    // The server now produces both themed maps; no client-side
                    // cloning fallback is necessary. If maps are missing, the
                    // theme updater will simply act on whatever wrappers exist.

                    // Hide loading indicator
                    loadingOverlay.style.display = 'none';
                    // Ensure map container is visible (remove bootstrap 'd-none')
                    mapContainer.style.display = 'block';
                    mapContainer.classList.remove && mapContainer.classList.remove('d-none');

                    // Handle iframes separately as they often need special handling
                    const iframes = mapContainer.querySelectorAll('iframe');
                    console.log('Found', iframes.length, 'iframes');
                    iframes.forEach(iframe => {
                        // If iframe used srcdoc, reassign it (safer). Otherwise
                        // reset src briefly to force reload.
                        if (iframe.hasAttribute('srcdoc')) {
                            const srcdoc = iframe.getAttribute('srcdoc');
                            iframe.removeAttribute('srcdoc');
                            setTimeout(() => { iframe.setAttribute('srcdoc', srcdoc); }, 10);
                        } else {
                            const src = iframe.src;
                            try {
                                iframe.src = '';
                                setTimeout(() => { iframe.src = src; }, 10);
                            } catch (e) {
                                console.warn('Failed to reload iframe safely', e);
                            }
                        }
                    });

                    // Re-execute scripts by creating fresh script elements. This
                    // avoids some tokenization/parsing issues with innerHTML-inserted
                    // <script> content.
                    const scripts = Array.from(mapContainer.querySelectorAll('script'));
                    console.log('Re-executing', scripts.length, 'scripts');
                    scripts.forEach(oldScript => {
                        try {
                            const newScript = document.createElement('script');
                            // Copy attributes, but let setting src happen via property
                            Array.from(oldScript.attributes).forEach(attr => {
                                if (attr.name === 'src') newScript.src = attr.value;
                                else newScript.setAttribute(attr.name, attr.value);
                            });
                            // Copy inline content
                            if (oldScript.textContent) newScript.textContent = oldScript.textContent;

                            if (oldScript.parentNode) {
                                oldScript.parentNode.replaceChild(newScript, oldScript);
                            } else {
                                mapContainer.appendChild(newScript);
                            }
                        } catch (e) {
                            console.warn('Failed to re-execute a script element', e);
                        }
                    });

                    console.log('Map loading complete, running theme update');
                    // Trigger the shared theme updater so the correct map is visible
                    try { window.__frigid_updateMapTheme && window.__frigid_updateMapTheme(); } catch (e) { console.warn('updateMapTheme failed', e); }

                } catch (error) {
                    console.error('Error loading map data:', error);
                    // Escape the error message before injecting into innerHTML to
                    // avoid token parsing / HTML injection problems.
                    const rawMsg = (error && error.message) ? String(error.message) : String(error);
                    const safeMsg = rawMsg.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
                    // Show error message (safe)
                    loadingOverlay.innerHTML = (
                        '<div class="error-content text-center">' +
                        '<i class="fas fa-exclamation-triangle text-danger fa-3x mb-3"></i>' +
                        '<h3>Unable to Load Map Data</h3>' +
                        '<p>There was a problem loading the map: ' + safeMsg + '</p>' +
                        '<button class="btn btn-primary mt-3" onclick="window.location.reload()">Refresh Page</button>' +
                        '</div>'
                    );
                }
            }

            // Start loading the map data after DOM is ready, and ensure theme setup is run first
            function start() {
                try { window.__frigid_setupThemeControls(); } catch(e) { console.warn('setupThemeControls failed', e); }
                // Start fetching map data but don't block UI
                fetchMapData().catch(err => console.error('fetchMapData error', err));
            }
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', start);
            } else {
                start();
            }
    })();
    """)

# Debug script to help diagnose issues
debug_script = Script("""
    console.log('Page loaded with map containers');
    setTimeout(() => {
        const mapContainer = document.getElementById('map-container');
        const lightMap = document.getElementById('light-map');
        const darkMap = document.getElementById('dark-map');
        console.log('Debug status after 5 seconds:');
        console.log('Map container:', mapContainer);
        console.log('Light map element:', lightMap);
        console.log('Dark map element:', darkMap);
        if (mapContainer) {
            console.log('Map container content:', mapContainer.innerHTML.substring(0, 100) + '...');
        }
    }, 5000);
""")