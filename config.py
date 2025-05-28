import os
from dotenv import load_dotenv

# load the .env file
load_dotenv()

# postgress configuration variables
DB_HOST = os.environ.get("DB_HOST")
DB_USER= os.environ.get("DB_USER")
DB_NAME = os.environ.get("DB_NAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_PORT= os.environ.get("DB_PORT")
URL= os.environ.get("URL")


if not DB_PASSWORD:
    raise EnvironmentError("Missing db_password env variable.")

if not DB_USER:
    raise EnvironmentError("Missing db_user env variable.")

if not DB_NAME:
    raise EnvironmentError("Missing db_name env variable.")

if not DB_HOST:
    raise EnvironmentError("Missing db_host env variable.")
