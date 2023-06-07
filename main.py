from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func, select
from wordcloud import WordCloud
import matplotlib.pyplot as plt

from interface import model, schemas
from util import db_util
import database
import boto3
import uuid

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.put("/wordcloud")
def put_board(body: schemas.wordcloud, db: Session = Depends(db_util.get_db)):
    wordcloud_data = model.wordcloud(content=body.content)

    wordcloud = WordCloud(font_path='./font/Pretendard-Medium.otf',  # 글꼴 설정
                          background_color='white',
                          max_words=20,
                          width=800,
                          height=800)

    wordcloud.generate(wordcloud_data)

    plt.imshow(wordcloud, interpolation='none')
    plt.axis('off')
    plt.savefig('wordcloud.png', dpi=300)

    return {"response": wordcloud_data}


def upload_file(fileName, file):
    s3 = boto3.resource("s3")
    s3.Bucket('wordcloud-storage').put_object(
        Key=fileName, Body=file, ContentType="image/jpeg")
    return


@app.post("/photo")  # 사진 post
async def upload_photo(file: UploadFile, db: Session = Depends(db_util.get_db)):
    content = await file.read()
    href = f"{str(uuid.uuid4())}.jpeg"  # uuid로 유니크한 파일명으로 변경
    upload_file(href, content)

    quote_data = model.quote(
        quote_content=body.quote_content, character_name=body.character_name)
    db_util.post_db(db, quote_data)

    return photoData
