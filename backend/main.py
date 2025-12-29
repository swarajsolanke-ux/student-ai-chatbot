
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from routers import auth, chat, upload, admin, application, university, assessment
import uvicorn

app = FastAPI(
    title="University Recommendation Platform",

)



# Include routers
app.include_router(auth.router)
app.include_router(university.router)
app.include_router(application.router)
app.include_router(assessment.router)
app.include_router(chat.router)
app.include_router(upload.router)
app.include_router(admin.router)

app.mount(
    "/static",
    StaticFiles(directory="frontend/static"),
    name="static"
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "University Recommendation Platform",
        "version": "1.0.0"
    }

@app.get("/", response_class=HTMLResponse)
def root():
    """Serve landing page"""
    return FileResponse(path="frontend/static/templates/landing.html")

@app.get("/login", response_class=HTMLResponse)
def login_page():
    return FileResponse(path="frontend/static/templates/login.html")

@app.get("/register", response_class=HTMLResponse)
def register_page():
    return FileResponse(path="frontend/static/templates/register.html")

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_page():
    return FileResponse(path="frontend/static/templates/dashboard.html")

@app.get("/assessment", response_class=HTMLResponse)
def assessment_page():
    return FileResponse(path="frontend/static/templates/assessment.html")

@app.get("/profile", response_class=HTMLResponse)
def profile_page():
    return FileResponse(path="frontend/static/templates/profile.html")

@app.get("/settings", response_class=HTMLResponse)
def settings_page():
    return FileResponse(path="frontend/static/templates/settings.html")

if __name__ == "__main__":
    from database_enhanced import create_enhanced_schema, seed_enhanced_data
    try:
        conn = create_enhanced_schema()
        seed_enhanced_data(conn)
        conn.close()
        print("Database initialized successfully!")
    except Exception as e:
        print(f" Database initialization: {e}")
    
    
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
