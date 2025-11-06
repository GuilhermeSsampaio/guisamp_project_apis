from fastapi import APIRouter

router = APIRouter(prefix="/diaries")

@router.get("/show_diary/{user_id}")
def show_diary():
    pass

@router.post("/create_diary/{user_id}")
def create_diary():
    pass

@router.post("/update_diary/{user_id}/{diary_id}")
def update_diary():
    pass

@router.delete("/delete_diary/{user_id}/{diary_id}")
def delete_diary():
    pass