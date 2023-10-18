from pydantic import BaseModel


class QueryOrderBySchema(BaseModel):
    column_name: str
    sort_desc: bool
