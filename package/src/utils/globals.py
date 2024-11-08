import glob
import os
<<<<<<< HEAD
=======
import glob
>>>>>>> 3b74dae6a22892a7d127384de2ebead9c54096b9

from dotenv import load_dotenv

load_dotenv("/app/keys/.env")
app_workdir = os.environ.get('APP_WORKDIR')

def work_dir(file: str = None): 
    if file is None:
        raise Exception("No file given")
    return f'{app_workdir}/files/temp/{file}' 

<<<<<<< HEAD
def clean_dir():
=======
def clean_work_dir():

>>>>>>> 3b74dae6a22892a7d127384de2ebead9c54096b9
    files = glob.glob(work_dir("*"))
    for f in files:
        os.remove(f)