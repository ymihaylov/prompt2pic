from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    tags=["home"],
)


class HelloResponse(BaseModel):
    message: str


@router.get("/", response_model=HelloResponse)
async def read_root():

    return HelloResponse(
        message="There's nothing for you to do here, you should go! 🥔"
    )
