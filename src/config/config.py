from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import json
import os


def find_or_create_json_file(config_path="/src/config/db/default-db.json"):
    home_directory = os.getcwd()
    
    full_config_path = home_directory + config_path
    
    default_json = {}

    if not os.path.exists(full_config_path):
        os.makedirs(full_config_path[:-11])

        with open(full_config_path,'w')as f:
            json.dump(default_json, f)

    return full_config_path

dotenv_path = find_dotenv(filename='.env')

if not Path(dotenv_path).exists():
    os.system("touch .env")

load_dotenv(dotenv_path)

DB_PATH = os.getenv('DB_PATH')
DB_PATH = find_or_create_json_file(DB_PATH)
print(DB_PATH)