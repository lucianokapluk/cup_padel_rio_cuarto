from typing import List, Optional

from sqlalchemy.orm import Session

from models.tournament_model import TournamentModel
from schemas.tournament import TournamentCreate, TournamentUpdate


def get_tournament(db: Session, tournament_id: int) -> Optional[TournamentModel]:
    return db.query(TournamentModel).filter(TournamentModel.id == tournament_id).first()


def get_tournaments(db: Session, skip: int = 0, limit: int = 100) -> List[TournamentModel]:
    return db.query(TournamentModel).offset(skip).limit(limit).all()


def create_tournament(db: Session, tournament: TournamentCreate) -> TournamentModel:
    db_tournament = TournamentModel(**tournament.dict())
    db.add(db_tournament)
    db.commit()
    db.refresh(db_tournament)
    return db_tournament


def update_tournament(db: Session, tournament_id: int, tournament: TournamentUpdate) -> Optional[TournamentModel]:
    db_tournament = db.query(TournamentModel).filter(
        TournamentModel.id == tournament_id).first()
    if db_tournament:
        for key, value in tournament.dict(exclude_unset=True).items():
            setattr(db_tournament, key, value)
        db.commit()
        db.refresh(db_tournament)
        return db_tournament


def delete_tournament(db: Session, tournament_id: int) -> Optional[TournamentModel]:
    db_tournament = db.query(TournamentModel).filter(
        TournamentModel.id == tournament_id).first()
    if db_tournament:
        db.delete(db_tournament)
        db.commit()
        return db_tournament
