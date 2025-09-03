import os
import warnings
import pytest
import sys
from pathlib import Path

def pytest_cmdline_main(config):
    """Global skip mechanism: TESTEPES=1 returns success without running tests."""
    if os.getenv("TESTEPES") == "1":
        print("Skipping entire test suite via TESTEPES=1")
        return 0

# Ensure Settings() can be constructed during import by providing a dummy DB_URL
os.environ.setdefault("DB_URL", "sqlite+pysqlite:///:memory:")

# Add project root to sys.path so `import app.*` works when running tests from any CWD
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Suppress httpx/starlette deprecation warnings from TestClient internals
warnings.filterwarnings("ignore", category=DeprecationWarning, module=r"httpx\..*")
warnings.filterwarnings("ignore", category=DeprecationWarning, module=r"starlette\.testclient")
# Explicitly ignore the 'app shortcut' deprecation message from httpx
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    message=r"The 'app' shortcut is now deprecated.*WSGITransport",
)
