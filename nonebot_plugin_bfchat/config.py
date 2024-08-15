from pydantic import BaseModel, Field


class Config(BaseModel):
    bfchat_prefix: str = Field(default='/')
    bfchat_dir: str = Field(default='./bfchat_data/')
