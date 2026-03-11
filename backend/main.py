# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_tables
from api.routes import auth, appointment, livekit
from core.config import settings

# --- Create App ---
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
)

# --- CORS --- React frontend ke liye
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routes ---
app.include_router(auth.router)
app.include_router(appointment.router)
app.include_router(livekit.router)


# --- Startup --- DB tables banao
@app.on_event("startup")
def startup():
    create_tables()
    print("✅ Database tables created")
    print("✅ App started successfully")


# --- Health Check ---
@app.get("/")
def root():
    return {"message": f"{settings.APP_NAME} is running!"}


# --- Run ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)