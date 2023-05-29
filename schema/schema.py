from typing import List

from pydantic import BaseModel

class Player(BaseModel):
    id: int
    name: str