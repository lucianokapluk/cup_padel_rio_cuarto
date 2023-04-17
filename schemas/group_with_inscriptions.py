from typing import List

from pydantic import BaseModel

from schemas.group import Group
from schemas.tournament_inscription import TournamentInscription


class GroupWithInscriptions(BaseModel):
    group: Group
    inscriptions: List[TournamentInscription] = []

    class Config:
        orm_mode = True


class TournamentWithGroupInscriptions(BaseModel):
    tournament_id: int
    items: List[GroupWithInscriptions] = []

    class Config:
        orm_mode = True
