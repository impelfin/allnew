import pandas as pd 
from sqlalchemy import create_engine
from PIL import Image
import base64
from io import BytesIO
from typing import List
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import uvicorn
import os.path
import json

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
secret_file = os.path.join(BASE_DIR, '../secret.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        errorMsg = "Set the {} environment variable.".format(setting)
        return errorMsg

HOSTNAME = get_secret("Mysql_Hostname")
PORT = get_secret("Mysql_Port")
USERNAME = get_secret("Mysql_Username")
PASSWORD = get_secret("Mysql_Password")
DBNAME = get_secret("Mysql_DBname")

DB_URL = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DBNAME}'

engine = create_engine(DB_URL, pool_recycle=500)

def InsertImageDB(filename):
## jpg dpi 100x100, png dpi 72x72
    with open(filename, "rb") as image_file:
        binary_image = image_file.read()
        binary_image = base64.b64encode(binary_image)
        binary_image = binary_image.decode('UTF-8')
        img_df = pd.DataFrame({'image_data':[binary_image]})
        img_df.to_sql('images', con=engine, if_exists='append', index=False)
    return f'Image file : {filename} Inserted~!!'

# “/”로 접근할 때 보여줄 HTML 코드 (가장 기본적으로 보여지는 부분)
@app.get("/")
async def main():
    content = """
<body>
<h3>Image File Upload to MySQL DB</h3>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    UPLOAD_DIRECTORY = "./"
    for file in files:
        contents = await file.read()
        with open(os.path.join(UPLOAD_DIRECTORY, file.filename), "wb") as fp:
            fp.write(contents)

    filename = [file.filename for file in files]
    print({"filenames": filename})  

    result = InsertImageDB(filename[0])
    return result

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=3000)
    