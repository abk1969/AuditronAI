import streamlit as st
from pathlib import Path
from typing import Dict, Any, Optional, Union
from .components import show_code_editor, show_file_browser, show_code_with_highlighting
from .report_style import show_analysis_report
from .api_settings import show_api_settings
from PromptWizard.core.analyzer import analyze_code
from PromptWizard.core.logger import logger
import os
from dotenv import load_dotenv, set_key

def init_page_state() -> None:
    """Initialize page state with default values.
    
    Sets up initial state for page navigation, analysis steps,
    analysis mode, and security configuration thresholds.
    
    Raises:
        ValueError: If environment variables contain invalid values
    """
    try:
        default_state = {
            'page': 'analysis',
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

def check_api_configuration() -> bool:
    """Check if required API keys are configured.
    
    Verifies the presence of either OpenAI or Google API keys
    in the environment variables.
    
    Returns:
        bool: True if API keys are configured, False otherwise
    """
    api_key = os.getenv('OPENAI_API_KEY') or os.getenv('GOOGLE_API_KEY')
    if not api_key:
        st.warning("⚠️ No API key configured. Please configure an API key to continue.")
        with st.expander("🔑 API Configuration", expanded=True):
            show_api_settings()
        return False
    return True

def validate_security_config(config: Dict[str, int]) -> bool:
    """Validate security configuration values.
    
    Args:
        config (Dict[str, int]): Dictionary containing security thresholds
        
    Returns:
        bool: True if configuration is valid, False otherwise
        
    Raises:
        ValueError: If configuration values are invalid
    """
    if not isinstance(config, dict):
        raise ValueError("Configuration must be a dictionary")
        
    required_keys = ['critical_threshold', 'high_threshold', 'medium_threshold']
    if not all(key in config for key in required_keys):
        raise ValueError("Missing required configuration keys")
        
    for key in required_keys:
        if not isinstance(config[key], int):
            raise ValueError(f"{key} must be an integer")
        if config[key] < 0:
            raise ValueError(f"{key} cannot be negative")
            
    return True

def save_security_config(config: Dict[str, int]) -> bool:
    """Save security configuration to .env file.
    
    Args:
        config (Dict[str, int]): Dictionary containing security thresholds
        
    Returns:
        bool: True if save successful, False otherwise
        
    Raises:
        ValueError: If configuration values are invalid
    """
    try:
        if not validate_security_config(config):
            return False
            
        env_path = Path(".env")
        
        # Load existing variables
        load_dotenv(env_path)
        
        # Update thresholds
        set_key(env_path, "CRITICAL_SEVERITY_THRESHOLD", str(config['critical_threshold']))
        set_key(env_path, "HIGH_SEVERITY_THRESHOLD", str(config['high_threshold']))
        set_key(env_path, "MEDIUM_SEVERITY_THRESHOLD", str(config['medium_threshold']))
        
        # Reload variables
        load_dotenv(override=True)
        return True
        
    except Exception as e:
        logger.error(f"Error saving security config: {str(e)}")
        return False

def reset_security_config() -> bool:
    """Reset security thresholds to default values.
    
    Returns:
        bool: True if reset successful, False otherwise
    """
    default_config = {
        'critical_threshold': 0,  # No critical vulnerabilities allowed
        'high_threshold': 2,      # Maximum 2 high vulnerabilities
        'medium_threshold': 5     # Maximum 5 medium vulnerabilities
    }
    
    try:
        if save_security_config(default_config):
            st.session_state.security_config = default_config
            return True
        return False
    except Exception as e:
        logger.error(f"Error resetting security config: {str(e)}")
        return False

def show_analysis_page() -> None:
    """Display the code analysis page with file upload and analysis options.
    
    Handles the main analysis workflow including:
    - Analysis mode selection
    - Code input through various methods
    - Analysis execution
    - Results display
    """
    init_page_state()
    
    try:
        # Check API configuration
        if not check_api_configuration():
            st.warning("⚠️ API configuration required")
            show_api_settings()
            return
        
        # Step 1: Choose analysis mode
        st.markdown("### Step 1: Choose Analysis Mode")
        st.session_state.analysis_mode = st.radio(
            "Analysis Mode",
            ["Single File", "Project Directory", "Code Editor"],
            horizontal=True,
            index=["Single File", "Project Directory", "Code Editor"].index(st.session_state.analysis_mode)
        )
        
        # Code input area
        st.markdown("### Step 2: Source Code")
        code: Optional[str] = None
        filename: Optional[str] = None
        
        if st.session_state.analysis_mode == "Single File":
            uploaded_file = st.file_uploader(
                "Select Python File",
                type=['py'],
                key='file_uploader'
            )
            if uploaded_file:
                code = uploaded_file.getvalue().decode('utf-8', errors='replace')
                filename = uploaded_file.name
                if st.checkbox("View Code", value=False):
                    show_code_with_highlighting(code)
                st.session_state.analysis_step = 2
                
        elif st.session_state.analysis_mode == "Project Directory":
            selected_file = show_file_browser()
            if selected_file and selected_file.exists():
                try:
                    with open(selected_file, 'r', encoding='utf-8') as f:
                        code = f.read()
                    filename = str(selected_file)
                    if st.checkbox("View Code", value=False):
                        show_code_with_highlighting(code)
                    st.session_state.analysis_step = 2
                except UnicodeDecodeError:
                    st.error("Unable to read file: Invalid encoding")
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")
                
        else:  # Code Editor
            code = show_code_editor()
            if code and code.strip():
                filename = "editor.py"
                st.session_state.analysis_step = 2
        
        # Analysis button
        if code:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🚀 Run Analysis", use_container_width=True):
                    with st.spinner("Analysis in progress..."):
                        try:
                            result = analyze_code(code, filename or "unknown.py")
                            st.session_state.last_analysis = result
                            st.session_state.analysis_step = 3
                        except Exception as e:
                            st.error(f"Analysis error: {str(e)}")
                            logger.error(f"Analysis failed: {str(e)}")
        
        # Display results
        if st.session_state.analysis_step == 3 and 'last_analysis' in st.session_state:
            result = st.session_state.last_analysis
            if 'error' in result:
                st.error(f"Analysis error: {result['error']}")
            show_analysis_report(result)
            
            # New analysis button
            if st.button("🔄 New Analysis"):
                st.session_state.analysis_step = 1
                st.experimental_rerun()
        
    except Exception as e:
        logger.error(f"Interface error: {str(e)}")
        st.error("An error occurred. Please try again.")
        if os.getenv('DEBUG', 'false').lower() == 'true':
            st.exception(e)
    
    # Progress indicator
    progress_text = {
        1: "📝 Select Code",
        2: "🔍 Code Loaded, Ready for Analysis",
        3: "✅ Analysis Complete"
    }
    
    st.sidebar.markdown("### Progress")
    st.sidebar.markdown(progress_text.get(st.session_state.analysis_step, ""))
    
    with st.sidebar.expander("ℹ️ Help", expanded=False):
        st.markdown("""
            ### How to Use the Analyzer
            1. Choose an analysis mode
            2. Load or enter your code
            3. Run the analysis
            4. Review results
            
            ### Available Modes
            - **Single File**: Analyze a .py file
            - **Project Directory**: Browse project files
            - **Code Editor**: Enter code directly
        """)

def show_config_page() -> None:
    """Display the configuration page for API and security settings.
    
    Handles:
    - API key configuration
    - Security threshold settings
    - Configuration persistence
    """
    st.markdown("## ⚙️ Configuration")
    
    # API Configuration
    with st.expander("🔑 API Configuration", expanded=True):
        show_api_settings()
    
    # Security Configuration
    with st.expander("🛡️ Security Configuration", expanded=True):
        st.markdown("### Severity Thresholds")
        
        # Action buttons
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🔄 Reset", help="Reset to default values"):
                if reset_security_config():
                    st.success("Configuration reset!")
                else:
                    st.error("Reset failed")
        
        # Initialize session state
        if 'security_config' not in st.session_state:
            try:
                st.session_state.security_config = {
                    'critical_threshold': int(os.getenv('CRITICAL_SEVERITY_THRESHOLD', '0')),
                    'high_threshold': int(os.getenv('HIGH_SEVERITY_THRESHOLD', '2')),
                    'medium_threshold': int(os.getenv('MEDIUM_SEVERITY_THRESHOLD', '5'))
                }
            except ValueError as e:
                logger.error(f"Error loading security config: {str(e)}")
                st.error("Invalid security configuration values")
                return
        
        # Configuration interface
        config_changed = False
        
        new_critical = st.slider(
            "Critical Threshold", 0, 5, 
            st.session_state.security_config['critical_threshold'],
            help="Maximum number of critical vulnerabilities allowed"
        )
        if new_critical != st.session_state.security_config['critical_threshold']:
            st.session_state.security_config['critical_threshold'] = new_critical
            config_changed = True
        
        new_high = st.slider(
            "High Threshold", 0, 10, 
            st.session_state.security_config['high_threshold'],
            help="Maximum number of high vulnerabilities allowed"
        )
        if new_high != st.session_state.security_config['high_threshold']:
            st.session_state.security_config['high_threshold'] = new_high
            config_changed = True
        
        new_medium = st.slider(
            "Medium Threshold", 0, 15, 
            st.session_state.security_config['medium_threshold'],
            help="Maximum number of medium vulnerabilities allowed"
        )
        if new_medium != st.session_state.security_config['medium_threshold']:
            st.session_state.security_config['medium_threshold'] = new_medium
            config_changed = True
        
        # Save changes
        if config_changed:
            if st.button("💾 Save Configuration"):
                try:
                    if save_security_config(st.session_state.security_config):
                        st.success("Configuration saved!")
                    else:
                        st.error("Failed to save configuration")
                except Exception as e:
                    st.error(f"Save error: {str(e)}")
                    logger.error(f"Configuration save failed: {str(e)}")
