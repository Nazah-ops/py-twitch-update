import glob
import os

from dotenv import load_dotenv

load_dotenv("/app/keys/.env")
app_workdir = os.environ.get('APP_WORKDIR')

def work_dir(file: str = None): 
    if file is None:
        raise Exception("No file given")
    return f'{app_workdir}/files/temp/{file}' 

def clean_dir():
    files = glob.glob(work_dir("*"))
    for f in files:
        os.remove(f)