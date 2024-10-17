from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST=os.environ.get("DB_HOST")
DB_PORT=os.environ.get("DB_PORT")
DB_NAME=os.environ.get("DB_NAME")
DB_USER=os.environ.get("DB_USER")
DB_PASS=os.environ.get("DB_PASS")
DB_SCHEMA=os.environ.get("DB_SCHEMA")

TOKEN_COOKIE_NAME = "token"
CSRF_TOKEN_SECRET = "__CHANGE_THIS_WITH_YOUR_OWN_SECRET_VALUE__"
