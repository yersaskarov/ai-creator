import os
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("PYTHON_DOTENV_DISABLED", "1")
os.environ.setdefault("TELEGRAM_BOT_TOKEN", "123456:dummy_token_for_tests")
