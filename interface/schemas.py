from pydantic import BaseModel


class wordcloud(BaseModel):
    content: str

    class Config:
        orm_mode: True
