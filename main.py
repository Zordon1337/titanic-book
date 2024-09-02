from fastapi import *
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
import uvicorn
import glob
from typing import List
import pymysql
from jinja2 import *
from fastapi.templating import Jinja2Templates
app = FastAPI()
app.mount("/images", StaticFiles(directory="images"), name="images")
app.mount("/static", StaticFiles(directory="static"), name="static")
security = HTTPBasic()
idkshit = {
    "admin": "recorderinthesandybridge"
}
templates = Jinja2Templates(directory="templates")
connection = pymysql.connect(
        host='localhost',
        user='root',
        password='test',
        database='booktitanic',
        cursorclass=pymysql.cursors.DictCursor 
)
def auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_password = idkshit.get(credentials.username)
    if not correct_password or correct_password != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-auth": "Basic"},
        )
    return credentials.username

@app.get("/")
def handle_index():
    return templates.TemplateResponse("home.html", {"request": {}, "x": glob.glob("./images/*")})

@app.post("/upload")
async def upload(desc: str = Form(...,alias='desc'),file: UploadFile = File(...), username: str = Depends(auth)):
    connection.ping(True)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO `gifs` (`file`, `tag`) VALUES (%s, %s);", (f"./images/{file.filename}", desc))
    connection.commit()
    with open(f"./images/{file.filename}", "wb") as f:
        f.write(await file.read())
    return {"Result":"Ok"}
@app.get("/search")
async def search(query: str = Query(..., alias="q")):
    connection.ping(True)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM gifs")
    results = cursor.fetchall()
    return templates.TemplateResponse("search.html", {"request": {}, "query": query, "results": results})
    
        
@app.get("/upload")
def upload_get(username: str = Depends(auth)):
    content = """
    <body>
    <form action="/upload/" enctype="multipart/form-data" method="post">
    <input name="file" type="file">
    <input name="desc" placeholder="Description of this gif, please use gifs text">
    <input type="submit">
    </form>
    </body>
    """
    return Response(content)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=14660)
