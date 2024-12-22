import streamlit as st
from pathlib import Path
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from PromptWizard.core.custom_dataset import CustomDataset
from PromptWizard.app.config import (
    setup_page, 
    load_css, 
    apply_theme,
    load_user_config
)
from PromptWizard.app.components import (
    show_code_editor,
    show_file_browser,
    show_code_with_highlighting,
    show_active_service,
    add_service_indicator_css
)
from PromptWizard.app.report_style import apply_report_style, show_analysis_report
from PromptWizard.app.layout_manager import init_layout_state, show_layout_controls
from PromptWizard.app.api_settings import show_api_settings
from PromptWizard.core.logger import setup_logger
from PromptWizard.core.history import AnalysisHistory
from PromptWizard.core.usage_stats import UsageStats
from PromptWizard.core.security_analyzer import SecurityAnalyzer
from PromptWizard.core.network_security import NetworkSecurity
from PromptWizard.app.pages import show_analysis_page, show_config_page
from PromptWizard.app.stats_page import show_stats_page

logger = None

# Initialize core services
try:
    logger = setup_logger()
    history = AnalysisHistory()
    usage_stats = UsageStats()
    security_analyzer = SecurityAnalyzer()
except Exception as e:
    st.error(f"Failed to initialize core services: {str(e)}")
    if logger:
        logger.error(f"Initialization error: {str(e)}")
    st.stop()

def init_session_state() -> None:
    """Initialize session state variables with default values.
    
    Sets up the initial state for analysis results, current file, analysis step,
    analysis mode, last analysis, and security configuration thresholds.
    """
    try:
        default_state = {
            'analysis_results': [],
            'current_file': None,
            'analysis_step': 1,
            'analysis_mode': "Single File",
            'last_analysis': None,
            'security_config': {
                'critical_threshold': int(os.getenv('CRITICAL_SEVERITY_THRESHOLD', '0')),
                'high_threshold': int(os.getenv('HIGH_SEVERITY_THRESHOLD', '2')),
                'medium_threshold': int(os.getenv('MEDIUM_SEVERITY_THRESHOLD', '5'))
            }
        }
        
        for key, value in default_state.items():
            if key not in st.session_state:
                st.session_state[key] = value
    except ValueError as e:
        logger.error(f"Error parsing environment variables: {str(e)}")
        st.error("Invalid configuration values in environment variables")
        st.stop()

def analyze_code(code: str, filename: str = "code.py") -> Dict[str, Any]:
    """Analyze Python code and generate comprehensive report.
    
    Args:
        code (str): Python source code to analyze
        filename (str): Name of the file being analyzed
        
    Returns:
        Dict[str, Any]: Analysis results including AI insights, security scan, and metrics
        
    Raises:
        ValueError: If code is empty or invalid
        RuntimeError: If analysis fails
    """
    if not code.strip():
        raise ValueError("Code cannot be empty")
        
    try:
        # AI Analysis
        dataset = CustomDataset("streamlit_analysis")
        result = dataset.generate_completion("project_analysis", {
            "file_path": filename,
            "code": code
        })
        
        # Security Analysis
        security_results = security_analyzer.analyze(code, filename)
        
        # Basic Statistics
        lines = code.split('\n')
        stats = {
            'Lines of Code': len(lines),
            'Characters': len(code),
            'Functions': len([l for l in lines if l.strip().startswith('def ')]),
            'Classes': len([l for l in lines if l.strip().startswith('class ')])
        }
        
        analysis_result = {
            "file": filename,
            "code": code,
            "analysis": result,
            "stats": stats,
            "security": security_results
        }
        
        # Save to history
        history.add_entry(analysis_result)
        
        # Record stats
        usage_stats.record_analysis(os.getenv('AI_SERVICE', 'openai'))
        
        logger.info(f"Analysis completed successfully for {filename}")
        return analysis_result
        
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        usage_stats.record_error()
        raise RuntimeError(f"Analysis failed: {str(e)}")

def main() -> None:
    """Main application entry point.
    
    Sets up the Streamlit application, initializes configurations,
    applies styling, and handles the main navigation flow.
    """
    # Page configuration must be first
    setup_page()
    
    # Load environment variables
    load_dotenv()
    
    # Initialize states and configurations
    init_session_state()
    init_layout_state()
    
    # Load user configuration
    user_config = load_user_config()
    
    # Apply theme
    apply_theme(user_config.get('theme', 'Light'))
    
    # Load styles
    load_css()
    add_service_indicator_css()
    apply_report_style()
    
    # Configure network security
    network_security = NetworkSecurity()
    network_security.write_streamlit_config()
    
    if not network_security.is_secure():
        st.warning("⚠️ Insecure network configuration - Check logs for details")
    
    # Application header
    st.title("🔍 AuditronAI - Python Code Analyzer")
    
    # Welcome message
    if 'first_visit' not in st.session_state:
        st.session_state.first_visit = False
        st.balloons()
        st.success("""
            👋 Welcome to AuditronAI!
            
            This tool helps you analyze your Python code with:
            - Advanced security analysis
            - Vulnerability detection
            - Quality metrics
            - Improvement recommendations
            
            Start by choosing an analysis mode in the left menu.
        """)
    
    # Main menu with visual indicator
    st.sidebar.markdown("## 🧭 Navigation")
    menu = st.sidebar.radio(
        "Menu",  # Label for accessibility
        ["Analysis", "Statistics", "Configuration"]
    )
    
    # Display corresponding page
    if menu == "Analysis":
        show_analysis_page()
    elif menu == "Statistics":
        show_stats_page(history, usage_stats)
    else:
        show_config_page()

if __name__ == "__main__":
    main()
