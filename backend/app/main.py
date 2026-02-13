from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, users, services, applications, services_api, whatsapp, documents, services_data, portal_redirect, proxy, torrent_power, torrent_power
from app.config import get_settings

settings = get_settings()

# Create database tables (only creates if they don't exist)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="Unified Portal for Gas, Electricity, Water & Property Services",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(services.router)
app.include_router(services_api.router)
app.include_router(services_data.router)
app.include_router(portal_redirect.router)
app.include_router(applications.router)
app.include_router(documents.router)
app.include_router(whatsapp.router)
app.include_router(proxy.router)
app.include_router(torrent_power.router)
app.include_router(torrent_power.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to Unified Services Portal",
        "services": ["Electricity", "Gas", "Water", "Property"],
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
