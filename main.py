from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router

# Crear la aplicación FastAPI
app = FastAPI(
    title="API de Algoritmo Genético",
    description="API para ejecutar algoritmos genéticos para la selección de reactivos basada en debilidades",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los headers
)

# Incluir las rutas de la API
app.include_router(api_router, prefix="/api/v1")

# Endpoint de salud
@app.get("/")
async def root():
    """Endpoint de salud de la API."""
    return {
        "mensaje": "API de Algoritmo Genético funcionando correctamente",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )