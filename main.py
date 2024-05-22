from datetime import datetime
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from db_connection import init_db
from routers.router_film import film_router
from routers.router_user import user_router
from routers.router_genre import genre_router


app = FastAPI()

# Add CORS middleware to allow requests from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update this with the origin of your frontend
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
#init_db()
#app.include_router(router)
app.include_router(film_router)
app.include_router(user_router)
app.include_router(genre_router)



@app.on_event("startup")
async def on_startup():
    open("log.txt", mode="a").write(f'{datetime.utcnow()}: Begin\n')
    await init_db()

@app.on_event("shutdown")
async def shutdown():
    open("log.txt", mode="a").write(f'{datetime.utcnow()}: End\n')

@app.get('/')
def main():
    return FileResponse("index.html")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)




