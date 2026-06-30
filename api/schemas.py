from pydantic import BaseModel

class TopProduct(BaseModel):
    term: str
    count: int

class ChannelActivity(BaseModel):
    date: str
    posts: int
    avg_views: float

class MessageResult(BaseModel):
    message_id: int
    text: str
    channel: str
    date: str

class VisualStats(BaseModel):
    channel_name: str
    total_posts: int
    image_posts: int
    image_percentage: float