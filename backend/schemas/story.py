from pydantic import BaseModel

class StoryBase(BaseModel):
    title: str
    content: str

class StoryCreate(StoryBase):
    pass

class Story(StoryBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
