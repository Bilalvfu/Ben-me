from pydantic import BaseModel, ConfigDict


class PostBase(BaseModel):
    title: str
    content: str
    slug: str


class PostCreate(PostBase):
    author_id: int


class PostResponse(PostBase):
    id: int
    author_id: int

    model_config = ConfigDict(from_attributes=True)
