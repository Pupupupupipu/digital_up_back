from fastapi import APIRouter, Depends, HTTPException
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from db_connection import get_session

from models.models import Film




film_router = APIRouter(tags=["film"], prefix="/film")

@film_router.get('/')
async def get_films(db: AsyncSession = Depends(get_session)):
    films = await db.execute(select(Film))
    print(films)
    if films == None:
        return JSONResponse(status_code=404, content={"message":"Нет записей"})
    return films.scalars().all()

@film_router.get('/id/{id}')
async def get_film( id: int,
    db: AsyncSession = Depends(get_session)):
    try: 
        film = await db.execute(select(Film).filter(Film.id == id))
        return film.scalars().first()
    except Exception as e:
        print(e)
        raise  HTTPException(status_code=500, detail=f"Произошла ошибка: {e}")
    

@film_router.get('/name/{name}')
async def get_film( name: str,
    db: AsyncSession = Depends(get_session)):
    try: 
        print("KDJSNFKSDJFNSKDJN", name)
        films = await db.execute(select(Film).filter(Film.name.ilike(f'{name}%')))
        return films.scalars().all()
    except Exception as e:
        print(e)
        raise  HTTPException(status_code=500, detail=f"Произошла ошибка: {e}")

