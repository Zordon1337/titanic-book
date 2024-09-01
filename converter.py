import pymysql
from PIL import Image
from pytesseract import *
import os
connection = pymysql.connect(
        host='localhost',
        user='root',
        password='test',
        database='booktitanic',
        cursorclass=pymysql.cursors.DictCursor 
)
cursor = connection.cursor()
for file_name in os.listdir("./images"):
    file_path = os.path.join("./images", file_name)
    if os.path.isfile(file_path):
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
        cursor.execute("INSERT INTO `gifs` (`file`, `tag`) VALUES (%s, %s);", (file_path, text))
        print(f"{file_path} done")
connection.commit()