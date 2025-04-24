import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "My Project"
DEBUG = os.getenv("DEBUG", "True") == "True"
