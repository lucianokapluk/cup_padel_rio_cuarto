

from typing import List

from pydantic import BaseModel

from schemas.category import Category
from schemas.tournament_inscription import TournamentInscription


class TournamentBase(BaseModel):
    name: str
    description: str
    mode: str
    category_id: int
    start_date_time: str
    end_date_time: str


class TournamentCreate(TournamentBase):
    pass


class TournamentUpdate(TournamentBase):
    pass


class Tournament(TournamentBase):
    id: int
    category: Category | None
    inscriptions: List[TournamentInscription] | None

    class Config:
        orm_mode = True
