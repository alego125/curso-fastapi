from fastapi import FastAPI
import uvicorn
from app.routers import user, auth
from app.db.database import Base,engine


# def crearTablas():
#     Creamos la tabla con el o los modelos que se tienen en base por esto es tan iomportante que los modelos hereden de Base a la hora de declararlos en database.py y luego le indicamos con create_all y bind el engine
#     Base.metadata.create_all(bind=engine)
# crearTablas()

app = FastAPI()
# Incluimos el router dentro de nuestra app
app.include_router(user.router)
app.include_router(auth.router)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)