# main.py - Part of backend module
from fastapi import FastAPI
from routers import auth, chat, upload, admin, application
import uvicorn
from fastapi.middleware.cors import  CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse,HTMLResponse
app = FastAPI(title="Student AI Chatbot")

app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(upload.router)
app.include_router(admin.router)
app.include_router(application.router)


app.mount(
    "/static",
    StaticFiles(directory="frontend/static"),
    name="static"
)

#added the middleware 
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
     "*"  
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/",response_class=HTMLResponse)
def root():
    return FileResponse(path="frontend/static/templates/index.html")
if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0",port=8000)






