from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from elasticsearch import Elasticsearch
import os
import json
from typing import Dict, Any
import uvicorn

from src.employee.controllers import router as employee_router

app = FastAPI(title="TechIntellect", version="1.0.0")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/pdfs", StaticFiles(directory="pdfs"), name="pdfs")

app.include_router(employee_router, tags=["employee"])

@app.get("/", response_class=HTMLResponse)
async def frontend():
    try:
        if os.path.exists("static/index.html"):
            with open("static/index.html", "r") as f:
                return HTMLResponse(content=f.read())
        else:
            return HTMLResponse(content="Frontend not found")
    except Exception as e:
        return HTMLResponse(content=f"Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
