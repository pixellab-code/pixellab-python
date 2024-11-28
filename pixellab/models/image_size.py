from pydantic import BaseModel, Field


class ImageSize(BaseModel):
    width: int = Field(default=128, ge=16, le=200)
    height: int = Field(default=128, ge=16, le=200)
