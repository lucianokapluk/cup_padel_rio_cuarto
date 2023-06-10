from pydantic import BaseModel


class MatchBase(BaseModel):
    first_inscription_id: int
    second_inscription_id: int
    winer: int
    tournament_id: int
    group_id: int
    result: str
    date_time_match: str


class MatchCreate(MatchBase):
    pass


class MatchUpdate(MatchBase):
    pass


class Match(MatchBase):
    id: int

    class Config:
        orm_mode = True
