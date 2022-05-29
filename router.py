import uvicorn
from fastapi import FastAPI, Body, Depends, APIRouter
# import router

router = APIRouter()


@router.get("/", tags=["greatings"])
async def list_users():
	return {"hello": "World"}
    
