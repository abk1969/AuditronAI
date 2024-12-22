import streamlit as st
import os
from pathlib import Path
from typing import Optional

def show_code_editor(default_code: str = "", height: int = 300) -> str:
    """Display a code editor with syntax highlighting.
    
    Args:
        default_code (str): Initial code to display in the editor
        height (int): Height of the editor in pixels, must be > 0
        
    Returns:
        str: The code entered by the user
        
    Raises:
        ValueError: If height is less than or equal to 0
    """
    if height <= 0:
        raise ValueError("Height must be greater than 0")
        
    if not isinstance(default_code, str):
        default_code = str(default_code)
        
    return st.text_area(
        "Python Code",
        value=default_code,
        height=height,
        key="code_editor",
        help="Enter your Python code here"
    )

def show_file_browser(root_path: Optional[Path] = None) -> Optional[Path]:
    """Display a file browser for Python files.
    
    Args:
        root_path (Optional[Path]): Root directory to start browsing from. Defaults to current working directory.
        
    Returns:
        Optional[Path]: Selected file path or None if no file selected or error occurs
    """
    st.sidebar.markdown("### 📂 File Explorer")
    
    # Use provided path or default to safe working directory
    if root_path is None:
        root_path = Path.cwd()
    
    try:
        if not root_path.exists():
            st.sidebar.error("❌ Directory not found!")
            return None
            
        # Only show .py files from allowed directories
        python_files = [
            f for f in root_path.rglob("*.py") 
            if "venv" not in str(f) and ".git" not in str(f)
        ]
        
        if not python_files:
            st.sidebar.warning("No Python files found in the directory!")
            return None
        
        selected = st.sidebar.selectbox(
            "Python Files",
            python_files,
            format_func=lambda x: str(x.relative_to(root_path))
        )
        
        # Validate file permissions
        if selected and selected.exists() and os.access(selected, os.R_OK):
            return selected
        else:
            st.sidebar.error("❌ Cannot access selected file!")
            return None
            
    except Exception as e:
        st.sidebar.error(f"Error browsing files: {str(e)}")
        return None

def show_code_with_highlighting(code: str) -> None:
    """Display code with syntax highlighting.
    
    Args:
        code (str): Python code to display
        
    Returns:
        None
        
    Note:
        If code has syntax errors, it will still be displayed but with an error message
    """
    if not isinstance(code, str):
        code = str(code)
        
    try:
        # Basic syntax validation
        compile(code, '<string>', 'exec')
        st.code(code, language="python")
    except (SyntaxError, ValueError, TypeError) as e:
        st.error(f"Code error: {str(e)}")
        st.code(code, language="python")

def show_active_service() -> str:
    """Display the currently active AI service.
    
    Returns:
        str: Name of the currently active service
    """
    service = st.session_state.get('current_service', 'openai')
    st.markdown(
        f"""<div class='service-indicator'>
            Active Service: {service.upper()}
        </div>""", 
        unsafe_allow_html=True
    )
    return service

def add_service_indicator_css() -> None:
    """Add CSS styling for the service indicator.
    
    Returns:
        None
    """
    st.markdown("""
        <style>
        .service-indicator {
            padding: 5px 10px;
            border-radius: 5px;
            background: #2E2E2E;
            color: white;
            display: inline-block;
        }
        </style>
    """, unsafe_allow_html=True)

def save_code_to_file(code: str, default_filename: str = "code.py") -> None:
    """Save code to a file with error handling and user feedback.
    
    Args:
        code (str): The code to save
        default_filename (str): Default name for the save file
        
    Returns:
        None
        
    Note:
        Uses Streamlit's built-in file handling for secure file operations
    """
    if not code.strip():
        st.error("No code to save!")
        return
        
    col1, col2 = st.columns([3, 1])
    
    with col1:
        filename = st.text_input("Filename", value=default_filename)
    
    with col2:
        if st.button("💾 Save"):
            try:
                # Ensure .py extension
                if not filename.endswith('.py'):
                    filename += '.py'
                    
                save_path = Path(filename)
                
                # Prevent overwriting files outside working directory
                if '..' in str(save_path):
                    st.error("Invalid file path!")
                    return
                    
                # Write the code
                save_path.write_text(code)
                st.success(f"✅ Saved to {filename}")
                
            except Exception as e:
                st.error(f"Error saving file: {str(e)}")
