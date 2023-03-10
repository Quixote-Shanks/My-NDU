from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

from fastapi.params import Body
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import engine, get_db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import mode
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Post']
)


@router.get("/", response_model=List[schemas.PostOut])
# @router.get("/")
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 5, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""select * FROM posts """)
    # posts = cursor.fetchall()

    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # posts = db.query(models.Post).filter(
    #     models.Post.owner_id == current_user.id).all()

    # if not posts:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"You do not have any posts")

    # if posts.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail=f"Is it your posts?")
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts


@ router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(posts: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                (posts.title, posts.content, posts.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # print(current_user.email)
    # print(current_user.id)
    new_post = models.Post(owner_id=current_user.id, **posts.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@ router.get('/{id}', response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE ID = %s """, (str(id)))
    # get_post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).first()

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")

    return posts


@ router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s returning * """, (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_querry = db.query(models.Post).filter(models.Post.id == id)

    post = post_querry.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exists")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Is it your post?, why do you want to delete it?")

    post_querry.delete(synchronize_session=False)
    db.commit()

    return {"data_detail": post}


@ router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (posts.title, posts.content, posts.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exists")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Go and update your own post, leave other people posts alone")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
