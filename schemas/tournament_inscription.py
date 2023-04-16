

from typing import Optional

from pydantic import BaseModel, Field


class TournamentInscriptionBase(BaseModel):
    first_player: int
    second_player: int
    rate_date_time: str


class TournamentInscriptionCreate(TournamentInscriptionBase):
    pass


class TournamentInscription(TournamentInscriptionBase):
    id: int

    class Config:
        orm_mode = True
