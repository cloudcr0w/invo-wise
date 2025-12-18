from fastapi import APIRouter

router = APIRouter(prefix="/version", tags=["version"])

VERSION = "0.1.0"   # do przyszłego Gita

@router.get("")
def read_version():
    return {"version": VERSION}
