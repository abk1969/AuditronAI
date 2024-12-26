import streamlit as st
from typing import Dict, Any, List, Optional
import json
from pathlib import Path
from enum import Enum

# Constants
DEFAULT_MAX_FILE_SIZE = 500 * 1024  # 500 KB
DEFAULT_EXCLUDED_PATTERNS = ['venv', '__pycache__', '*.pyc']
CONFIG_DIR = ".AuditronAI"
CONFIG_FILE = "config.json"
REPO_URL = "https://github.com/your-repo/AuditronAI"

class Theme(str, Enum):
    """Available UI themes."""
    LIGHT = "Light"
    DARK = "Dark"
    CUSTOM = "Custom"

def load_user_config() -> Dict[str, Any]:
    """Load user configuration from file.
    
    Returns:
        Dict[str, Any]: User configuration dictionary
        
    Note:
        Returns empty dict if config file doesn't exist or is invalid
    """
    config_path = Path.home() / CONFIG_DIR / CONFIG_FILE
    
    if not config_path.exists():
        return {}
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError, OSError) as e:
        st.error(f"Error loading configuration: {str(e)}")
        return {}

def save_user_config(config: Dict[str, Any]) -> bool:
    """Save user configuration to file.
    
    Args:
        config (Dict[str, Any]): Configuration to save
        
    Returns:
        bool: True if save successful, False otherwise
    """
    try:
        config_dir = Path.home() / CONFIG_DIR
        config_dir.mkdir(parents=True, exist_ok=True)
        
        config_path = config_dir / CONFIG_FILE
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        return True
    except OSError as e:
        st.error(f"Error saving configuration: {str(e)}")
        return False

def validate_excluded_patterns(patterns: List[str]) -> List[str]:
    """Validate and clean excluded file patterns.
    
    Args:
        patterns (List[str]): List of file patterns to validate
        
    Returns:
        List[str]: List of valid patterns
    """
    valid_patterns = []
    for pattern in patterns:
        pattern = pattern.strip()
        if pattern and not any(c in pattern for c in ['<', '>', '|', ':', '"', '?', '*/']):
            valid_patterns.append(pattern)
    return valid_patterns

def show_config_page() -> None:
    """Display the configuration page.
    
    Handles:
    - Theme selection
    - File size limits
    - Exclusion patterns
    - Analysis options
    - Configuration persistence
    """
    st.markdown("## ⚙️ Configuration")
    
    config = load_user_config()
    
    # Theme
    theme = st.selectbox(
        "Theme",
        [t.value for t in Theme],
        index=[t.value for t in Theme].index(
            config.get('theme', Theme.LIGHT.value)
        ),
        help="Select the application theme"
    )
    
    # Maximum file size
    max_size = st.number_input(
        "Maximum file size (KB)",
        value=config.get('max_file_size', DEFAULT_MAX_FILE_SIZE) // 1024,
        min_value=1,
        help="Maximum size for files to be analyzed"
    )
    
    # Exclusion patterns
    excluded = st.text_area(
        "Patterns to exclude (one per line)",
        value="\n".join(config.get('excluded_patterns', DEFAULT_EXCLUDED_PATTERNS)),
        help="File patterns to exclude from analysis"
    )
    
    # Analysis options
    st.markdown("### Analysis Options")
    show_stats = st.checkbox(
        "Show statistics",
        value=config.get('show_stats', True),
        help="Display code statistics in analysis results"
    )
    show_code = st.checkbox(
        "Show source code",
        value=config.get('show_code', True),
        help="Display source code in analysis results"
    )
    
    # Save changes
    if st.button("💾 Save Configuration"):
        excluded_patterns = validate_excluded_patterns([
            p.strip() for p in excluded.split('\n') if p.strip()
        ])
        
        new_config = {
            'theme': theme,
            'max_file_size': max_size * 1024,
            'excluded_patterns': excluded_patterns,
            'show_stats': show_stats,
            'show_code': show_code
        }
        
        if save_user_config(new_config):
            st.success("✅ Configuration saved!")

def setup_page() -> None:
    """Configure Streamlit page settings.
    
    Sets up:
    - Page title and icon
    - Layout configuration
    - Menu items and help links
    """
    st.set_page_config(
        page_title="AuditronAI - Python Code Analyzer",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': f"{REPO_URL}",
            'Report a bug': f"{REPO_URL}/issues",
            'About': """
            # AuditronAI

            Python code analyzer with AI and enhanced security.
            
            ## Licenses
            This project uses the following open source components:
            - Streamlit (Apache License 2.0)
            - Bandit (Apache License 2.0)
            - Safety (MIT License)
            - Semgrep (LGPL-2.1 License)
            - Pylint (GPL-2.0 License)
            - Python-dotenv (BSD License)
            - Loguru (MIT License)
            
            ## Credits
            - User interface based on Streamlit
            - Security analysis: Bandit, Safety, Semgrep, Pylint
            - Logging: Loguru
            - Configuration: Python-dotenv
            
            ## Project License
            This project is distributed under the MIT license.
            Copyright (c) 2024 AuditronAI
            """
        }
    )

def apply_theme(theme: str = Theme.LIGHT.value) -> None:
    """Apply the selected theme to the application.
    
    Args:
        theme (str): Theme name to apply (Light/Dark/Custom)
    """
    if theme == Theme.DARK.value:
        st.markdown("""
            <style>
                .stApp { background-color: #0E1117; }
                .stButton > button { background-color: #262730; }
                .stTextInput > div > div > input { background-color: #262730; }
                .stats-card { background-color: #1E1E1E; color: white; }
                .navigation-menu { background-color: #262730; }
                .breadcrumb { background-color: #262730; }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
                .stats-card { background-color: white; }
                .navigation-menu { background-color: #f8f9fa; }
                .breadcrumb { background-color: #f8f9fa; }
            </style>
        """, unsafe_allow_html=True)

def load_css() -> None:
    """Load custom CSS styles.
    
    Applies:
    - Base styles
    - Navigation styles
    - Component styles
    - Animations
    """
    st.markdown("""
        <style>
        /* Base styles */
        .stApp {
            transition: background-color 0.3s ease;
        }
        
        /* Navigation */
        .navigation-menu {
            padding: 1rem;
            border-radius: 5px;
            margin-bottom: 1rem;
            transition: background-color 0.3s ease;
        }
        
        /* Components */
        .file-tree {
            font-family: 'JetBrains Mono', monospace;
            line-height: 1.5;
        }
        
        .breadcrumb {
            padding: 0.5rem;
            border-radius: 3px;
            margin-bottom: 1rem;
            transition: background-color 0.3s ease;
        }
        
        .stats-card {
            padding: 1rem;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
            transition: all 0.3s ease;
        }
        
        /* Animations */
        .stButton > button {
            transition: all 0.2s ease;
        }
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
        </style>
    """, unsafe_allow_html=True)
