import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class HTMLUtils:
    @staticmethod
    def create_root_index():
        """Creates a root index.html that lists all content types and dates"""
        index_path = os.path.join("./generated", 'index.html')
        
        # Get all date folders for both content types
        youtube_dates = sorted([d for d in os.listdir("./generated/youtube") 
                              if os.path.isdir(os.path.join("./generated/youtube", d))], reverse=True)
        reddit_dates = sorted([d for d in os.listdir("./generated/reddit") 
                             if os.path.isdir(os.path.join("./generated/reddit", d))], reverse=True)
        
        content = '''
        <html>
        <head>
            <title>Crypto Market Intelligence - Archive</title>
            <style>
                :root {
                    --bg-color: #ffffff;
                    --text-color: #333333;
                    --link-color: #007bff;
                    --nav-bg: #f8f9fa;
                    --border-color: #dee2e6;
                    --hover-bg: #e9ecef;
                }
                
                [data-theme="dark"] {
                    --bg-color: #1a1a1a;
                    --text-color: #ffffff;
                    --link-color: #66b0ff;
                    --nav-bg: #2d2d2d;
                    --border-color: #404040;
                    --hover-bg: #404040;
                }
                
                body { 
                    font-family: Arial, sans-serif; 
                    line-height: 1.6; 
                    margin: 0; 
                    padding: 20px; 
                    max-width: 1200px; 
                    margin: 0 auto;
                    background-color: var(--bg-color);
                    color: var(--text-color);
                }
                
                .content-section { margin-bottom: 40px; }
                
                .date-list { 
                    list-style: none; 
                    padding: 0; 
                }
                
                .date-list li { 
                    margin-bottom: 15px;
                    padding: 10px;
                    background-color: var(--nav-bg);
                    border-radius: 5px;
                }
                
                .date-list a {
                    text-decoration: none;
                    color: var(--link-color);
                    font-size: 1.1em;
                }
                
                .date-list a:hover { text-decoration: underline; }
                
                h1, h2 { color: var(--text-color); }
                h1 { margin-bottom: 30px; }
                h2 { margin-bottom: 20px; }
                
                .nav-tabs {
                    display: flex;
                    margin-bottom: 30px;
                    border-bottom: 2px solid var(--border-color);
                }
                
                .nav-tabs a {
                    padding: 10px 20px;
                    text-decoration: none;
                    color: var(--text-color);
                    margin-right: 2px;
                    border-radius: 4px 4px 0 0;
                }
                
                .nav-tabs a:hover {
                    background-color: var(--hover-bg);
                }
                
                .nav-tabs a.active {
                    color: var(--link-color);
                    border: 2px solid var(--border-color);
                    border-bottom: 2px solid var(--bg-color);
                    margin-bottom: -2px;
                }
                
                .theme-switch {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    padding: 10px;
                    background-color: var(--nav-bg);
                    border: 1px solid var(--border-color);
                    border-radius: 5px;
                    cursor: pointer;
                    color: var(--text-color);
                }
                
                .theme-switch:hover {
                    background-color: var(--hover-bg);
                }
            </style>
        </head>
        <body>
            <button class="theme-switch" onclick="toggleTheme()">Toggle Theme</button>
            <h1>Crypto Market Intelligence Hub</h1>
            
            <div class="nav-tabs">
                <a href="#youtube" class="active" onclick="showSection('youtube'); return false;">YouTube Analysis</a>
                <a href="#reddit" onclick="showSection('reddit'); return false;">Reddit Insights</a>
            </div>
            
            <div id="youtube" class="content-section">
                <h2>Latest YouTube Summaries</h2>
                <ul class="date-list">
        '''
        
        # Add YouTube summaries
        for folder in youtube_dates:
            display_date = f"{folder[:4]}-{folder[4:6]}-{folder[6:]}"
            content += f'<li><a href="youtube/{folder}/index.html">YouTube Summaries for {display_date}</a></li>\n'
        
        content += '''
                </ul>
            </div>
            
            <div id="reddit" class="content-section" style="display: none;">
                <h2>Latest Reddit Analysis</h2>
                <ul class="date-list">
        '''
        
        # Add Reddit summaries
        for folder in reddit_dates:
            display_date = f"{folder[:4]}-{folder[4:6]}-{folder[6:]}"
            content += f'<li><a href="reddit/{folder}/reddit_summary.html">Reddit Analysis for {display_date}</a></li>\n'
        
        content += '''
                </ul>
            </div>

            <script>
            // Theme handling
            function setTheme(theme) {
                document.documentElement.setAttribute('data-theme', theme);
                localStorage.setItem('theme', theme);
            }
            
            function toggleTheme() {
                const currentTheme = localStorage.getItem('theme') || 'light';
                const newTheme = currentTheme === 'light' ? 'dark' : 'light';
                setTheme(newTheme);
            }
            
            // Initialize theme
            const savedTheme = localStorage.getItem('theme') || 'light';
            setTheme(savedTheme);
            
            // Tab handling
            function showSection(section) {
                document.getElementById('youtube').style.display = section === 'youtube' ? 'block' : 'none';
                document.getElementById('reddit').style.display = section === 'reddit' ? 'block' : 'none';
                
                // Update active tab
                document.querySelectorAll('.nav-tabs a').forEach(tab => {
                    if (tab.getAttribute('href') === '#' + section) {
                        tab.classList.add('active');
                    } else {
                        tab.classList.remove('active');
                    }
                });
            }
            </script>
        </body>
        </html>
        '''
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)
            logger.info("Created/updated root index.html")

    @staticmethod
    def get_html_template(title, content, include_theme=True):
        """Returns a standard HTML template with optional theme support"""
        theme_style = '''
            :root {
                --bg-color: #ffffff;
                --text-color: #333333;
                --link-color: #007bff;
                --nav-bg: #f8f9fa;
                --border-color: #dee2e6;
                --hover-bg: #e9ecef;
            }
            
            [data-theme="dark"] {
                --bg-color: #1a1a1a;
                --text-color: #ffffff;
                --link-color: #66b0ff;
                --nav-bg: #2d2d2d;
                --border-color: #404040;
                --hover-bg: #404040;
            }
        ''' if include_theme else ''
        
        theme_script = '''
            function setTheme(theme) {
                document.documentElement.setAttribute('data-theme', theme);
                localStorage.setItem('theme', theme);
            }
            
            function toggleTheme() {
                const currentTheme = localStorage.getItem('theme') || 'light';
                const newTheme = currentTheme === 'light' ? 'dark' : 'light';
                setTheme(newTheme);
            }
            
            // Initialize theme
            const savedTheme = localStorage.getItem('theme') || 'light';
            setTheme(savedTheme);
        ''' if include_theme else ''
        
        theme_button = '''
            <button class="theme-switch" onclick="toggleTheme()">Toggle Theme</button>
        ''' if include_theme else ''
        
        return f'''
        <html>
        <head>
            <title>{title}</title>
            <style>
                {theme_style}
                body {{ 
                    font-family: Arial, sans-serif; 
                    line-height: 1.6; 
                    margin: 0; 
                    padding: 20px; 
                    max-width: 1200px; 
                    margin: 0 auto;
                    background-color: var(--bg-color);
                    color: var(--text-color);
                }}
                nav {{ 
                    margin-bottom: 20px; 
                    padding: 10px; 
                    background-color: var(--nav-bg);
                }}
                nav a {{ 
                    margin-right: 15px; 
                    text-decoration: none; 
                    color: var(--link-color);
                }}
                nav a:hover {{ text-decoration: underline; }}
                .theme-switch {{
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    padding: 10px;
                    background-color: var(--nav-bg);
                    border: 1px solid var(--border-color);
                    border-radius: 5px;
                    cursor: pointer;
                    color: var(--text-color);
                }}
                .theme-switch:hover {{
                    background-color: var(--hover-bg);
                }}
            </style>
        </head>
        <body>
            {theme_button}
            <nav>
                <a href="/index.html">Home</a>
                <a href="index.html">Today's Summaries</a>
            </nav>
            {content}
            <script>
                {theme_script}
            </script>
        </body>
        </html>
        ''' 