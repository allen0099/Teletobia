import os
from pathlib import Path

from .env import Env

# Read environment file from .env file
env: Env = Env()
BASE_DIR = Path(__file__).resolve().parent.parent
Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
TELEGRAM_API_ID = env.str("TELEGRAM_API_ID")
TELEGRAM_API_HASH = env.str("TELEGRAM_API_HASH")
TELEGRAM_BOT_TOKEN = env.str("TELEGRAM_BOT_TOKEN")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", False)
