from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#from fastapi_pagination import Page, add_pagination
#from server.routes.usuarios import router as UsuariosRouter
#from server.routes.madurador import router as MaduradorRouter
from server.routes.datos import router as DatosRouter
from server.routes.comando import router as ComandosRouter
from server.routes.receta import router as RecetasRouter



app = FastAPI(
    title="Integracion ZTRACK API TEST",
    summary="Modulos de datos bidireccional",
    version="0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    #allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#añadir el conjunto de rutas de notificaciones
#app.include_router(UsuariosRouter, tags=["usuarios"], prefix="/usuarios")
app.include_router(DatosRouter, tags=["Datos"], prefix="/Datos")
app.include_router(ComandosRouter, tags=["Comandos"], prefix="/Comandos")
app.include_router(RecetasRouter, tags=["Recetas"], prefix="/Recetas")



@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app ztrack by test!"}
