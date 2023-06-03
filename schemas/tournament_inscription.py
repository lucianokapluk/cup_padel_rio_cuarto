

from datetime import date, datetime
from typing import Optional

from click import DateTime
from pydantic import BaseModel, Field

from schemas.user import User


class TournamentInscriptionBase(BaseModel):
    position: int | None
    updated_at: str | None
    rate_date_time: str


class TournamentInscriptionCreate(TournamentInscriptionBase):
    first_player_id: int
    second_player_id: int


class TournamentInscription(TournamentInscriptionBase):
    id: int
    first_player: User
    second_player: User

    class Config:
        orm_mode = True
