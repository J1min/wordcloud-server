from pydantic import BaseModel


class wordcloud(BaseModel):
    content: str

    class Config:
        orm_mode: True


class photo(BaseModel):
    photo_url: str

    class Config:
        orm_mode: True
