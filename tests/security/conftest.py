import pytest
from AuditronAI.core.security_analyzer import SecurityAnalyzer

@pytest.fixture
def security_analyzer():
    """Shared fixture for SecurityAnalyzer instance."""
    analyzer = SecurityAnalyzer()
    yield analyzer
    # Ensure cleanup after each test
    if analyzer._temp_manager.temp_dir and analyzer._temp_manager.temp_dir.exists():
        analyzer._temp_manager.cleanup()
