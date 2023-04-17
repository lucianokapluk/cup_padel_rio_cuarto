
from typing import List, Optional

from pydantic import BaseModel

from schemas.tournament_inscription import TournamentInscription


class GroupBase(BaseModel):
    tournament_id: int
    group_number: int


class GroupCreate(GroupBase):
    pass


class Group(GroupBase):
    id: int

    class Config:
        orm_mode = True
