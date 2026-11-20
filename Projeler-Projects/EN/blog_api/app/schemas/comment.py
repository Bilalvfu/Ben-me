from pydantic import BaseModel, ConfigDict


class CommentCreate(BaseModel):
    content: str
    post_id: int
    author_id: int


class CommentResponse(BaseModel):
    id: int
    content: str
    post_id: int
    author_id: int

    model_config = ConfigDict(from_attributes=True)
