"""Custom CSS styles for Notion-like UI."""

def get_custom_css(theme: str = "light"):
    """
    Get custom CSS for the application based on the selected theme.
    """
    if theme == "dark":
        vars = """
        --bg-color: #191919;
        --sidebar-bg: #202020;
        --card-bg: #252525;
        --text-color: #FFFFFF;
        --text-secondary: #9B9B9B;
        --border-color: #2F2F2F;
        --accent-color: #2383E2;
        --hover-bg: #2F2F2F;
        --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
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
        --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        """

    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    :root {{
        {vars}
    }}

    /* Global Overrides */
    .stApp {{
        background-color: var(--bg-color);
        font-family: 'Inter', sans-serif;
        color: var(--text-color);
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: var(--sidebar-bg);
        border-right: 1px solid var(--border-color);
    }}

    /* Header & Navigation */
    header {{ visibility: visible !important; background: transparent !important; }}
    [data-testid="stHeader"] {{ background: transparent !important; }}
    
    /* Move Sidebar Toggle to Top Right (Simulated) */
    /* This is hard in Streamlit without custom JS, so we'll just make the default one beautiful */
    [data-testid="stSidebarCollapse"] {{
        position: fixed;
        right: 5rem;
        top: 0.75rem;
        z-index: 99999;
        background: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 6px !important;
    }}

    /* Cards */
    .notion-card {{
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 2rem;
        box-shadow: var(--shadow);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 1.5rem;
        animation: fadeIn 0.6s ease-out;
    }}
    
    .notion-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border-color: var(--accent-color);
    }}

    /* Chat Bubbles */
    .stChatMessage {{
        border-radius: 12px !important;
        border: 1px solid transparent !important;
        margin-bottom: 1rem !important;
        padding: 1rem !important;
        transition: background 0.2s;
    }}
    
    .stChatMessage:hover {{
        background-color: var(--hover-bg) !important;
        border-color: var(--border-color) !important;
    }}

    /* Inputs */
    .stChatInput {{
        border-radius: 12px !important;
        border: 1px solid var(--border-color) !important;
        background: var(--card-bg) !important;
        padding: 0.5rem !important;
    }}

    /* Animations */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* Progress and Success */
    .stProgress > div > div > div > div {{
        background-color: var(--accent-color);
        border-radius: 10px;
    }}

    /* Welcome Icons */
    .welcome-icon {{
        font-size: 4rem;
        margin-bottom: 1rem;
        filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));
    }}

    </style>
    """
