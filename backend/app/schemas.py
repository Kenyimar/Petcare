from pydantic import BaseModel, ConfigDict


class ContentResponse(BaseModel):
    id: int
    title: str
    category: str
    content_type: str
    summary: str
    body: str

    model_config = ConfigDict(from_attributes=True)