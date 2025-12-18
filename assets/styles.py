"""Custom CSS styles for Notion-like UI."""

def get_custom_css(theme: str = "light"):
    """
    Get custom CSS for the application based on the selected theme.
    
    Args:
        theme: 'light' or 'dark'
    """
    
    # Define color palettes with strict Notion contrast
    if theme == "dark":
        vars = """
        --bg-color: #191919;
        --sidebar-bg: #202020;
        --card-bg: #252525;
        --text-color: #FFFFFF; /* Pure White */
        --text-secondary: #B0B0B0; /* Silver */
        --border-color: #2F2F2F;
        --accent-color: #0A85D1;
        --hover-bg: #2F2F2F;
        --code-bg: #2c2c2c;
        --logo-filter: invert(1) brightness(100%);
        """
    else:
        vars = """
        --bg-color: #FFFFFF;
        --sidebar-bg: #F7F7F5;
        --card-bg: #FFFFFF;
        --text-color: #37352F;
        --text-secondary: #787774;
        --border-color: #E9E9E7;
        --accent-color: #2383E2;
        --hover-bg: #F1F1EF;
        --code-bg: #F7F6F3;
        --logo-filter: none;
        """

    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    :root {{
        {vars}
    }}

    /* Global Settings */
    * {{
        box-sizing: border-box;
    }}

    /* Main App Background */
    .stApp {{
        background-color: var(--bg-color);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
        color: var(--text-color);
    }}

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background-color: var(--sidebar-bg);
        border-right: 1px solid var(--border-color);
    }}
    
    /* Centered Sidebar Content Class */
    .sidebar-content {{
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding-top: 2rem;
    }}

    /* Hide Header/Footer */
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    #MainMenu {{visibility: hidden;}}

    /* Top Right Toggle Positioning */
    .theme-toggle-container {{
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 99999;
    }}

    /* Headings */
    h1, h2, h3, h4, h5, h6 {{
        color: var(--text-color) !important;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        letter-spacing: -0.02em;
    }}
    
    p, li {{
        color: var(--text-color);
        line-height: 1.6;
    }}
    
    /* Secondary Text */
    .small-font, small, caption {{
        color: var(--text-secondary) !important;
    }}

    /* Card / Container Styling */
    .stContainer, [data-testid="stVerticalBlock"] > div > div {{
        background-color: transparent;
        border: 1px solid transparent; 
    }}

    /* Notion-style Buttons */
    .stButton > button {{
        background-color: transparent;
        border: 1px solid var(--border-color);
        color: var(--text-color);
        border-radius: 4px;
        padding: 0.5rem 1rem;
        transition: background-color 0.2s;
    }}
    
    .stButton > button:hover {{
        background-color: var(--hover-bg);
        border-color: var(--text-secondary);
        color: var(--text-color);
    }}

    /* Primary Buttons */
    .stButton > button[kind="primary"] {{
        background-color: var(--accent-color);
        color: white;
        border: none;
    }}
    
    /* Inputs */
    .stTextInput input, .stChatInput input {{
        background-color: transparent;
        border: 1px solid var(--border-color);
        color: var(--text-color);
        border-radius: 6px;
    }}
    
    .stTextInput input:focus, .stChatInput input:focus {{
        border-color: var(--accent-color);
        box-shadow: 0 0 0 2px rgba(35, 131, 226, 0.2);
    }}

    /* Neural Pulse Thinking Animation */
    .thinking-container {{
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 16px;
        border-radius: 8px;
        background-color: var(--hover-bg);
        border: 1px solid var(--border-color);
        margin-top: 10px;
        margin-bottom: 20px;
        width: fit-content;
    }}
    
    .neural-dots {{
        display: flex;
        gap: 4px;
    }}
    
    .dot {{
        width: 6px;
        height: 6px;
        background-color: var(--accent-color);
        border-radius: 50%;
        animation: pulse 1.4s infinite ease-in-out both;
    }}
    
    .dot:nth-child(1) {{ animation-delay: -0.32s; }}
    .dot:nth-child(2) {{ animation-delay: -0.16s; }}
    
    @keyframes pulse {{
        0%, 80%, 100% {{ transform: scale(0); opacity: 0.5; }}
        40% {{ transform: scale(1); opacity: 1; }}
    }}
    
    .thinking-text {{
        font-size: 0.9rem;
        color: var(--text-secondary);
        font-weight: 500;
    }}

    /* Document Badges (Sidebar) */
    .doc-badge {{
        background-color: var(--code-bg);
        color: var(--text-secondary);
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.75rem;
        border: 1px solid var(--border-color);
    }}

    /* Centered Welcome Screen */
    .welcome-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 4rem 2rem;
    }}
    
    /* Horizontal Rule */
    hr {{
        border-color: var(--border-color);
        opacity: 0.5;
    }}

    </style>
    """
