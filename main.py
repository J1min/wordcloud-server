from fastapi import FastAPI, Response
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import os
import boto3
import uuid
from interface import schemas, model
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()

AWS_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


boto3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)


@app.post("/wordcloud")
async def create_wordcloud(body: schemas.wordcloud):

    wordcloud = WordCloud(font_path='./font/Pretendard-Medium.otf',  # 글꼴 설정
                          background_color='white',
                          max_words=16,
                          width=512,
                          height=512).generate(body.content)

    wordcloud_image = wordcloud.to_image().convert('RGB')
    image_byte = io.BytesIO()

    wordcloud_image.save(image_byte, format='PNG')
    image_byte.seek(0)

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.close()

    random_uuid = uuid.uuid4()
    file_name = f'{random_uuid}.png'
    boto3_client.upload_fileobj(image_byte, AWS_BUCKET_NAME, file_name)

    return {
        "message": "Wordcloud created and uploaded to S3!",
        "url": f"http://localhost:8000/wordcloud/{random_uuid}.png"
    }


@app.get("/wordcloud/{file_name}")
def get_file(file_name: str):
    response = boto3_client.get_object(
        Bucket=AWS_BUCKET_NAME,
        Key=file_name)

    file_data = response["Body"].read()
    return Response(content=file_data, media_type="image/png")
