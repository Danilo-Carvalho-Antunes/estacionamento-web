import os
import pytest
import sys
from pathlib import Path

# Skip global: TESTEPES=1 pytest -q
if os.getenv("TESTEPES") == "1":
    pytest.skip("Skipping entire test suite via TESTEPES=1", allow_module_level=True)

# Ensure Settings() can be constructed during import by providing a dummy DB_URL
os.environ.setdefault("DB_URL", "sqlite+pysqlite:///:memory:")

# Add project root to sys.path so `import app.*` works when running tests from any CWD
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
