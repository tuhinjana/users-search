from datetime import datetime
from typing import List
from typing import Optional

from pydantic import AnyUrl
from pydantic import BaseModel
from pydantic import Field
from pydantic import validator


class Author(BaseModel):
    name: str
    email: str
    date: datetime

    @validator('date')
    def datetime_to_string(cls, v):
        return v.isoformat()


class CommitterDetails(BaseModel):
    author: Optional[Author]

    class Config:
        arbitrary_types_allowed = True


class CommitSchema(BaseModel):
    sha: str
    commit: CommitterDetails
    html_url: AnyUrl


class RepoSchema(BaseModel):
    id: int
    name: str
    url: AnyUrl
    created_at: str
    updated_at: str
    commit_latest: Optional[CommitSchema]


class SingleResponseSchema(BaseModel):
    user_id: int = Field(..., alias='id')
    login_name: str = Field(..., alias='login')
    resource_uri: AnyUrl = Field(..., alias='url')
    repo_list: Optional[List[RepoSchema]]
