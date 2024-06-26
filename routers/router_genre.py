from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession
from db_connection import get_session
from models.models import Genre

genre_router = APIRouter(tags=['genre'], prefix='/genre')

@genre_router.post('/')
async def quick_add(
        item: str,
        db: AsyncSession = Depends(get_session)):
    try:
        query = text(item)
        await db.execute(query)
        await db.commit()
        return "Genres added"
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Произошла ошибка: {e}")

@genre_router.get('/{id}')
async def get_genre(id: int,
    db: AsyncSession = Depends(get_session)):
    try:
        genre = await db.execute(select(Genre).filter(Genre.id == id))
        return genre.scalars().first()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Произошла ошибка: {e}")