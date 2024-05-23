from fastapi import APIRouter, Depends, HTTPException
from db_connection import get_session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import User
from models.schemas import User_create, User_patch
import bcrypt
from config import settings


user_router = APIRouter(tags=["users"], prefix="/users")

# salt = bcrypt.gensalt()
salt = settings.salt.encode('utf-8')



@user_router.post('/')
async def create_user(
    item: User_create,
    db: AsyncSession=Depends(get_session)):
    try:

        existing_user = await db.execute(select(User).filter(User.login == item.login))
        existing_user = existing_user.scalars().all()

        if existing_user != []:
            raise HTTPException(detail="User with this login already exists", status_code=400)
           
        hashed_password = bcrypt.hashpw(item.password.encode('utf-8'), salt)

        user = User(
                    login = item.login,
                    hash_password = str(hashed_password)
                    )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return {"id": user.id, 
                "name": user.name, 
                "login": user.login}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Произошла ошибка: {e}")

@user_router.post('/sign_in')
async def sign_in_user(
    item: User_create,
    db: AsyncSession=Depends(get_session)):

    try:
        hashed_password = bcrypt.hashpw(item.password.encode('utf-8'), salt)
        user = await db.execute(select(User).filter(User.login == item.login))
        user = user.scalars().first()

        if user == None:
            raise HTTPException(detail="User with this login not exists", status_code=400)
        
        if user.hash_password != str(hashed_password):
            raise HTTPException(detail="Incorrect password", status_code=400)
        
        return { "id": user.id, "name": user.name, "login": user.login }
    except Exception as e:
        print(e)
        raise  HTTPException(status_code=500, detail=f"Произошла ошибка: {e}")
    


@user_router.get('/')
async def get_users(db: AsyncSession=Depends(get_session)):
    try:
        users = await db.execute(select(User))

        return users.scalars().all()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Произошла ошибка: {e}")
    
@user_router.patch('/name')
async def change_name_user(
    user_new_name: User_patch,
    db: AsyncSession=Depends(get_session)):
    try:
        user = await db.execute(select(User).filter(User.id == user_new_name.id))

        user = user.scalars().first()
        user.name = user_new_name.new_name
        await db.commit()
        await db.refresh(user)
        return user
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Произошла ошибка: {e}")
