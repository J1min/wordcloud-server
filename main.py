from fastapi.responses import FileResponse
import os
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from konlpy.tag import Okt
from wordcloud import WordCloud
from dotenv import load_dotenv
from boto3 import client
from io import BytesIO
from os import environ
from uuid import uuid4

import matplotlib.pyplot as plt
from PyKomoran import *

from interface import schemas, model

app = FastAPI()
load_dotenv()

AWS_BUCKET_NAME = environ.get('AWS_BUCKET_NAME')
AWS_ACCESS_KEY = environ.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY = environ.get('AWS_SECRET_KEY')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


SAVE_DIR = "./wordcloud_images"


@app.patch("/wordcloud")
async def create_wordcloud(body: schemas.wordcloud):

    random_uuid = uuid4()
    file_name = f'{random_uuid}.png'
    local_file_path = os.path.join(SAVE_DIR, file_name)

    wordcloud = WordCloud(font_path='./font/Pretendard-Medium.otf',
                          background_color='white',
                          max_words=16,
                          width=512,
                          height=512).generate(body.content)

    wordcloud_image = wordcloud.to_image().convert('RGB')
    image_byte = BytesIO()

    wordcloud_image.save(local_file_path, format='PNG')

    return {
        "message": "Wordcloud created and saved locally!",
        "url": f"http://192.168.10.253:8001/wordcloud/{random_uuid}.png"
    }


@app.get("/wordcloud/{file_name}")
def get_file(file_name: str):
    local_file_path = os.path.join(SAVE_DIR, file_name)
    return FileResponse(local_file_path, media_type="image/png")
