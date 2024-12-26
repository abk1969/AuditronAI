import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
import os
import re
from typing import Dict, Optional, Literal
from enum import Enum

class AIService(str, Enum):
    """Supported AI services."""
    OPENAI = "openai"
    GOOGLE = "google"

class OpenAIModel(str, Enum):
    """Available OpenAI models."""
    GPT4_MINI = "gpt-4o-mini"
    GPT4O = "gpt-4o"
    GPT4 = "gpt-4"

class GeminiModel(str, Enum):
    """Available Google Gemini models."""
    FLASH = "gemini-2.0-flash-exp"
    PRO = "gemini-pro"
    PRO_VISION = "gemini-pro-vision"

def sanitize_env_value(value: str) -> str:
    """Sanitize environment variable value.
    
    Args:
        value (str): Value to sanitize
        
    Returns:
        str: Sanitized value with potentially harmful characters removed
    """
    # Remove any non-alphanumeric characters except common special chars
    return re.sub(r'[^a-zA-Z0-9\-_\.]', '', value)

def validate_api_key(key: str, service: AIService) -> bool:
    """Validate API key format.
    
    Args:
        key (str): API key to validate
        service (AIService): Service the key is for
        
    Returns:
        bool: True if key format is valid, False otherwise
    """
    if not key:
        return False
        
    if service == AIService.OPENAI:
        return bool(re.match(r'^sk-[a-zA-Z0-9]{32,}$', key))
    elif service == AIService.GOOGLE:
        return bool(re.match(r'^[a-zA-Z0-9_-]{39}$', key))
    return False

def update_env_file(new_values: Dict[str, str]) -> bool:
    """Update the .env file with new values.
    
    Args:
        new_values (Dict[str, str]): Dictionary of environment variables to update
        
    Returns:
        bool: True if update successful, False otherwise
        
    Raises:
        OSError: If file operations fail
        ValueError: If environment values are invalid
    """
    try:
        env_path = Path(".env")
        
        # Validate and sanitize new values
        sanitized_values = {
            sanitize_env_value(k): sanitize_env_value(v)
            for k, v in new_values.items()
        }
        
        # Read existing .env file
        current_env = {}
        if env_path.exists():
            try:
                with open(env_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            try:
                                key, value = line.split('=', 1)
                                current_env[key.strip()] = value.strip()
                            except ValueError:
                                continue  # Skip invalid lines
            except UnicodeDecodeError:
                st.error("Invalid file encoding in .env file")
                return False
        
        # Update with new values
        current_env.update(sanitized_values)
        
        # Write updated .env file
        try:
            with open(env_path, 'w', encoding='utf-8') as f:
                for key, value in current_env.items():
                    f.write(f"{key}={value}\n")
        except OSError as e:
            st.error(f"Failed to write configuration: {str(e)}")
            return False
        
        # Reload environment variables
        load_dotenv(override=True)
        return True
        
    except Exception as e:
        st.error(f"Failed to update configuration: {str(e)}")
        return False

def get_api_key(service: AIService) -> Optional[str]:
    """Get API key for the specified service.
    
    Args:
        service (AIService): Service to get API key for
        
    Returns:
        Optional[str]: API key if found and valid, None otherwise
    """
    if service == AIService.OPENAI:
        key = os.getenv('OPENAI_API_KEY')
        return key if key and validate_api_key(key, service) else None
    elif service == AIService.GOOGLE:
        key = os.getenv('GOOGLE_API_KEY')
        return key if key and validate_api_key(key, service) else None
    return None

def show_api_settings() -> None:
    """Display API configuration settings in the sidebar.
    
    Handles:
    - Service selection between OpenAI and Google Gemini
    - API key configuration
    - Model selection
    - Configuration persistence
    - Current settings display
    """
    st.markdown("### 🔑 API Configuration")
    
    # AI Service selection
    current_service = os.getenv("AI_SERVICE", "openai").lower()
    service = st.selectbox(
        "AI Service",
        ["OpenAI", "Google Gemini"],
        index=0 if current_service == AIService.OPENAI else 1,
        help="Select the AI service to use for analysis"
    )
    
    # Service-specific configuration
    if service == "OpenAI":
        api_key = st.text_input(
            "OpenAI API Key",
            value=get_api_key(AIService.OPENAI) or "",
            type="password",
            help="Enter your OpenAI API key (starts with 'sk-')"
        )
        
        model = st.selectbox(
            "Model",
            [m.value for m in OpenAIModel],
            index=0,
            help="Select the OpenAI model to use"
        )
        
        if st.button("💾 Save OpenAI Config", help="Save OpenAI configuration"):
            if not api_key:
                st.warning("⚠️ Please enter an API key")
            elif not validate_api_key(api_key, AIService.OPENAI):
                st.error("❌ Invalid OpenAI API key format")
            else:
                if update_env_file({
                    "AI_SERVICE": AIService.OPENAI.value,
                    "OPENAI_API_KEY": api_key,
                    "OPENAI_MODEL": model
                }):
                    st.success("✅ OpenAI configuration saved!")
                    
    else:  # Google Gemini
        api_key = st.text_input(
            "Google API Key",
            value=get_api_key(AIService.GOOGLE) or "",
            type="password",
            help="Enter your Google API key (39 characters)"
        )
        
        model = st.selectbox(
            "Model",
            [m.value for m in GeminiModel],
            index=0,
            help="Select the Gemini model to use"
        )
        
        if st.button("💾 Save Gemini Config", help="Save Gemini configuration"):
            if not api_key:
                st.warning("⚠️ Please enter an API key")
            elif not validate_api_key(api_key, AIService.GOOGLE):
                st.error("❌ Invalid Google API key format")
            else:
                if update_env_file({
                    "AI_SERVICE": AIService.GOOGLE.value,
                    "GOOGLE_API_KEY": api_key,
                    "GOOGLE_MODEL": model
                }):
                    st.success("✅ Gemini configuration saved!")
    
    # Display current configuration
    st.markdown("#### Current Configuration")
    current_service = os.getenv('AI_SERVICE', 'openai').upper()
    current_model = os.getenv(f"{service.upper().replace(' ', '_')}_MODEL", 'Not set')
    api_status = '🟢 Configured' if get_api_key(
        AIService.OPENAI if service == "OpenAI" else AIService.GOOGLE
    ) else '🔴 Not configured'
    
    st.markdown(f"""
        **Active Service:** {current_service}  
        **Model:** {current_model}  
        **API Key Status:** {api_status}
    """)
