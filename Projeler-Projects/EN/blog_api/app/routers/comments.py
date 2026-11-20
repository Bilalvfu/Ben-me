from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.comment import Comment
from app.models.post import Post
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentResponse

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(payload: CommentCreate, db: Session = Depends(get_db)):
    if not db.query(Post).filter(Post.id == payload.post_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if not db.query(User).filter(User.id == payload.author_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")

    comment = Comment(
        content=payload.content,
        post_id=payload.post_id,
        author_id=payload.author_id,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@router.get("/", response_model=list[CommentResponse])
def list_comments(db: Session = Depends(get_db)):
    return db.query(Comment).all()
